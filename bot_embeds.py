import discord
import os

from tabulate import tabulate

from database import *
from s3_file_handler import S3_file_handler

def get_question_embed(id, intro, level, acceptance, points):
    def get_description(id):
        description = ""
        s3_file_handler = S3_file_handler()
        s3_file_handler.download_file(str(id)+".txt", "temp/"+str(id)+".txt")
        with open("temp/"+str(id)+".txt", "r") as f:
            for line in f:
                description += line
        os.remove("temp/"+str(id)+".txt")
        return description
    embed = discord.Embed(title=intro, description=get_description(id), color=discord.Color.blue())
    embed.add_field(name="level", value=level)
    embed.add_field(name="acceptance", value=acceptance)
    embed.add_field(name="points", value=points)
    embed.add_field(name="reactions", value="attempt the question by reacting 👍 and if you have solved it, react ✅")
    embed.add_field(name="help", value="🖐️ will alert the moderators and you will be provided help")
    return embed


def get_leaderboard_embed():
    result = get_top_users()
    if result["status"] == "failure":
        print(result["reason"])
        users = []
    else:
        users = result["users"]
    heading = ['username', 'rating', 'attempted', 'solved']
    myTable = '```' + tabulate(users, headers=heading, tablefmt="grid") + '```'
    return myTable
    
def get_help_embed():
    description = "```"
    description += "'!lc regsiter' to register yourself with discord username" + "\n"
    description += "\n"
    description += "\n"
    description += "'!lc regsiter <user_name>' to register yourself with given user_name" + "\n"
    description += "         EG: !lc register botguy" + "\n"
    description += "\n"
    description += "\n"
    description += "'!lc moderator' to check who are the moderators" + "\n"
    description += "\n"
    description += "\n"
    description += "'!lc moderator @mention' to add a moderator, only server admin can add moderators" + "\n"
    description += "\n"
    description += "\n"
    description += "'!lc post' bot gives users a question to solve" + "\n"
    description += "          Note: only moderators can post a question, please don't post more than 2 questions a day" + "\n"
    description += "          Registered users can react to the message as mentioned to attempt, solve the question" + "\n"
    description += "          Registered user can also ask for help for the question my reacting as mentioned" + "\n"
    description += "\n"
    description += "\n"
    description += "Ratings will be provided for each registered user and rating can be increased by solving more questions" + "\n"
    description += "\n"
    description += "\n"
    description += "'!lc leaderboard' to get the leaderboard of all the users" + "\n"
    description += "\n"
    description += "\n"
    description += "Each question has some points, users can earn points by solving the question" + "\n"
    description += "User will be provided 1 point for attempting a question" + "\n"
    description += "\n"
    description += "\n"
    description += "```"
    embed = discord.Embed(title="Hi! Here are the commands you can give me: ", description=description, color=discord.Color.green())
    return embed