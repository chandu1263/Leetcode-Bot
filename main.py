import os
import discord

from parser import parse, get_username
from database import *

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
				

client.run(os.getenv('TOKEN'))

'''
<Message id=855859088202006538 channel=<TextChannel id=855851138049507360 name='general' position=0 nsfw=False news=False category_id=855851138049507358> type=<MessageType.default: 0> author=<Member id=632171686807994371 name='longshot_007' discriminator='4675' bot=False nick=None guild=<Guild id=855851137604517959 name='Testing' shard_id=None chunked=False member_count=3>> flags=<MessageFlags value=0>>
<Message id=855859088742285346 channel=<TextChannel id=855851138049507360 name='general' position=0 nsfw=False news=False category_id=855851138049507358> type=<MessageType.default: 0> author=<Member id=855851833020776458 name='leetcode bot' discriminator='5902' bot=True nick=None guild=<Guild id=855851137604517959 name='Testing' shard_id=None chunked=False member_count=3>> flags=<MessageFlags value=0>>
'''