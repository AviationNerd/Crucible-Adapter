import requests
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import openai
import asyncio
import os

load_dotenv()
# ANCHOR init
SEASON = os.getenv('SEASON')
ROBOTEVENTS_API_KEY = os.getenv("ROBOTEVENTS_API_KEY")
CGPT_API_KEY = os.getenv("CGPT_API_KEY")
BOT_KEY = os.getenv("BOT_KEY")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
infoJson = {}
loggedMessages = []
endpoint = ""
headers = {"Authorization": ROBOTEVENTS_API_KEY}


# ANCHOR teamevents
@bot.tree.command(name="events")
@app_commands.describe(teamnum="Team Number")
async def pullEvents(interaction: discord.Interaction, teamnum: str):
    title = ""
    id = 0
    endpoint = (
        f"https://www.robotevents.com/api/v2/teams?number%5B%5D={teamnum}&myTeams=false"
    )
    infoJson = requests.get(endpoint, headers=headers).json()
    teamData = infoJson.get("data", [])
    response = ""
    if teamData:
        for team in teamData:
            if team.get("program").get("code") == "VRC" and team.get("registered") == True:
                title = team.get('number')
                id = team.get("id")
                print(id)
                endpoint = f"https://www.robotevents.com/api/v2/teams/{id}/events?season%5B%5D={SEASON}"
                infoJson = requests.get(endpoint, headers=headers).json()
                teamEvents = infoJson.get("data", [])
                response = "**Team " + title + " Events:**\n"
                for event in teamEvents:
                    if event.get("season").get("name") == "VRC 2023-2024: Over Under":
                        eventName = event.get("name")
                        response = response + "* " + eventName + "\n"
                
            else:
                if response == "":
                    response = "Exception: The given team is not part of VRC, or the team is not active"
    else:
        response = "Exception: Given team does not exist"


    await interaction.response.send_message(response)


# ANCHOR teaminfo
@bot.tree.command(name="teaminfo")
@app_commands.describe(teamnumber="Team Number")
async def pullInfo(interaction: discord.Interaction, teamnumber: str):
    endpoint = f"https://www.robotevents.com/api/v2/teams?number%5B%5D={teamnumber}&myTeams=false"
    infoJson = requests.get(endpoint, headers=headers).json()
    teamData = infoJson.get("data", [])
    response = ""
    if teamData:
        for team in teamData:
            if team.get("program").get("code") == "VRC":
                number = team.get("number")
                name = team.get("team_name")
                org = team.get("organization")

                location = team.get("location")
                locationCity = location.get("city", "N/A")
                locationCountry = location.get("country", "N/A")

                programInfo = team.get("program")
                programCode = programInfo.get("code", "N/A")
                grade = team.get("grade")
                roborName = team.get("robot_name")
                activity = team.get("registered")
                response = f"Team Number: {number}\nName: {name}\nOrganization: {org}\nLocation: {locationCity}, {locationCountry}\nProgram: {programCode}, {grade}\nRobot Name: {roborName}\nActive: {activity}\n\n"
            else:
                if response == "":
                    response = "Exception: The given team is not part of VRC"
    else:
        response = "Exception: Given team does not exist"
    print(infoJson)
    await interaction.response.send_message(response)


# ANCHOR start
@bot.event
async def on_ready():
    print("online")
    await bot.user.edit(username="Crucible Adapter")
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("RobotEvents API")
    )
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)


bot.run(BOT_KEY)
