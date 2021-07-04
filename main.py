import os
import discord
import time

from parser import parse, get_username
from database import *
from bot_embeds import get_question_embed, get_leaderboard_embed, get_help_embed

client = discord.Client()
posted_questions = {}

@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

	if message.author == client.user:
		return
	
	if message.content.startswith("!lc"):
		user_id = message.author.id
		command = parse(message.content)
		
		if command[0] == "ping":
			await message.channel.send("pong!")
			return
		
		if command[0] == "help":
			await message.channel.send(embed=get_help_embed())
			return

		if command[0] == "register": #reigster request
			if len(command) > 2: #invalid request
				await message.channel.send("Invalid request!")
				return
			user = get_user_from_users(user_id)
			if user["status"] == "failure":
				await message.channel.send("Bot is down, please reach out to the bot owners")
				return
			if user["value"][0] != "": # no user
				await message.channel.send("User already registered with username: " + str(user["value"][1]))
				return
			else:
				username = message.author.name
				if len(command) > 1: # user provided a username
					username = command[1]
				status = add_user_to_users(user_id, username)
				if status["status"] == "failure":
					await message.channel.send("User registration failed!!")
					print(status)
					return
				else:
					await message.channel.send("User successfully registered!!")
					print(status)
					return

		if command[0] == "moderator": # get or add moderator

			if len(command) > 2: # invalid request
				await message.channel.send("Invalid request!")
				return

			if len(command) == 1: # get moderators
				result = get_moderators()
				if result["status"] == "failure":
					await message.channel.send(result["reason"])
					return
				moderators = result["moderators"]
				if len(moderators) == 0:
					await message.channel.send("No moderators yet!")
					return
				mods = ""
				for moderator in moderators:
					moderator_profile = await client.fetch_user(int(moderator))
					mods += moderator_profile.name + ", "
				mods = mods[:-2]
				await message.channel.send(mods)
				return
			
			if len(command) == 2: # add moderator
				if not message.author.guild_permissions.administrator:
					await message.channel.send("Only admin can add a moderator!")
					return
				new_moderator = message.mentions[0].id
				result = add_moderator(new_moderator)
				if result["status"] == "failure":
					await message.channel.send(result["reason"])
					return
				await message.channel.send("moderator added successfully!")
				return

		if command[0] == "post":

			if len(command) > 1: # invalid request
				await message.channel.send("Invalid request!")
				return	

			if not is_moderator(user_id): # question requested by not moderator
				await message.channel.send("You don't have access to post a question!")
				return

			result = get_next_question()
			if result["status"] == "failure": # internal server error
				await message.channel.send("Bot is down, please reach out to bot owner")
				return

			if result["question"] == -1: # all the questions in database are posted
				await message.channel.send("No more questions, add a new question")
				return

			with open("temp/posted.txt", "a") as f:
				f.write(str(result["question"]) + "\n")
			posted_question = await message.channel.send(embed=get_question_embed(result["question"], result["intro"], result["level"], result["acceptance"], result["points"], result["url"]))
			add_to_posted(posted_question.id, result["question"])
			posted_questions[posted_question.id] = time.time()
			await posted_question.add_reaction("👍")
			await posted_question.add_reaction("✅")
			await posted_question.add_reaction("🖐️")
			return 

		if command[0] == "leaderboard":

			if len(command) > 1:
				await message.channel.send("Invalid request!")
				return

			await message.channel.send(get_leaderboard_embed())
			return
			


@client.event
async def on_raw_reaction_add(payload):
	
	if payload.member == client.user:
		return

	for message_id in posted_questions:
		if time.time() - posted_questions[message_id] > 86400*4:
			print("removing message ", message_id)
			posted_questions.pop(message_id)
	
	if payload.message_id in posted_questions:
		result = get_questionid_from_posted(payload.message_id)
		if result["status"] == "failure":
			await message.channel.send("Bot is down, please reach out to bot owner")
			return
		question_id = result["question_id"]
		
		if not is_user_in_users(payload.user_id):
			user = await client.fetch_user(int(payload.user_id))
			dmchannel = await user.create_dm()
			await dmchannel.send("please register yourself by sending !lc register <username> before solving")
			return

		if payload.emoji.name == '👍':
			result = add_to_attempted(payload.user_id, question_id)
			if result["status"] == "failure":
				print(result["reason"])
				return
			result = add_attempted_for_user(payload.user_id)
			if result["status"] == "failure":
				print(result["reason"])
				return
			add_points_to_user(payload.user_id, 1)
			return

		if payload.emoji.name == '✅':
			result = add_to_solved(payload.user_id, question_id)
			if result["status"] == "failure":
				print(result["reason"])
				return
			result = add_solved_for_user(payload.user_id)
			if result["status"] == "failure":
				print(result["reason"])
				return
			result = get_points_for_question(question_id)
			if result["status"] == "failure":
				print(result["reason"])
				return
			add_points_to_user(payload.user_id, result["points"])
			return
		
		if payload.emoji.name == '🖐️':
			print(payload.user_id, "needs help", payload.message_id)
			return


client.run(os.getenv('TOKEN'))