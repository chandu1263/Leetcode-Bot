import discord
import os

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
    return embed