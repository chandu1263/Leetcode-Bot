import os
import discord

from parser import parse, get_username
from database import *
from bot_embeds import get_question_embed

client = discord.Client()

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
			add_to_posted(message.id)
			await message.channel.send(embed=get_question_embed(result["question"], result["intro"], result["level"], result["acceptance"], result["points"]))
			return 

client.run(os.getenv('TOKEN'))