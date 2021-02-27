import discord 

import os

import requests

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Client()

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")

        guild_count += 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
    msg = message.content
    msgArray = msg.split(" ")
    if msgArray[0] != "cfbot":
        await message.channel.send("start the command by cfbot")
    else:
        if msgArray[1] == "rate":
            res = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[2])
            data = res.json()
            await message.channel.send(data["result"][0]["maxRating"])
        if msgArray[1] == "compare":
            if(len(msgArray)<=3):
                await message.channel.send("Error: 2 parameters required")
            else:
                res1 = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[2])
                res2 = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[3])
                data1 = res1.json()
                data2 = res2.json()
                rating1 = data1["result"][0]["rating"]  
                rating2 = data2["result"][0]["rating"]
                r1 = str(rating1)
                r2 = str(rating2)
                rank1 = str(data1["result"][0]["rank"])
                rank2 = str(data2["result"][0]["rank"])
                if rating2 >= rating1:
                    diff = str(rating2 - rating1)
                    await message.channel.send(msgArray[3] + " has higher rating than " + msgArray[2] + " by a margin of " + diff + "\n" + msgArray[3] + " is a " + rank2 + "(" + r2 + ")" + " and " + msgArray[2] + " is a " + rank1 + "(" + r1 + ")" )
                else:
                    diff = str(rating1 - rating2)
                    await message.channel.send(msgArray[2] + " has higher rating than " + msgArray[3] + " by a margin of " + diff + "\n" + msgArray[2] + " is a " + rank1 + "(" + r1 + ")" + " and " + msgArray[3] + " is a " + rank2 + "(" + r2 + ")" )
        if msgArray[1] == "hello":
            await message.channel.send("hey dirtbag")

bot.run("ODE0OTIyODE0ODc1MzY5NTM0.YDk6Aw.qfchD2w1omHTKE1PR6gmbLsLUGo")