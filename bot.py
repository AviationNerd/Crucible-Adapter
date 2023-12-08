import requests
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import openai
import asyncio

# ANCHOR init
robotEventsApiKey = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMTI2ZjliZGZkMzA0OTllNjNiMDVmOWY5NDk0MzVkOWRkMjEyNDA1ZWI5YmIxNzBkMGY2M2Y1YmVkYzY0ZDA3YzM4Yjc3OGIxNjY1MDgxYTciLCJpYXQiOjE3MDE4MTUyOTIuNzQ1MjE5OSwibmJmIjoxNzAxODE1MjkyLjc0NTIyMywiZXhwIjoyNjQ4NTg2NDkyLjcyNjY4NSwic3ViIjoiMTI0NTA0Iiwic2NvcGVzIjpbXX0.FHAH30QfjvhBr2zvz_I7ipiAb7MyItdQrJDVtaFY69igy6sc96cIv2S1WNP_ORd6ZUnAIcpWG2RoABDmBHyAIzBLP3wkOY4bSqE4oG_FUe4DWfrdyPsYPmktrzKjbI8m4BwbtSthRfjS-MZeXHMdd-kPz2cQnZGmPK9lVqoXdf-_1Q0ers__LDrncxsG7sJIn6HmJ1zNlc8ZICjgpv6NksiPyXNjtChKN8JWvPHTTkmVayfGTc8pwmejsonl-_VNZ0GDK3WR2mcZttl4-kkVJTgiDGOApRa3L5q8u7JdGUrzP9fgB7xxC-GqdwFSuFzcaqVOaNA3dSRuTOFgjFlldfOkk3N5Ud_PsDCzRJ_WQaA_FMOYC3VNdRzvqzuMmSxj0nZn_NloMTL7PLtscSg97r7bPYunOmmdY690fMACPeQIQmReP7Mop2kc-0frf_fGg9ry3OLz2NUAwP2mRBCkuMndwt8DRRjodSLnF0pkCUy0ePPfUs5d4dUEvwmFD1lwBW09psn6BInCxtzMXMDBWW7GluIcI5tuNTRZ-JaQhbQHCVjD2wwFjBRF9AEq8ElyUxJ2t7uCdAh1Cnknj9YBJ5jyJHUiSk6qLO4kNm2rIIijHtyE-yYUow6Wbd2fJTiwHP_1YfTYrJ0KQcTXOiGwKZOgxlEnNoZWAWkLYYO3Ras"
cgptApiKey = "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"
botKey = "MTEwODU2NDI2NTI1MTY0NzUxMg.GqhPbZ.QMb5sdDnTjCU1klZXsG4v6I9lB2VEGAGHQyQiE"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
infoJson = {}
loggedMessages = []
endpoint = ""
headers = {
    "Authorization": robotEventsApiKey
}

# ANCHOR teaminfo
@bot.tree.command(name="teaminfo")
@app_commands.describe(teamnumber="Team Number")
async def pullInfo(interaction:discord.Interaction, teamnumber: str):
    endpoint = f"https://www.robotevents.com/api/v2/teams?number%5B%5D={teamnumber}&myTeams=false"
    infoJson = requests.get(endpoint, headers=headers).json()
    teamData = infoJson.get('data', [])
    response = ''
    if teamData:
        for team in teamData:
                if team.get('program').get('code') == 'VRC':
                    number = team.get('number')
                    name = team.get('team_name')
                    org = team.get('organization')
                    
                    location = team.get('location')
                    locationCity = location.get('city', 'N/A')
                    locationCountry = location.get('country', 'N/A')
                    
                    programInfo = team.get('program')
                    programCode = programInfo.get('code', 'N/A')
                    grade = team.get('grade')
                    roborName = team.get('robot_name')
                    activity = team.get('registered')
                    response = f"Team Number: {number}\nName: {name}\nOrganization: {org}\nLocation: {locationCity}, {locationCountry}\nProgram: {programCode}, {grade}\nRobot Name: {roborName}\nActive: {activity}\n\n"
                else:
                    if response == '':
                        response = "Exception: The given team is not part of VRC"
    else:
        response = "Exception: Given team does not exist"
    print(infoJson)
    await interaction.response.send_message(response)

'''
@bot.tree.command(name="log")
async def log(interaction: discord.Interaction):
    msg = f"Currently logging {len(loggedMessages)} messages from all servers:\n"
    for i in loggedMessages:
        if i.startswith(interaction.guild.name):
            msg = msg + i + "\n"
    await interaction.response.send_message(msg)
'''
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


bot.run(botKey)

