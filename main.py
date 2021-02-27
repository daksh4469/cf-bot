import discord 
import time as tm
import os
import unittest
import sys
from PIL import Image
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Client()

import datetime

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
    if msgArray[0] == "bunny":
        if msgArray[1] == "help":
            helpmsg = discord.Embed(title="Welcome to Bunny: The CF Bot!", description="There are several commands that you can use, to stalk people ofc ;)", color = 0x34ebab)
            helpmsg.add_field(name = "bunny hello", value = "Greet the bot losers", inline = False)
            helpmsg.add_field(name = "bunny rate *username*", value = "Gets the CodeForces rating of the desired user", inline = False)
            helpmsg.add_field(name = "bunny rank *username*", value = "Gets the CodeForces rank of the desired user", inline = False)
            helpmsg.add_field(name = "bunny max *username*", value = "Gets the CodeForces peak statistics of the desired user", inline = False)
            helpmsg.add_field(name = "bunny online *username*", value = "Gets the last online appearance of the desired user on CodeForces", inline = False)
            helpmsg.add_field(name = "bunny compare *username1* *username2*", value = "Gets the comparison of the CodeForces rating of the desired user", inline = False)
            helpmsg.add_field(name = "bunny contests u", value = "Get the info on upcoming contests on CodeForces", inline = False)
            helpmsg.add_field(name = "bunny contests c", value = "Get the info on recently completed contests on CodeForces", inline = False)
            helpmsg.add_field(name = "bunny recent *username*", value = "Gets the recently solved question of the desired user", inline = False)
            helpmsg.add_field(name = "bunny cmp *username1* *username2*", value = "Create a vizualisation of the comparison between two CodeForces users", inline = False)
            await message.channel.send(embed = helpmsg)

        if msgArray[1] == "rate":
            res = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[2])
            data = res.json()
            await message.channel.send(data["result"][0]["rating"])

        if msgArray[1] == "rank":
            res = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[2])
            data = res.json()
            await message.channel.send(data["result"][0]["rank"])
            
        if msgArray[1] == "max":
            res = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[2])
            data = res.json()
            finalmsg = str(data["result"][0]["maxRating"]) + "(" + data["result"][0]["maxRank"] + ")"
            await message.channel.send(finalmsg)

        if msgArray[1] == "online":
            res = requests.get("https://codeforces.com/api/user.info?handles=" + msgArray[2])
            data = res.json()
            await message.channel.send("Last Online: " + str(datetime.datetime.fromtimestamp(int(str(data["result"][0]["lastOnlineTimeSeconds"])) ).strftime('%Y-%m-%d %H:%M:%S')))

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
        if msgArray[1] == "cmp":
            driver=webdriver.Chrome(executable_path=r"C:\\Users\\91852\\OneDrive\\Desktop\\basicbot\\chromedriver\\tools\\chromedriver.exe")
            driver.get("https://cfviz.netlify.app/compare.html")
            handle1=driver.find_element_by_xpath('//*[@id="handle1"]')
            handle2=driver.find_element_by_xpath('//*[@id="handle2"]')
            cmpbutton=driver.find_element_by_xpath('//*[@id="submitButton"]')
            handle1.send_keys(msgArray[2])
            handle2.send_keys(msgArray[3])
            cmpbutton.click()
            driver.maximize_window()
            tm.sleep(10)
            driver.save_screenshot('my_screenshot.png')
            img = Image.open("my_screenshot.png")
            area = (100, 330, 1800, 800)
            img.crop(area).save("my_screenshot.png",'PNG')
            out=discord.Embed(title="comparison",description="",color=0x34ebab)
            file = discord.File("my_screenshot.png", filename="image.png")
            out.set_image(url="attachment://image.png")
            await message.channel.send(file=file,embed=out)
            driver.quit()

        if msgArray[1] == "hello":
            username = str(message.author.name)
            await message.channel.send("Hey " + username + "......What's up?")

        if msgArray[1] == "contests":
            if msgArray[2] == "u":
                res = requests.get("https://codeforces.com/api/contest.list?phase=BEFORE")
                data = res.json()
                finalmsg = ""
                for i in range(5):
                    hours = data["result"][i]["durationSeconds"]/3600
                    days = 0
                    time = str(hours) + " hours"
                    timeUnit = "hours"
                    if hours >= 24:
                        days = hours//24
                        hours = hours%24
                        timeUnit = "days"
                        time = str(days) + " days " + str(hours) + " hours"
                    finalmsg = finalmsg + "Contest: " + str(data["result"][i]["name"]) + " ---------- " + "Duration Time: " + time + "\n>>>>> Start Time:   " + str(datetime.datetime.fromtimestamp( int(str(data["result"][i]["startTimeSeconds"])) ).strftime('%Y-%m-%d %H:%M:%S')) + "\n\n"
                await message.channel.send(finalmsg)
            elif msgArray[2] == "c":
                res = requests.get("https://codeforces.com/api/contest.list?gym=true")
                data = res.json()
                finalmsg = ""
                n = len(data["result"])
                for i in range(5):
                    hours = data["result"][(-(i+1))]["durationSeconds"]/3600
                    days = 0
                    time = str(hours) + " hours"
                    timeUnit = "hours"
                    if hours >= 24:
                        days = hours//24
                        hours = hours%24
                        timeUnit = "days"
                        time = str(days) + " days " + str(hours) + " hours"
                    finalmsg = finalmsg + "Contest: " + str(data["result"][-(i+1)]["name"]) + "\n\n"
                await message.channel.send(finalmsg)
        if msgArray[1] == "recent":
            res = requests.get("https://codeforces.com/api/user.status?handle=" + msgArray[2] + "&from=1&count=50")
            data = res.json()
            finalmsg = ""
            cnt = 0
            n = int(msgArray[3])
            for i in range(50):
                if cnt == n:
                    break
                if(data["result"][i]["verdict"] == "OK"):
                    link = ""
                    link = link + "https://codeforces.com/problemset/problem/" + str(data["result"][i]["problem"]["contestId"]) + "/" + str(data["result"][i]["problem"]["index"]) + "/"
                    finalmsg = finalmsg + "Problem: " + str(data["result"][i]["problem"]["contestId"]) + str(data["result"][i]["problem"]["index"]) + " ( Rating: " + str(data["result"][i]["problem"]["rating"]) + ")  " + str(data["result"][i]["problem"]["name"]) + "   " + link + "\n"
                    cnt = cnt + 1
            await message.channel.send(finalmsg)
        if msgArray[1] == "problems":
            # tags = []
            # rating = 0
            # cnt = 0
            # for i in msgArray:
            #     cnt += 1
            #     if cnt < 2:
            #         continue
            #     elif i.isnumeric():
            #         rating = int(i)
            #         break
            #     else:
            #         tags.append(i)
            #  if len(tags) > 0:
            #     if rating>0:
            tags = msgArray[2]
            res = requests.get("https://codeforces.com/api/problemset.problems?tags="+tags)
            finalmsg = ""
            data = res.json()
            for i in range(5):
                link = ""
                link = link + "https://codeforces.com/problemset/problem/" + str(data["result"]["problems"][i]["contestId"]) + "/" + str(data["result"]["problems"][i]["index"]) + "/"
                finalmsg = finalmsg + "Problem: " + str(data["result"]["problems"][i]["contestId"]) + str(data["result"]["problems"][i]["index"]) + " ( Rating: " + str(data["result"]["problems"][i]["rating"]) + ")  " + str(data["result"]["problems"][i]["name"]) + "   " + link + "\n"
            await message.channel.send(finalmsg)



            



bot.run(DISCORD_TOKEN)