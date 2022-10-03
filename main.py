import discord
import asyncio
import aiohttp
import json
import datetime
import os
import random
import time 
import keep_alive
from discord.enums import ChannelType
from discord.ext import commands, tasks
from discord.http import Route
from random import randint
from itertools import cycle
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from math import ceil

#intents = discord.Intents.default()
#intents.members = True
intents = discord.Intents().all()
client = commands.Bot(command_prefix="$", intents=intents)
client.remove_command("help")
status = cycle(['Made by Gamsa','Welcome Bot', 'Entertainment Bot', 'Music Bot', 'Gambling Bot', 'Support Bot', 'Made by Gamsa'])

client.story = ""
client.storyauthor = ""
client.storyid = ""
client.counter = 0
client.dealer = ['Mike', 'Dan', 'David', 'Max', 'Niko']
client.rulesChannel = 788745311836569611
client.logsChannel = 788754802989334529
client.rolesChannel = 788807038578458664
client.supChannel = 789146917824757760
client.surveyChannel = 789161097646964778
client.memberRole = '|| Member'
client.loginRole = '|| Registration'
client.teamRoles = ['|| Admins','|| TheBot']
client.adminRole = '|| Admins'
client.supRole = '|| Sups'
client.modRole = '|| Mods'
client.settingCat = 788711358957879317
client.queue = {}
client.link = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Casino_Chip.svg/1024px-Casino_Chip.svg.png"

#                       Bot Status
#      Change every 5 seconds
#
@tasks.loop(seconds=5)
async def status_change():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_ready():
    status_change.start()
    print("Logged in as: {}!".format(client.user.name))
    client.queue = {}

#                       New Player
#      Welcome Banner
#      get the Registration Role
  
@client.event
async def on_member_join(ctx):
    server = ctx.guild.id
    await logs(ctx, "Joined the server!")

    if server == 609841305132204032:
        role = discord.utils.get(ctx.guild.roles, name="ㅤㅤㅤㅤㅤㅤRanksㅤㅤㅤㅤㅤㅤㅤ")
        await ctx.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="ㅤㅤㅤㅤㅤㅤAbout meㅤㅤㅤㅤㅤㅤ")
        await ctx.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="ㅤㅤㅤㅤㅤㅤChannelsㅤㅤㅤㅤㅤㅤ")
        await ctx.add_roles(role)
    with open('ids.txt', 'r') as f:
        users = json.load(f)
    
    try:
        role = discord.utils.get(ctx.guild.roles, name=users[str(server)]['loginRole'])
        await ctx.add_roles(role)
    except:
        pass 
    asset = ctx.avatar.with_size(128) 
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((500, 500))
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.Resampling.LANCZOS)
    pfp.putalpha(mask)

    output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    #if output.mode == "RGBA":
    #    output.save(f"{ctx}.png")
    #else:
    #    await logs(ctx, "Joined the server with {output.mode} mode!")
    #    return
         
    background = Image.open('banner.jpg')
    background.paste(pfp, (700, 150), pfp)
    try:
        background.save(f"{ctx}.png")
    except:
        return

    font = ImageFont.truetype("UniSans.otf", 150)
    fontb = ImageFont.truetype("UniSans.otf", 80)
    img = Image.open(f"{ctx}.png")
    draw = ImageDraw.Draw(img)
    text = "WELCOME"
    strip_width, strip_height = 1920, 1000
    text_width, text_height = draw.textsize(text, font)
    position = ((strip_width - text_width) / 2, (strip_height - text_height) / 2 + 220)
    draw.text(position, text, (255, 255, 255), font=font)
    textb = str(ctx)
    text_width, text_height = draw.textsize(textb, fontb)
    positionb = ((strip_width - text_width) / 2, (strip_height - text_height) / 2 + 340)
    draw.text(positionb, textb, (255, 255, 255), font=fontb)
    try:
        img.save(f"{ctx}.png")
    except:
        return
    
    channel = client.get_channel(client.rulesChannel)

    try:
        users[str(server)]['welmsg']
    except:
        users[str(server)]['welmsg'] = 1

        with open('ids.txt', 'w') as f:
            json.dump(users, f)

    if users[str(server)]['welmsg'] == 1:
        await ctx.guild.system_channel.send("{0}, **Welcome to this Discord Server!**\n"
                                            "Before you can find your way around here, please read the rules in {1} first\n"
                                            "You are the **{2}th member. Have fun on our server!**".format(ctx.mention,
                                                                                                           ctx.guild.get_channel(users[str(server)]['ruleChannel']).mention,
                                                             ctx.guild.member_count),
                                            file=discord.File(f"{ctx}.png"))
    elif users[str(server)]['welmsg'] == 2:
        await ctx.guild.system_channel.send("{0}, **Willkommen auf diesem Discord Server!**\n"
                                            "Bevor du dich hier zurechtfindest, lese doch bitte die Regeln in {1} zuerst durch\n"
                                            "Du bist der **{2}. Member. Viel Spaß!**".format(
            ctx.mention,
            ctx.guild.get_channel(users[str(server)]['ruleChannel']).mention,
            ctx.guild.member_count),
            file=discord.File(f"{ctx}.png"))
    elif users[str(server)]['welmsg'] == 3:
        await ctx.guild.system_channel.send("{0}, **Willkommen auf diesem offizielen KSJ RoStu Discord Server!**\n"
                                            "Bevor du dich hier zurechtfindest, lese doch bitte die Infos in {1}\n"
                                            "Du bist der **{2}. Member. Viel Spaß!**".format(
            ctx.mention,
            ctx.guild.get_channel(users[str(server)]['ruleChannel']).mention,
            ctx.guild.member_count),
            file=discord.File(f"{ctx}.png"))

    #os.remove(f"{ctx}.png")

  
@client.command(aliases=['sl'])
async def __sl(ctx, num):
    server = ctx.guild.id
    with open('ids.txt', 'r') as f:
        users = json.load(f)

    users[str(server)]['welmsg'] = num

    with open('ids.txt', 'w') as f:
        json.dump(users, f)


async def emojiExist(ctx, emoji):
    try:
        if not str(emoji) == "undefined":
            return True
    except:
        return False

#                       Settings
#       edit Channels
#       edit Roles
      
@client.command(aliases=['s'])
async def __s(ctx, arg=None):
    server = ctx.guild.id
    with open('ids.txt', 'r') as f:
        users = json.load(f)

    try:
        users[str(server)]
    except:
        users[str(server)] = {}
        users[str(server)]['ruleChannel'] = "undefined"
        users[str(server)]['roleChannel'] = "undefined"
        users[str(server)]['supChannel'] = "undefined"
        users[str(server)]['logsChannel'] = "undefined"
        users[str(server)]['surveyChannel'] = "undefined"
        users[str(server)]['welmsg'] = 1

        with open('ids.txt', 'w') as f:
            json.dump(users, f)

    try:
        users[str(server)]['memberRole']
    except:
        users[str(server)]['memberRole'] = client.memberRole
        users[str(server)]['loginRole'] = client.loginRole
        users[str(server)]['adminRole'] = client.adminRole
        users[str(server)]['supRole'] = client.supRole
        users[str(server)]['modRole'] = client.modRole

        with open('ids.txt', 'w') as f:
            json.dump(users, f)

    try:
        users[str(server)]['oneRole']
    except:
        users[str(server)]['oneRole'] = "undefined"
        users[str(server)]['oneEmoji'] = "undefined"
        users[str(server)]['twoRole'] = "undefined"
        users[str(server)]['twoEmoji'] = "undefined"
        users[str(server)]['threeRole'] = "undefined"
        users[str(server)]['threeEmoji'] = "undefined"
        users[str(server)]['fourRole'] = "undefined"
        users[str(server)]['fourEmoji'] = "undefined"
        users[str(server)]['fiveRole'] = "undefined"
        users[str(server)]['fiveEmoji'] = "undefined"
        users[str(server)]['sixRole'] = "undefined"
        users[str(server)]['sixEmoji'] = "undefined"

        with open('ids.txt', 'w') as f:
            json.dump(users, f)

    def isText(msg):
        try:
            if msg.author == ctx.author:
                return True
        except ValueError:
            return False

    if arg == None:
        embed = discord.Embed(title="Server Settings",
                              description="To edit any of these Settings, type '$s (Channel or Role)'",
                              color=0xff00f6)
        if users[str(server)]['ruleChannel'] == "undefined":
          embed.add_field(name="**Channel: Rules**", value="undefined",
                        inline=True)
        else:
          embed.add_field(name="**Channel: Rules**", value=ctx.guild.get_channel(users[str(server)]['ruleChannel']).mention,
                        inline=True)
        if users[str(server)]['roleChannel'] == "undefined":
          embed.add_field(name="**Channel: Roles**", value="undefined",
                        inline=True)
        else:
          embed.add_field(name="**Channel: Roles**", value=client.get_channel(users[str(server)]['roleChannel']).mention,
                        inline=True)
        if users[str(server)]['supChannel'] == "undefined":
          embed.add_field(name="**Channel: Support**", value="undefined",
                        inline=True)
        else:
          embed.add_field(name="**Channel: Support**", value=client.get_channel(users[str(server)]['supChannel']).mention,
                        inline=True)
        if users[str(server)]['logsChannel'] == "undefined":
          embed.add_field(name="**Channel: Logs**", value="undefined",
                        inline=True)
        else:
          embed.add_field(name="**Channel: Logs**", value=client.get_channel(users[str(server)]['logsChannel']).mention,
                        inline=True)
        if users[str(server)]['surveyChannel'] == "undefined":
          embed.add_field(name="**Channel: Survey**", value="undefined",
                        inline=True)
        else:
          embed.add_field(name="**Channel: Survey**", value=client.get_channel(users[str(server)]['surveyChannel']).mention,
                        inline=True)
        if users[str(server)]['welmsg'] == 1:
          embed.add_field(name="**Welcome Message: wm**", value="English",
                        inline=True)
        else:
          embed.add_field(name="**Welcome Message: wm**", value="German",
                        inline=True)


        rt = await roleExist(ctx, users[str(server)]['memberRole'])
        if rt:
            embed.add_field(name="**Role: Member**",
                            value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['memberRole']).mention,
                            inline=True)
        else:
            embed.add_field(name="**Role: Member**",
                            value="undefined",
                            inline=True)
        rt = await roleExist(ctx, users[str(server)]['loginRole'])
        if rt:
            embed.add_field(name="**Role: Login**",
                            value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['loginRole']).mention,
                            inline=True)
        else:
            embed.add_field(name="**Role: Login**",
                            value="undefined",
                            inline=True)
        rt = await roleExist(ctx, users[str(server)]['adminRole'])
        if rt:
            embed.add_field(name="**Role: Admin**",
                            value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['adminRole']).mention,
                            inline=True)
        else:
            embed.add_field(name="**Role: Admin**",
                            value="undefined",
                            inline=True)
        rt = await roleExist(ctx, users[str(server)]['supRole'])
        if rt:
            embed.add_field(name="**Role: Supporter**",
                            value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['supRole']).mention,
                            inline=True)
        else:
            embed.add_field(name="**Role: Supporter**",
                            value="undefined",
                            inline=True)
        rt = await roleExist(ctx, users[str(server)]['modRole'])
        if rt:
            embed.add_field(name="**Role: Moderator**",
                            value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['modRole']).mention,
                            inline=True)
        else:
            embed.add_field(name="**Role: Moderator**",
                            value="undefined",
                            inline=True)
        rt = await roleExist(ctx, users[str(server)]['oneRole'])
        re = await emojiExist(ctx, users[str(server)]['oneEmoji'])
        if rt:
            if re:
                embed.add_field(name="**Selfrole: one**",
                                value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['oneRole']).mention + " → " + str(users[str(server)]['oneEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: one**",
                                value=discord.utils.get(ctx.guild.roles, name=users[str(server)]['oneRole']).mention + " → undefined",
                                inline=True)
        else:
            if re:
                embed.add_field(name="**Selfrole: one**",
                                value="undefined → " + str(users[str(server)]['oneEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: one**",
                                value="undefined → undefined",
                                inline=True)
        rt = await roleExist(ctx, users[str(server)]['twoRole'])
        re = await emojiExist(ctx, users[str(server)]['twoEmoji'])
        if rt:
            if re:
                embed.add_field(name="**Selfrole: two**",
                                value=discord.utils.get(ctx.guild.roles,
                                                        name=users[str(server)]['twoRole']).mention + " → " + str(
                                    users[str(server)]['twoEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: two**",
                                value=discord.utils.get(ctx.guild.roles,
                                                        name=users[str(server)]['twoRole']).mention + " → undefined",
                                inline=True)
        else:
            if re:
                embed.add_field(name="**Selfrole: two**",
                                value="undefined → " + str(users[str(server)]['twoEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: two**",
                                value="undefined → undefined",
                                inline=True)
        rt = await roleExist(ctx, users[str(server)]['threeRole'])
        re = await emojiExist(ctx, users[str(server)]['threeEmoji'])
        if rt:
            if re:
                embed.add_field(name="**Selfrole: three**",
                                value=discord.utils.get(ctx.guild.roles,
                                                        name=users[str(server)]['threeRole']).mention + " → " + str(
                                    users[str(server)]['threeEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: three**",
                                value=discord.utils.get(ctx.guild.roles,
                                                        name=users[str(server)]['threeRole']).mention + " → undefined",
                                inline=True)
        else:
            if re:
                embed.add_field(name="**Selfrole: three**",
                                value="undefined → " + str(users[str(server)]['threeEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: three**",
                                value="undefined → undefined",
                                inline=True)
        rt = await roleExist(ctx, users[str(server)]['fourRole'])
        re = await emojiExist(ctx, users[str(server)]['fourEmoji'])
        if rt:
            if re:
                embed.add_field(name="**Selfrole: four**",
                                value=discord.utils.get(ctx.guild.roles,
                                                        name=users[str(server)]['fourRole']).mention + " → " + str(
                                    users[str(server)]['fourEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: four**",
                                value=discord.utils.get(ctx.guild.roles,
                                                        name=users[str(server)]['fourRole']).mention + " → undefined",
                                inline=True)
        else:
            if re:
                embed.add_field(name="**Selfrole: four**",
                                value="undefined → " + str(users[str(server)]['fourEmoji']),
                                inline=True)
            else:
                embed.add_field(name="**Selfrole: four**",
                                value="undefined → undefined",
                                inline=True)
        rr = await ctx.send(embed=embed)
    elif arg.lower() == 'wm':
        embed = discord.Embed(title="Edit Language:",
                              description="Type 1 for English or 2 for German",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['welmsg'] = int(res)
    elif arg.lower() == 'rules':
        embed = discord.Embed(title="Edit Channel: Rules",
                              description="Type new Channel ID!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['ruleChannel'] = int(res)
    elif arg.lower() == 'roles':
        embed = discord.Embed(title="Edit Channel: Roles",
                              description="Type new Channel ID!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['roleChannel'] = int(res)
    elif arg.lower() == 'support':
        embed = discord.Embed(title="Edit Channel: Support",
                              description="Type new Channel ID!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['supChannel'] = int(res)
    elif arg.lower() == 'logs':
        embed = discord.Embed(title="Edit Channel: Logs",
                              description="Type new Channel ID!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['logsChannel'] = int(res)
    elif arg.lower() == 'survey':
        embed = discord.Embed(title="Edit Channel: Survey",
                              description="Type new Channel ID!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['surveyChannel'] = int(res)
    elif arg.lower() == 'supporter':
        embed = discord.Embed(title="Edit Role: Supporter",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['supRole'] = str(res)
    elif arg.lower() == 'admin':
        embed = discord.Embed(title="Edit Role: Admin",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['adminRole'] = str(res)
    elif arg.lower() == 'moderator':
        embed = discord.Embed(title="Edit Role: Moderator",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['modRole'] = str(res)
    elif arg.lower() == 'member':
        embed = discord.Embed(title="Edit Role: Member",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['memberRole'] = str(res)
    elif arg.lower() == 'login':
        embed = discord.Embed(title="Edit Role: Login",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['loginRole'] = str(res)

    elif arg.lower() == 'one':
        embed = discord.Embed(title="Edit Selfrole: one",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['oneRole'] = str(res)
        embed = discord.Embed(title="Edit Selfrole: one",
                              description="Type the new Emoji!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['oneEmoji'] = str(res)

    elif arg.lower() == 'two':
        embed = discord.Embed(title="Edit Selfrole: two",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['twoRole'] = str(res)
        embed = discord.Embed(title="Edit Selfrole: two",
                              description="Type the new Emoji!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['twoEmoji'] = str(res)

    elif arg.lower() == 'three':
        embed = discord.Embed(title="Edit Selfrole: three",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['threeRole'] = str(res)
        embed = discord.Embed(title="Edit Selfrole: three",
                              description="Type the new Emoji!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['threeEmoji'] = str(res)

    elif arg.lower() == 'four':
        embed = discord.Embed(title="Edit Selfrole: four",
                              description="Type the exact new Rolename!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['fourRole'] = str(res)
        embed = discord.Embed(title="Edit Selfrole: four",
                              description="Type the new Emoji!",
                              color=0xff00f6)
        rr = await ctx.send(embed=embed)

        response = await client.wait_for('message', timeout=30.0, check=isText)
        res = response.content
        await response.delete()
        await rr.delete()
        users[str(server)]['fourEmoji'] = str(res)

    with open('ids.txt', 'w') as f:
        json.dump(users, f)


@client.command(aliases=['su'])
async def __su(channel, arg=None):
    embed = discord.Embed(title="Create Survey",
                          description="Type your Question",
                          color=0xff00f6)
    rr = await channel.send(embed=embed)

    def isText(msg):
        try:
            str(msg.content)
            if msg.author == channel.author:
                return True
        except ValueError:
            return False

    response = await client.wait_for('message', timeout=30.0, check=isText)
    res = response.content
    await response.delete()
    await rr.delete()
    embed = discord.Embed(title="**Survey from: {0}**".format(channel.author.name),
                          description=res,
                          color=0xff00f6)
    rr = await channel.send(embed=embed)
    await rr.add_reaction('✅')
    await rr.add_reaction('❌')
    await logs(channel.author, "Created a survey!")

#                       Roles
#      accept the rules to get the Member Role
#      add Reaction to get Role
#      remove Reaction to remove Role
#      add Reaction to create Support Ticket
  
@client.event
async def on_raw_reaction_add(reaction):
    user = reaction.member
    if not user.bot:

        server = user.guild.id
        with open('ids.txt', 'r') as f:
            users = json.load(f)
        channel = client.get_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)

        if (reaction.channel_id == users[str(server)]['ruleChannel']):
            if str(reaction.emoji) == '✅':
                memberRole = discord.utils.get(message.guild.roles, name=users[str(server)]['memberRole'])
                loginRole = discord.utils.get(message.guild.roles, name=users[str(server)]['loginRole'])
                await user.add_roles(memberRole)
                await user.remove_roles(loginRole)
                await logs(user, "Has accepted the rules!")
                return

        elif reaction.channel_id == users[str(server)]['supChannel']:
            if str(reaction.emoji) == '✉️':
                
                await message.remove_reaction(reaction.emoji, user)

                guild = user.guild
                rolesearch = discord.utils.get(guild.roles, name="Leckere Sups")
                rolesearch2 = discord.utils.get(guild.roles, name="Süße Mods")
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    user: discord.PermissionOverwrite(read_messages=True),
                    rolesearch: discord.PermissionOverwrite(read_messages=True),
                    rolesearch2: discord.PermissionOverwrite(read_messages=True)
                }
                category = discord.utils.get(guild.categories, id=610113831682834443)
                sup = await guild.create_text_channel(str(user) + ' Support_Ticket', overwrites=overwrites,
                                                     category=category)

                embed = discord.Embed(title="Beschreibe dein Anliegen so detailiert wie möglich!",
                                      description="Wir antworten so schnell wie es geht",
                                      color=0xff00f6)
                await sup.send(embed=embed)
                await logs(user, "Created a support ticket!")
                return

        elif reaction.channel_id == users[str(server)]['surveyChannel']:
            if str(reaction.emoji) == '❓':
                embed = discord.Embed(title="Create Survey",
                                      description="Type your Question",
                                      color=0xff00f6)
                rr = await channel.send(embed=embed)

                await message.remove_reaction(reaction.emoji, user)

                def isText(msg):
                    try:
                        str(msg.content)
                        if msg.author == user:
                            return True
                    except ValueError:
                        return False

                response = await client.wait_for('message', timeout=30.0, check=isText)
                res = response.content
                await response.delete()
                await rr.delete()
                embed = discord.Embed(title="**Survey from: {0}**".format(user.name),
                                      description=res,
                                      color=0xff00f6)
                rr = await channel.send(embed=embed)
                await rr.add_reaction('✅')
                await rr.add_reaction('❌')
                await logs(user, "Created a survey!")
        elif reaction.channel_id == users["908500273369063434"]['roleChannel']:
            if str(reaction.emoji) == '👨‍🦰':
                role = discord.utils.get(message.guild.roles, name="Männlich")
            elif str(reaction.emoji) == '👩‍🦰':
                role = discord.utils.get(message.guild.roles, name="Weiblich")
            elif str(reaction.emoji) == '👤':
                role = discord.utils.get(message.guild.roles, name="Divers")
            elif str(reaction.emoji) == '🦄':
                role = discord.utils.get(message.guild.roles, name="12-14")
            elif str(reaction.emoji) == '🐭':
                role = discord.utils.get(message.guild.roles, name="15-17")
            elif str(reaction.emoji) == '🐻':
                role = discord.utils.get(message.guild.roles, name="18+")
            elif str(reaction.emoji) == '🧍‍♂️':
                role = discord.utils.get(message.guild.roles, name="Single")
            elif str(reaction.emoji) == '🧑‍🤝‍🧑':
                role = discord.utils.get(message.guild.roles, name="Vergeben")
            elif str(reaction.emoji) == '🔵':
                role = discord.utils.get(message.guild.roles, name="Blau")
            elif str(reaction.emoji) == '🟡':
                role = discord.utils.get(message.guild.roles, name="Yellow")
            elif str(reaction.emoji) == '🟠':
                role = discord.utils.get(message.guild.roles, name="Orange")
            elif str(reaction.emoji) == '👛':
                role = discord.utils.get(message.guild.roles, name="Pink")
            elif str(reaction.emoji) == '🟢':
                role = discord.utils.get(message.guild.roles, name="Green")
            elif str(reaction.emoji) == '🟣':
                role = discord.utils.get(message.guild.roles, name="Purple")
            elif str(reaction.emoji) == '🔴':
                role = discord.utils.get(message.guild.roles, name="Red")
            try:
                await user.add_roles(role)
            except:
                return
            await logs(user, "Add the Role " + role.mention + "!")
            return
        elif reaction.channel_id == users[str(server)]['roleChannel']:
            if str(reaction.emoji) == '👨‍🦰':
                role = discord.utils.get(message.guild.roles, name="boy")
            elif str(reaction.emoji) == '👩‍🦰':
                role = discord.utils.get(message.guild.roles, name="girl")
            elif str(reaction.emoji) == '👤':
                role = discord.utils.get(message.guild.roles, name="divers")
            elif str(reaction.emoji) == '🦄':
                role = discord.utils.get(message.guild.roles, name="U12")
            elif str(reaction.emoji) == '🐭':
                role = discord.utils.get(message.guild.roles, name="U16")
            elif str(reaction.emoji) == '🦕':
                role = discord.utils.get(message.guild.roles, name="Ü16")
            elif str(reaction.emoji) == '🐻':
                role = discord.utils.get(message.guild.roles, name="Ü18")
            elif str(reaction.emoji) == '🐢':
                role = discord.utils.get(message.guild.roles, name="Ü20")
            elif str(reaction.emoji) == '🌳':
                role = discord.utils.get(message.guild.roles, name="Lollibaum")
            elif str(reaction.emoji) == '✉️':
                role = discord.utils.get(message.guild.roles, name="Ping")
            elif str(reaction.emoji) == '🤩':
                role = discord.utils.get(message.guild.roles, name="Netter Junge! :)")
            elif str(reaction.emoji) == str(users[str(server)]['oneEmoji']):
                role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['oneRole']))
            elif str(reaction.emoji) == str(users[str(server)]['twoEmoji']):
                role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['twoRole']))
            elif str(reaction.emoji) == str(users[str(server)]['threeEmoji']):
                role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['threeRole']))
            elif str(reaction.emoji) == str(users[str(server)]['fourEmoji']):
                role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['fourRole']))
            elif str(reaction.emoji) == '🌍':
                role = discord.utils.get(message.guild.roles, name="|| Minecraft")
            elif str(reaction.emoji) == '🔫':
                role = discord.utils.get(message.guild.roles, name="|| CS:GO")
            elif str(reaction.emoji) == '🦸':
                role = discord.utils.get(message.guild.roles, name="|| Overwatch")
            elif str(reaction.emoji) == '⚠':
                role = discord.utils.get(message.guild.roles, name="|| COD")
            elif str(reaction.emoji) == '🎃':
                role = discord.utils.get(message.guild.roles, name="|| League of Legends")
            elif str(reaction.emoji) == '🚔':
                role = discord.utils.get(message.guild.roles, name="|| GTA")
            elif str(reaction.emoji) == '<:2000pxJavaLogo:788895383303487518>':
                role = discord.utils.get(message.guild.roles, name="|| Java")
            elif str(reaction.emoji) == '<:python:788894989420986378>':
                role = discord.utils.get(message.guild.roles, name="|| Python")
            elif str(reaction.emoji) == '<:C_:788895128253104168>':
                role = discord.utils.get(message.guild.roles, name="|| C++")
            elif str(reaction.emoji) == '<:C_:788895222645129256>':
                role = discord.utils.get(message.guild.roles, name="|| C#")
            elif str(reaction.emoji) == '<:nodejsjavascriptwebapplicationex:788895806232985621>':
                role = discord.utils.get(message.guild.roles, name="|| NodeJs")
            elif str(reaction.emoji) == '<:CSGO:888488169086017626>':
                role = discord.utils.get(message.guild.roles, name="CS:GO")
            elif str(reaction.emoji) == '<:LoL:888488077281087599>':
                role = discord.utils.get(message.guild.roles, name="LoL")
            elif str(reaction.emoji) == '<:R6s:888487392439320656>':
                role = discord.utils.get(message.guild.roles, name="R6s")
            elif str(reaction.emoji) == '<:RL:888488645756063754>':
                role = discord.utils.get(message.guild.roles, name="RL")
            elif str(reaction.emoji) == '<:Val:888488987235348530>':
                role = discord.utils.get(message.guild.roles, name="Val")
            elif str(reaction.emoji) == '<:OwlTournament:888487158799798274>':
                role = discord.utils.get(message.guild.roles, name="OwlTournament")

            try:
                await user.add_roles(role)
            except:
                return
            await logs(user, "Add the Role " + role.mention + "!")
            return

@client.event

async def on_raw_reaction_remove(reaction):

    guild = client.get_guild(reaction.guild_id)
    user = guild.get_member(reaction.user_id)
    channel = client.get_channel(reaction.channel_id)
    message = await channel.fetch_message(reaction.message_id)

    server = user.guild.id
    with open('ids.txt', 'r') as f:
        users = json.load(f)
    if reaction.channel_id == users["908500273369063434"]['roleChannel']:
            if str(reaction.emoji) == '👨‍🦰':
                role = discord.utils.get(message.guild.roles, name="Männlich")
            elif str(reaction.emoji) == '👩‍🦰':
                role = discord.utils.get(message.guild.roles, name="Weiblich")
            elif str(reaction.emoji) == '👤':
                role = discord.utils.get(message.guild.roles, name="Divers")
            elif str(reaction.emoji) == '🦄':
                role = discord.utils.get(message.guild.roles, name="12-14")
            elif str(reaction.emoji) == '🐭':
                role = discord.utils.get(message.guild.roles, name="15-17")
            elif str(reaction.emoji) == '🐻':
                role = discord.utils.get(message.guild.roles, name="18+")
            elif str(reaction.emoji) == '🧍‍♂️':
                role = discord.utils.get(message.guild.roles, name="Single")
            elif str(reaction.emoji) == '🧑‍🤝‍🧑':
                role = discord.utils.get(message.guild.roles, name="Vergeben")
            elif str(reaction.emoji) == '🔵':
                role = discord.utils.get(message.guild.roles, name="Blau")
            elif str(reaction.emoji) == '🟡':
                role = discord.utils.get(message.guild.roles, name="Yellow")
            elif str(reaction.emoji) == '🟠':
                role = discord.utils.get(message.guild.roles, name="Orange")
            elif str(reaction.emoji) == '👛':
                role = discord.utils.get(message.guild.roles, name="Pink")
            elif str(reaction.emoji) == '🟢':
                role = discord.utils.get(message.guild.roles, name="Green")
            elif str(reaction.emoji) == '🟣':
                role = discord.utils.get(message.guild.roles, name="Purple")
            elif str(reaction.emoji) == '🔴':
                role = discord.utils.get(message.guild.roles, name="Red")
            try:
                await user.remove_roles(role)
            except:
                return
            await logs(user, "Remove the Role " + role.mention + "!")
            return  
    elif reaction.channel_id == users[str(server)]['roleChannel']:
        if str(reaction.emoji) == '👨‍🦰':
            role = discord.utils.get(message.guild.roles, name="boy")
        elif str(reaction.emoji) == '👩‍🦰':
            role = discord.utils.get(message.guild.roles, name="girl")
        elif str(reaction.emoji) == '👤':
            role = discord.utils.get(message.guild.roles, name="divers")
        elif str(reaction.emoji) == '🦄':
            role = discord.utils.get(message.guild.roles, name="U12")
        elif str(reaction.emoji) == '🐭':
            role = discord.utils.get(message.guild.roles, name="U16")
        elif str(reaction.emoji) == '🦕':
            role = discord.utils.get(message.guild.roles, name="Ü16")
        elif str(reaction.emoji) == '🐻':
            role = discord.utils.get(message.guild.roles, name="Ü18")
        elif str(reaction.emoji) == '🐢':
            role = discord.utils.get(message.guild.roles, name="Ü20")
        elif str(reaction.emoji) == '🌳':
            role = discord.utils.get(message.guild.roles, name="Lollibaum")
        elif str(reaction.emoji) == '✉️':
                role = discord.utils.get(message.guild.roles, name="Ping")
        elif str(reaction.emoji) == '🤩':
            role = discord.utils.get(message.guild.roles, name="Netter Junge! :)")
            role = discord.utils.get(message.guild.roles, name="|| Minecraft")
        elif str(reaction.emoji) == str(users[str(server)]['oneEmoji']):
            role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['oneRole']))
        elif str(reaction.emoji) == str(users[str(server)]['twoEmoji']):
            role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['twoRole']))
        elif str(reaction.emoji) == str(users[str(server)]['threeEmoji']):
            role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['threeRole']))
        elif str(reaction.emoji) == str(users[str(server)]['fourEmoji']):
            role = discord.utils.get(message.guild.roles, name=str(users[str(server)]['fourRole']))
        elif str(reaction.emoji) == '🔫':
            role = discord.utils.get(message.guild.roles, name="|| CS:GO")
        elif str(reaction.emoji) == '🦸':
            role = discord.utils.get(message.guild.roles, name="|| Overwatch")
        elif str(reaction.emoji) == '⚠':
            role = discord.utils.get(message.guild.roles, name="|| COD")
        elif str(reaction.emoji) == '🎃':
            role = discord.utils.get(message.guild.roles, name="|| League of Legends")
        elif str(reaction.emoji) == '🚔':
            role = discord.utils.get(message.guild.roles, name="|| GTA")
        elif str(reaction.emoji) == '<:2000pxJavaLogo:788895383303487518>':
            role = discord.utils.get(message.guild.roles, name="|| Java")
        elif str(reaction.emoji) == '<:python:788894989420986378>':
            role = discord.utils.get(message.guild.roles, name="|| Python")
        elif str(reaction.emoji) == '<:C_:788895128253104168>':
            role = discord.utils.get(message.guild.roles, name="|| C++")
        elif str(reaction.emoji) == '<:C_:788895222645129256>':
            role = discord.utils.get(message.guild.roles, name="|| C#")
        elif str(reaction.emoji) == '<:nodejsjavascriptwebapplicationex:788895806232985621>':
            role = discord.utils.get(message.guild.roles, name="|| NodeJs")
        elif str(reaction.emoji) == '<:CSGO:888488169086017626>':
            role = discord.utils.get(message.guild.roles, name="CS:GO")
        elif str(reaction.emoji) == '<:LoL:888488077281087599>':
            role = discord.utils.get(message.guild.roles, name="LoL")
        elif str(reaction.emoji) == '<:R6s:888487392439320656>':
            role = discord.utils.get(message.guild.roles, name="R6s")
        elif str(reaction.emoji) == '<:RL:888488645756063754>':
            role = discord.utils.get(message.guild.roles, name="RL")
        elif str(reaction.emoji) == '<:Val:888488987235348530>':
            role = discord.utils.get(message.guild.roles, name="Val")
        elif str(reaction.emoji) == '<:OwlTournament:888487158799798274>':
            role = discord.utils.get(message.guild.roles, name="OwlTournament")

        try:
            await user.remove_roles(role)
        except:
            return
        await logs(user, "Remove the Role " + role.mention + "!")
        return  

#
#                       Send Embeds
#       send specific embeds with the token
      
@client.command(aliases=['send'])
async def __send(ctx, arg=None):
    isInTeam = await isTeam(ctx)
    if isInTeam:
        if arg==None:
            embed = discord.Embed(title="Missing Argument!",
                                  description="$send (token)",
                                  color=0xff00f6)
            await ctx.send(embed=embed)
        if arg=="rr":
            embed = discord.Embed(title="Roles:",
                                  description="To get one of these ranks, leave expected reaction below",
                                  color=0xff00f6)
            embed.add_field(name="**Choose your gender**",
                            value="👨‍🦰 → {0}\n" 
                                  "👩‍🦰‍️ → {1}\n"
                                  "👤 → {2}\n".format(discord.utils.get(ctx.guild.roles, name="|| Male").mention,
                                                       discord.utils.get(ctx.guild.roles, name="|| Female").mention,
                                                       discord.utils.get(ctx.guild.roles, name="|| Divers").mention), inline=False)
            embed.add_field(name="**Choose which games you play**",
                            value="🌍 → {0}\n" 
                                  "🔫 → {1}\n" 
                                  "🦸 → {2}\n" 
                                  "⚠️ → {3}\n" 
                                  "🎃 → {4}\n"
                                  "🚔 → {5}\n".format(discord.utils.get(ctx.guild.roles, name="|| Minecraft").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| CS:GO").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| Overwatch").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| COD").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| League of Legends").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| GTA").mention), inline=False)
            embed.add_field(name="**Choose in which language you program**",
                            value="<:2000pxJavaLogo:788895383303487518> → {0}\n"
                                  "<:python:788894989420986378> → {1}\n"
                                  "<:C_:788895128253104168> → {2}\n"
                                  "<:C_:788895222645129256> → {3}\n"
                                  "<:nodejsjavascriptwebapplicationex:788895806232985621> → {4}\n".format(discord.utils.get(ctx.guild.roles, name="|| Java").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| Python").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| C++").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| C#").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| NodeJs").mention), inline=False)
            rr = await ctx.send(embed=embed)

            emojiList = ['👨‍🦰','👩‍🦰','👤','🌍','🔫','🦸','⚠','🎃','🚔','<:2000pxJavaLogo:788895383303487518>',
                         '<:python:788894989420986378>','<:C_:788895128253104168>','<:C_:788895222645129256>',
                         '<:nodejsjavascriptwebapplicationex:788895806232985621>']
            for emoji in emojiList:
                try:
                    await rr.add_reaction(emoji)
                except:
                    pass
        elif arg=="lc":
            embed = discord.Embed(title="Roles:",
                                  description="Um einer der Rollen zu erhalten, das entsprechende Emoji anklicken",
                                  color=0xff00f6)
            embed.add_field(name="**Wähle dein Geschlecht**",
                            value="👨‍🦰 → {0}\n" 
                                  "👩‍🦰‍️ → {1}\n"
                                  "👤 → {2}\n".format(discord.utils.get(ctx.guild.roles, name="boy").mention,
                                                       discord.utils.get(ctx.guild.roles, name="girl").mention,
                                                       discord.utils.get(ctx.guild.roles, name="divers").mention), inline=False)
            embed.add_field(name="**Wähle deine Alter**",
                            value="🦄 → {0}\n" 
                                  "🐭 → {1}\n" 
                                  "🦕 → {2}\n" 
                                  "🐻 → {3}\n"
                                  "🐢 → {4}\n".format(discord.utils.get(ctx.guild.roles, name="U12").mention,
                                                        discord.utils.get(ctx.guild.roles, name="U16").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Ü16").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Ü18").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Ü20").mention), inline=False)
            embed.add_field(name="**Extra Ränge?**",
                            value="🌳 → {0}\n"
                                  "🤩 → {1}\n"
                                  "✉️ → {2}\n".format(discord.utils.get(ctx.guild.roles, name="Lollibaum").mention,
                                                      discord.utils.get(ctx.guild.roles, name="Netter Junge! :)").mention,
                                                      discord.utils.get(ctx.guild.roles, name="Ping").mention), inline=False)
            rr = await ctx.send(embed=embed)

            emojiList = ['👨‍🦰','👩‍🦰','👤','🦄','🐭','🦕','🐻','🐢','🌳','🤩','✉️']
            for emoji in emojiList:
                try:
                    await rr.add_reaction(emoji)
                except:
                    pass
        elif arg=="sd":
            embed = discord.Embed(title="Roles:",
                                  description="Um einer der Rollen zu erhalten, das entsprechende Emoji anklicken",
                                  color=0xff00f6)
            embed.add_field(name="**Wähle dein Geschlecht**",
                            value="👨‍🦰 → {0}\n" 
                                  "👩‍🦰‍️ → {1}\n"
                                  "👤 → {2}\n".format(discord.utils.get(ctx.guild.roles, name="Männlich").mention,
                                                       discord.utils.get(ctx.guild.roles, name="Weiblich").mention,
                                                       discord.utils.get(ctx.guild.roles, name="Divers").mention), inline=False)
            embed.add_field(name="**Wähle deine Alter**",
                            value="🦄 → {0}\n" 
                                  "🐭 → {1}\n" 
                                  "🐻 → {2}\n".format(discord.utils.get(ctx.guild.roles, name="12-14").mention,
                                                        discord.utils.get(ctx.guild.roles, name="15-17").mention,
                                                        discord.utils.get(ctx.guild.roles, name="18+").mention), inline=False)
            embed.add_field(name="**Wähle dein Beziehungsstatus**",
                            value="🧍‍♂️ → {0}\n"
                                  "🧑‍🤝‍🧑 → {1}\n".format(discord.utils.get(ctx.guild.roles, name="Single").mention,
                                                      discord.utils.get(ctx.guild.roles, name="Vergeben").mention), inline=False)
            embed.add_field(name="**Wähle deine Farbe**",
                            value="🔵 → {0}\n" 
                                  "🟡 → {1}\n" 
                                  "🟠 → {2}\n" 
                                  "👛 → {3}\n"
                                  "🟢 → {4}\n"
                                  "🟣 → {5}\n"
                                  "🔴 → {6}\n".format(discord.utils.get(ctx.guild.roles, name="Blue").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Yellow").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Orange").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Pink").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Green").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Purple").mention,
                                                        discord.utils.get(ctx.guild.roles, name="Red").mention), inline=False)
            rr = await ctx.send(embed=embed)

            emojiList = ['👨‍🦰','👩‍🦰','👤','🦄','🐭','🦕','🐻','🧍‍♂️','🧑‍🤝‍🧑','🔵','🟡','🟠','👛','🟢','🟣','🔴']
            for emoji in emojiList:
                try:
                    await rr.add_reaction(emoji)
                except:
                    pass
        elif arg=="ll":
            embed = discord.Embed(title="Roles:",
                                  description="To get one of these ranks, leave expected reaction below",
                                  color=0xff00f6)
            embed.add_field(name="**Choose your gender**",
                            value="👨‍🦰 → {0}\n" 
                                  "👩‍🦰‍️ → {1}\n"
                                  "👤 → {2}\n".format(discord.utils.get(ctx.guild.roles, name="|| Male").mention,
                                                       discord.utils.get(ctx.guild.roles, name="|| Female").mention,
                                                       discord.utils.get(ctx.guild.roles, name="|| Divers").mention), inline=False)
            embed.add_field(name="**Choose youre role**",
                            value="🏃‍♀️→ {0}\n" 
                                  "🪖→ {1}\n".format(discord.utils.get(ctx.guild.roles, name="|| Mannschaft").mention,
                                                        discord.utils.get(ctx.guild.roles, name="|| Trainer").mention), inline=False)
            rr = await ctx.send(embed=embed)

            emojiList = ['👨‍🦰','👩‍🦰','👤','🏃‍♀️','🪖']
            for emoji in emojiList:
                try:
                    await rr.add_reaction(emoji)
                except:
                    pass
        elif arg=="ss":
            embed = discord.Embed(title="Support Ticket", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="To create a support ticket, respond to this message with ✉!")
            embed.add_field(name="**- How does the ticket system work?**",
                            value="After you have submitted a response, "
                                  "creates a text channel for you \n"
                                  "in which you can describe your problem, "
                                  "where a supporter will assist you as soon as possible.", inline=False)
            embed.add_field(name="**- When may/can I create a ticket?**",
                            value="In the following cases, you are welcome to "
                                  "Create a ticket: Server questions, "
                                  "Bug reports, player reports or "
                                  "other concerns you have.", inline=False)
            embed.add_field(name="**- How long does it take for a ticket to be processed?**",
                            value="This may vary from case to case "
                                  "Please be patient, the "
                                  "Supporters will not keep you waiting unnecessarily. ")
            embed.add_field(name="**- Also:**", value="- Abuse will be punished!", inline=False)
            embed.add_field(name="**- Opening hours:**",
                            value="Between 10 - 24 o'clock our supporters are normally there for you", inline=False)

            rr = await ctx.send(embed=embed)

            await rr.add_reaction('✉')
        elif arg=="dl":
            embed = discord.Embed(title="DL Anfrage", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="Um eine Frage zustellen, mit ✉ auf diese Nachricht reagieren!")
            embed.add_field(name="**- Wie funktioniert das System?**",
                            value="Nach dem du auf den ✉ klickst, "
                                  "wird ein Textkanal mit dir und der DL erstellt \n"
                                  "Hier kannst du dann deine Frage genauer erläutern! ", inline=False)
            embed.add_field(name="**- Opening hours:**",
                            value="Die DL versucht so schnell wie möglich zu antworten!", inline=False)

            rr = await ctx.send(embed=embed)

            await rr.add_reaction('✉')
        elif arg=="vv":
            embed = discord.Embed(title="Create Surveys", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="To create a Survey, respond to this message with ❓ !")

            rr = await ctx.send(embed=embed)

            await rr.add_reaction('❓')

    else:
        embed = discord.Embed(title="Permission Denied.",
                              description="You do not have the necessary permission for this command!",
                              color=0xff00f6)
        await ctx.send(embed=embed)
    await ctx.message.delete()


async def roleExist(ctx, role):
    try:
        if not discord.utils.get(ctx.guild.roles, name=role) == None:
            return True
    except:
        return False


async def isTeam(ctx):
    server = ctx.guild.id
    with open('ids.txt', 'r') as f:
        users = json.load(f)

    for role in client.teamRoles:
        role = discord.utils.get(ctx.guild.roles, name=users[str(server)]['adminRole'])
        if role in ctx.author.roles:
            return True
        role = discord.utils.get(ctx.guild.roles, name=users[str(server)]['modRole'])
        if role in ctx.author.roles:
            return True
        role = discord.utils.get(ctx.guild.roles, name=users[str(server)]['supRole'])
        if role in ctx.author.roles:
            return True
    return False

#                       Player Logs System
#      get new Logs
#      edit Log List in Channel
  
async def logs(user, action):
    server = user.guild.id

    with open('ids.txt', 'r') as f:
        users = json.load(f)

    if not str(user) in users[str(server)]:
        users[str(server)][str(user)] = {}
        users[str(server)][str(user)]['log'] = "[" + str(datetime.datetime.now()) + "] " + (str(action))

        embed = discord.Embed(title="Logs of: " + str(user),
                              description=str(action),
                              color=0xff00f6)
        channel = client.get_channel(users[str(server)]['logsChannel'])

        to_send = await channel.send(embed=embed)
        users[str(server)][str(user)]['msgid'] = str(to_send.id) + "!"
    else:
        users[str(server)][str(user)]['log'] = users[str(server)][str(user)]['log'] + "[" + str(datetime.datetime.now()) + "] " + str(action)

    logs = users[str(server)][str(user)]['log'].split("!")
    logmsg = ""
    for enum in logs:
        logmsg = logmsg + "\n" + enum

    channel = client.get_channel(users[str(server)]['logsChannel'])

    for i in range(ceil(len(logmsg) / 2048.0)):
        part = logmsg[i * 2048:min((i + 1) * 2048, len(logmsg))]
        embed = discord.Embed(title="Update of: " + str(user),
                            description=part,
                            color=0xff00f6)

        msg = users[str(server)][str(user)]['msgid'].split("!")
        if i > 0:
            if len(msg) < i + 2:
                to_send = await channel.send(embed=embed)
                users[str(server)][str(user)]['msgid'] = users[str(server)][str(user)]['msgid'] + str(to_send.id) + "!"

        msg = users[str(server)][str(user)]['msgid'].split("!")
        message = await channel.fetch_message(msg[i])
        await message.edit(embed=embed)

        with open('ids.txt', 'w') as f:
            json.dump(users, f)


@client.command(aliases=['youtuber'])
async def __yt(ctx):
    if ctx.channel.id == 610115371130945545:
        user = ctx.author
        guild = ctx.guild
        rolesearch = discord.utils.get(guild.roles,name="Leckere Sups")
        rolesearch2 = discord.utils.get(guild.roles,name="Süße Mods")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            rolesearch: discord.PermissionOverwrite(read_messages=True),
            rolesearch2: discord.PermissionOverwrite(read_messages=True)
        }
        hi = await guild.create_text_channel(str(user) + ' Youtuber-Rang Antrag', overwrites=overwrites)
        await ctx.message.delete()
        await hi.send("Senden sie die zuvor aufgeführten Referenzen in diesen Channel. Ein Supporter wird sich schon bald um sie kümmern")


@client.command(aliases=['streamer'])
async def __st(ctx):
    if ctx.channel.id == 610115371130945545:
        user = ctx.author
        guild = ctx.guild
        rolesearch = discord.utils.get(guild.roles, name="Leckere Sups")
        rolesearch2 = discord.utils.get(guild.roles, name="Süße Mods")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            rolesearch: discord.PermissionOverwrite(read_messages=True),
            rolesearch2: discord.PermissionOverwrite(read_messages=True)
        }
        hi = await guild.create_text_channel(str(user) + ' Streamer-Rang Antrag', overwrites=overwrites)
        await ctx.message.delete()
        await hi.send("Senden sie die zuvor aufgeführten Referenzen in diesen Channel. Ein Supporter wird sich schon bald um sie kümmern")


@client.command(aliases=['supporter'])
async def __sup(ctx):
    if ctx.channel.id == 610115371130945545:
        user = ctx.author
        guild = ctx.guild
        rolesearch = discord.utils.get(guild.roles, name="Leckere Sups")
        rolesearch2 = discord.utils.get(guild.roles, name="Süße Mods")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            rolesearch: discord.PermissionOverwrite(read_messages=True),
            rolesearch2: discord.PermissionOverwrite(read_messages=True)
        }
        hi = await guild.create_text_channel(str(user) + ' Supporter-Rang Antrag', overwrites=overwrites)
        await ctx.message.delete()
        await hi.send("Senden sie die zuvor aufgeführten Referenzen in diesen Channel. Ein Supporter wird sich schon bald um sie kümmern")


@client.command(aliases=['konto','Konto'])
async def _konto(ctx, arg=None):
    if (ctx.channel.id == 705010192042950726) or (ctx.channel.id ==673168938351198239):
        if arg == None:
            embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Bank",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um Hilfe zum Konto zu erhalten:**",
                            value="$konto help", inline=False)

            rr = await ctx.send(embed=embed)
        elif (arg.lower() == "help") or (arg.lower() == "hilfe") or (arg.lower() == "rules") or (arg.lower() == "regeln"):
            embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Bank",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um ein Konto zu erstellen:**",
                            value="$konto create", inline=True)
            embed.add_field(name="**Um seinen Kontostand einzusehen:**",
                            value="$konto view", inline=True)

            rr = await ctx.send(embed=embed)
        elif arg.lower() == "create":
            embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description=" ⌛ Ihr Konto wird gesucht ⌛ ")
            embed.set_author(name="Golden Doors Bank",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")

            rr = await ctx.send(embed=embed)
            channel = client.get_channel(889118584318619678)

            #isInKonto = await isKonto(ctx, ctx.author, 0)
            getInKonto = await getKonto(ctx.author)
            if getInKonto:
                embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="-- Sie haben bereits ein Konto erstellt --")
                embed.set_author(name="Golden Doors Bank",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                embed.add_field(name="**Kontostand:**",
                                value="{}$".format(getInKonto), inline=False)

                await rr.edit(embed=embed)
                return
            else:
                await channel.send("{}".format(ctx.author.id) + ":1500:🐎")
                embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="-- Ihr Konto wurde erfolgreich erstellt --")
                embed.set_author(name="Golden Doors Bank",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                embed.add_field(name="**Kontostand:**",
                                value="1500$", inline=False)

                await rr.edit(embed=embed)

        elif arg.lower() == "view":
            embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description=" ⌛ Ihr Konto wird gesucht ⌛ ")
            embed.set_author(name="Golden Doors Bank",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")

            rr = await ctx.send(embed=embed)
            channel = client.get_channel(889118584318619678)

            isInKonto = await isKonto(ctx, ctx.author, 1)
            getInKonto = await getKonto(ctx.author)
            if isInKonto:
                embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="-- Konto Informationen --")
                embed.set_author(name="Golden Doors Bank",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                embed.add_field(name="**Kontostand:**",
                                value="{}$".format(getInKonto), inline=False)

                await rr.edit(embed=embed)
                return
            else:
                embed = discord.Embed(title="{}".format(ctx.author), colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="-- Sie besitzen noch kein Konto --")
                embed.set_author(name="Golden Doors Bank",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                embed.add_field(name="**Konto hilfe:**",
                                value="$konto help", inline=False)

                await rr.edit(embed=embed)


async def isKonto(ctx, user, money):
    channel = client.get_channel(889118584318619678)

    async for msg in channel.history(limit=10000):
        message = str(msg.content).split(":")
        if message[0] == str(user.id):
            if money <= 0:
                return False         
            eM = await enoughMoney(message, user, money)
            if eM:
                return True
    return False


async def getKonto(user):
    channel = client.get_channel(889118584318619678)

    async for msg in channel.history(limit=10000):
        message = str(msg.content).split(":")
        if message[0] == str(user.id):
            return message[1]


async def removeMoney(ctx, user, money):
    channel = client.get_channel(889118584318619678)

    async for msg in channel.history(limit=10000):
        message = str(msg.content).split(":")
        if message[0] == str(user.id):
            await msg.delete()
            await channel.send(str(user.id) + ":" + str(int(message[1]) - int(money)) + ":" + str(message[2]))
            await testRank(ctx, user, int(message[1]) + money)
            return
          
async def addMoney(ctx, user, money):
    channel = client.get_channel(889118584318619678)

    async for msg in channel.history(limit=10000):
        message = str(msg.content).split(":")
        if message[0] == str(user.id):
            await msg.delete()
            await channel.send(str(user.id) + ":" + str(int(message[1]) + int(money)) + ":" + str(message[2]))
            await testRank(ctx, user, int(message[1]) + money)
            return


async def getEmoji(ctx, user):
    channel = client.get_channel(889118584318619678)

    async for msg in channel.history(limit=10000):
        message = str(msg.content).split(":")
        if message[0] == str(user.id):
            return message[2]



async def enoughMoney(message, user, money):
    if int(message[1]) >= money:
        return True
    return False


async def testRank(ctx, user, money):
    channel = client.get_channel(889118584318619678)

    userList = []
    moneyList = []
    async for msg in channel.history(limit=10000):
        message = str(msg.content).split(":")
        userList.append(message[0])
        moneyList.append(message[1])
    channel = discord.utils.get(ctx.guild.channels, id=903965902125559808)
    msg = await channel.fetch_message(903979231871123506)
    moneyList = [int(i) for i in moneyList]
    embed = discord.Embed(title="Casino Leaderboard", colour=0xff00f6,
                          url="https://www.Youtube.com")
    embed.set_author(name="Golden Doors Casino",
                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
    user = await client.fetch_user(userList[moneyList.index(max(moneyList))])
    embed.add_field(name="**1. Platz:**",
                    value=f"**{user}** -> {max(moneyList)}", inline=False)
    userList.remove(userList[moneyList.index(max(moneyList))])
    moneyList.remove(max(moneyList))
    user = await client.fetch_user(userList[moneyList.index(max(moneyList))])
    embed.add_field(name="**2. Platz:**",
                    value=f"**{user}** -> {max(moneyList)}", inline=False)
    userList.remove(userList[moneyList.index(max(moneyList))])
    moneyList.remove(max(moneyList))
    user = await client.fetch_user(userList[moneyList.index(max(moneyList))])
    embed.add_field(name="**3. Platz:**",
                    value=f"**{user}** -> {max(moneyList)}", inline=False)

    await msg.edit(embed=embed)


@client.command(aliases=['__am'])
async def _addMoney(ctx, user: discord.User, arg2=None):
    if (ctx.channel.id == 889118584318619678) or (ctx.channel.id ==673168938351198239):
        await addMoney(ctx, user, int(arg2))
        await ctx.message.delete()


@client.command(aliases=['__rm'])
async def _removeMoney(ctx, user: discord.User, arg2=None):
    if (ctx.channel.id == 889118584318619678) or (ctx.channel.id ==673168938351198239):
        await removeMoney(ctx, user, int(arg2))
        await ctx.message.delete()


@client.command(aliases=['ranking'])
async def _ranking(ctx, arg=None):
    if (ctx.channel.id == 903965902125559808) or (ctx.channel.id ==673168938351198239):
        if arg == None:
            embed = discord.Embed(title="Casino Leaderboard", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**1. Platz:**",
                            value="Playername -> Money", inline=True)
            embed.add_field(name="**2. Platz:**",
                            value="Playername -> Money", inline=True)
            embed.add_field(name="**3. Platz:**",
                            value="Playername -> Money", inline=True)

            rr = await ctx.send(embed=embed)


@client.command(aliases=['games'])
async def _games(ctx):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239):
        embed = discord.Embed(title="Games", colour=0xff00f6,
                                  url="https://www.Youtube.com")
        embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
        embed.add_field(name="**Pferderennen:**",
                            value="$pr help", inline=False)
        embed.add_field(name="**Blackjack:**",
                            value="$bj help", inline=False)
        embed.add_field(name="**Glücksrad:**",
                        value="$gr help", inline=False)
        embed.add_field(name="**Slot Machine:**",
                        value="$slot help", inline=False)
        embed.add_field(name="**Higher Lower:**",
                        value="$hl help", inline=False)
        await ctx.send(embed=embed)


@client.command(aliases=['pr', 'pferderennen', 'PR', 'Pferderennen', 'hr', 'horserace', 'HR', 'Horserace'])
async def _pr(ctx, arg=None, arg2=None):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239):
        if arg == None:
            embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$pr start", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$pr help", inline=False)
            embed.add_field(name="**Um den Shop zu öffnen:**",
                            value="$pr shop", inline=False)
            embed.add_field(name="**Um ein Item zu kaufen:**",
                            value="$pr buy (Item Nummer)", inline=False)

            rr = await ctx.send(embed=embed)
        elif (arg.lower() == "help") or (arg.lower() == "hilfe") or (arg.lower() == "rules") or (arg.lower() == "regeln"):
            embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$pr start", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$pr help", inline=False)
            embed.add_field(name="**Um den Shop zu öffnen:**",
                            value="$pr shop", inline=False)
            embed.add_field(name="**Um ein Item zu kaufen:**",
                            value="$pr buy (Item Nummer)", inline=False)
            embed.add_field(name="**Einsatz:**",
                            value="100$", inline=True)
            embed.add_field(name="**Gewinn:**",
                            value="200$", inline=True)
            embed.add_field(name="**Regeln:**",
                            value="- Aufs eigene Pferd setzen und gewinnen!", inline=False)

            rr = await ctx.send(embed=embed)
        elif (arg.lower() == "shop") or (arg.lower() == "store"):
            embed = discord.Embed(title="Pferderennen Shop", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Kaufgegenstände:**",
                            value="**ㅤㅤㅤㅤㅤ╔╣Gewöhnlich╠╗**", inline=False)
            embed.add_field(name="**Item 1 : 🐌**",
                            value="Kosten: 200$", inline=True)
            embed.add_field(name="**Item 2: 🐖**",
                            value="Kosten: 200$", inline=True)
            embed.add_field(name="**Item 3: 🐕**",
                            value="Kosten: 200$", inline=True)
            embed.add_field(name="**Item 4: 🐓**",
                            value="Kosten: 200$", inline=True)
            embed.add_field(name="**Item 5: 🐀**",
                            value="Kosten: 200$", inline=True)
            embed.add_field(name="ㅤ",
                            value="**ㅤㅤㅤㅤㅤㅤ╔╣Selten╠╗**", inline=False)
            embed.add_field(name="**Item 6: 🐈**",
                            value="Kosten: 500$", inline=True)
            embed.add_field(name="**Item 7: 🦀**",
                            value="Kosten: 500$", inline=True)
            embed.add_field(name="**Item 8: 🐢**",
                            value="Kosten: 500$", inline=True)
            embed.add_field(name="ㅤ",
                            value="**ㅤㅤㅤㅤㅤㅤ╔╣Episch╠╗**", inline=False)
            embed.add_field(name="**Item 9: 🐒**",
                            value="Kosten: 1000$", inline=True)
            embed.add_field(name="**Item 10: 🐘**",
                            value="Kosten: 1000$", inline=True)
            embed.add_field(name="**Item 11: 🦘**",
                            value="Kosten: 1000$", inline=True)
            embed.add_field(name="ㅤ",
                            value="**ㅤㅤㅤ   ㅤㅤ╔╣Legendary╠╗**", inline=False)
            embed.add_field(name="**Item 12: 🦥:**",
                            value="Kosten: 10000$", inline=True)
            embed.add_field(name="**Item 13: 🦖**",
                            value="Kosten: 10000$", inline=True)
            embed.add_field(name="ㅤ",
                        value="**$pr buy (Item Nummer)**", inline=False)
            rr = await ctx.send(embed=embed)

        elif arg.lower() == "buy":
            emojiList = ['🐌', '🐖', '🐕', '🐓', '🐀', '🐈', '🦀', '🐢', '🐒', '🐘', '🦘', '🦥', '🦖']
            try:
                num = int(arg2) -1
            except:
                return
            if int(arg2) == 1:
                money = 200
            elif int(arg2) == 2:
                money = 200
            elif int(arg2) == 3:
                money = 200
            elif int(arg2) == 4:
                money = 200
            elif int(arg2) == 5:
                money = 200
            elif int(arg2) == 6:
                money = 500
            elif int(arg2) == 7:
                money = 500
            elif int(arg2) == 8:
                money = 500
            elif int(arg2) == 9:
                money = 1000
            elif int(arg2) == 10:
                money = 1000
            elif int(arg2) == 11:
                money = 1000
            elif int(arg2) == 12:
                money = 1000
            elif int(arg2) == 13:
                money = 10000
            elif int(arg2) == 14:
                money = 10000
            else:
                return
            isInKonto = await isKonto(ctx, ctx.author, money)
            if isInKonto:
                emoji = emojiList[num]
                channel = client.get_channel(889118584318619678)
                async for msg in channel.history(limit=10000):
                    message = str(msg.content).split(":")
                    if message[0] == str(ctx.author.id):
                        await msg.delete()
                        await channel.send(str(ctx.author.id) + ":" + str(message[1]) + ":" + str(emoji))
                await removeMoney(ctx, ctx.author, money)
            else:
                await ctx.author.send("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                return


        elif arg.lower() == "start":
            money = 100 
            embed = discord.Embed(title="Pferderennen <a:loading:904384754944733274>", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="Um der Runde beizutreten, Reaktion hinzufügen! (Start in 10 Sek)")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")

            react = await ctx.send(embed=embed)
            await react.add_reaction('✅')
            timer = 10
            pferde_members = []
            emojis = []
            while(True):
                if timer == 0:
                    break
                timer -= 1
                await asyncio.sleep(0.5)
                member = await ctx.channel.fetch_message(react.id)
                for reactor in member.reactions:
                    async for user in reactor.users():
                        if not user.bot:
                            if reactor.emoji == '✅':
                                isInKonto = await isKonto(ctx, user, money)
                                if isInKonto:
                                    pferde_members.append(user)
                                    await removeMoney(ctx, user, 100)
                                    emoji = await getEmoji(ctx, ctx.author)
                                    emojis.append(str(emoji))
                                    await react.remove_reaction('✅', user)
                                    embed = discord.Embed(title="Pferderennen <a:loading:904384754944733274>", colour=0xff00f6,
                                                          url="https://www.Youtube.com",
                                                          description="Um der Runde beizutreten, Reaktion hinzufügen! (Start in 10 Sek)")
                                    embed.set_author(name="Golden Doors Casino",
                                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                                    tn = ""
                                    for user in pferde_members:
                                        tn += user.mention + ", "
                                    tn += "..."
                                    embed.add_field(name="**Teilnehmer:**",
                                                    value=tn, inline=False)
                                    await react.edit(embed=embed)
                                else:
                                    await user.send("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                                    await react.remove_reaction('✅', user)
            if len(pferde_members) == 0:
                embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="Das Rennen wurde abgebrochen")
                embed.set_author(name="Golden Doors Casino",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                await react.edit(embed=embed)
                return

            embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="Das Rennen wird gestartet...")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            tn = ""
            for user in pferde_members:
                tn += user.mention + ", "
            tn += "..."
            embed.add_field(name="**Teilnehmer:**",
                            value=tn, inline=False)
            await react.edit(embed=embed)
            await asyncio.sleep(3)

            embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")

            if len(pferde_members) > 1:
                sleep = ['0.9', '0.7', '0.5', '1', '0.6', '0.8']
                m = []
                for user in pferde_members:
                    embed.add_field(name=user,
                                    value=f"🏴 ▫▫▫▫▫▫▫▫▫▫▫▫▫{emojis[pferde_members.index(user)]} 🏳️", inline=False)
                    m.append(0)
                await react.edit(embed=embed)
                end = False
                while end == False:
                    embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                          url="https://www.Youtube.com")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    sl = random.choice(sleep)
                    ra = randint(0, len(pferde_members) - 1)
                    m[ra] += 1
                    await asyncio.sleep(float(sl))
                    for user in pferde_members:
                        pValue = "🏴 "
                        p = 0
                        while p < 13 - m[pferde_members.index(user)]:
                            p += 1
                            pValue += "▫"
                        pValue += str(emojis[pferde_members.index(user)])
                        p = 0
                        while p < m[pferde_members.index(user)]:
                            p += 1
                            pValue += "▫"
                        pValue += " 🏳️"
                        embed.add_field(name=user,
                                    value=pValue, inline=False)
                    await react.edit(embed=embed)
                    for user in m:
                        if user >= 13:
                            embed.add_field(name="Der Gewinner ist:",
                                            value="{.mention}!".format(pferde_members[m.index(user)]), inline=False)
                            await react.edit(embed=embed)
                            await addMoney(ctx, pferde_members[0], 200)
                            end = True
            else:
                embed.add_field(name=pferde_members[0],
                                value=f"🏴 ▫▫▫▫▫▫▫▫▫▫▫▫▫{emojis[pferde_members.index(user)]} 🏳️", inline=False)
                embed.add_field(name="Bot Gegner",
                                value="🏴 ▫▫▫▫▫▫▫▫▫▫▫▫▫🐎 🏳️", inline=False)
                await react.edit(embed=embed)

                sleep = ['0.9', '0.7', '0.5', '1', '0.6', '0.8']
                r1 = ['🏴 ▫▫▫▫▫▫▫▫▫▫▫▫▫🐎 🏳️',
                      '🏴 ▫▫▫▫▫▫▫▫▫▫▫▫▫🐎 🏳️',
                      '🏴 ▫▫▫▫▫▫▫▫▫▫▫▫🐎▫ 🏳️',
                      '🏴 ▫▫▫▫▫▫▫▫▫▫▫🐎▫▫ 🏳️',
                      '🏴 ▫▫▫▫▫▫▫▫▫▫🐎▫▫▫ 🏳️',
                      '🏴 ▫▫▫▫▫▫▫▫▫🐎▫▫▫▫ 🏳️',
                      '🏴 ▫▫▫▫▫▫▫▫🐎▫▫▫▫▫ 🏳️',
                      '🏴 ▫▫▫▫▫▫▫🐎▫▫▫▫▫▫ 🏳️',
                      '🏴 ▫▫▫▫▫▫🐎▫▫▫▫▫▫▫ 🏳️',
                      '🏴 ▫▫▫▫▫🐎▫▫▫▫▫▫▫▫ 🏳️',
                      '🏴 ▫▫▫▫🐎▫▫▫▫▫▫▫▫▫ 🏳️',
                      '🏴 ▫▫▫🐎▫▫▫▫▫▫▫▫▫▫ 🏳️',
                      '🏴 ▫▫🐎▫▫▫▫▫▫▫▫▫▫▫ 🏳️',
                      '🏴 ▫🐎▫▫▫▫▫▫▫▫▫▫▫▫ 🏳️',
                      '🏴 🐎▫▫▫▫▫▫▫▫▫▫▫▫▫ 🏳️',]
                r2 = r1
                m1 = 0
                m2 = 0
                winner = 0
                while (m1 < 14) and (m2 < 14):
                    sl = random.choice(sleep)
                    ra = randint(1, 2)
                    if int(ra) == 2:
                        m1 += 1
                        await asyncio.sleep(float(sl))
                        embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                              url="https://www.Youtube.com")
                        embed.set_author(name="Golden Doors Casino",
                                         icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                        for user in pferde_members:
                            pValue = "🏴 "
                            p = 0
                            while p < 13 - m1:
                                p += 1
                                pValue += "▫"
                            pValue += str(emojis[pferde_members.index(user)])
                            p = 0
                            while p < m1:
                                p += 1
                                pValue += "▫"
                            pValue += " 🏳️"
                            embed.add_field(name=user,
                                            value=pValue, inline=False)
                        embed.add_field(name="Bot Gegner",
                                        value=r2[m2], inline=False)
                        await react.edit(embed=embed)
                        if m1 >= 13:
                            winner = 1
                    else:
                        m2 += 1
                        await asyncio.sleep(float(sl))
                        embed = discord.Embed(title="Pferderennen", colour=0xff00f6,
                                              url="https://www.Youtube.com")
                        embed.set_author(name="Golden Doors Casino",
                                         icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                        for user in pferde_members:
                            pValue = "🏴 "
                            p = 0
                            while p < 13 - m1:
                                p += 1
                                pValue += "▫"
                            pValue += str(emojis[pferde_members.index(user)])
                            p = 0
                            while p < m1:
                                p += 1
                                pValue += "▫"
                            pValue += " 🏳️"
                            embed.add_field(name=user,
                                            value=pValue, inline=False)
                        embed.add_field(name="Bot Gegner",
                                        value=r2[m2], inline=False)
                        await react.edit(embed=embed)
                        if m2 >= 13:
                            winner = 2
                if winner == 1:

                    embed.add_field(name="Der Gewinner ist:",
                                    value="{.mention}!".format(pferde_members[0]), inline=False)
                    await react.edit(embed=embed)
                    await addMoney(ctx, pferde_members[0], 200)

                elif winner == 2:
                    embed.add_field(name="Der Gewinner ist:",
                                    value="Bot Gegner", inline=False)
                    await react.edit(embed=embed)


@client.command(aliases=['gr'])
async def _gr(ctx, arg=None, arg2=None):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239):
        try:
            client.queue[ctx.guild.id]
        except:
            client.queue[ctx.guild.id] = []
        if arg == None:
            embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$gr start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$gr help", inline=False)

            rr = await ctx.send(embed=embed)
        elif (arg.lower() == "help") or (arg.lower() == "hilfe") or (arg.lower() == "rules") or (arg.lower() == "regeln"):
            embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$gr start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$gr help", inline=False)
            embed.add_field(name="**Einsatz:**",
                            value="???$", inline=True)
            embed.add_field(name="**Gewinn:**",
                            value="???$", inline=True)
            embed.add_field(name="**Regeln:**",
                            value="- Rad drehen und fette Gewinne abstauben!", inline=False)

            rr = await ctx.send(embed=embed)
        elif arg2 == None:
            embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$gr start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$gr help", inline=False)

            rr = await ctx.send(embed=embed)
            return
        elif arg.lower() == "start":
            money = int(arg2)
            if ctx.author in client.queue[ctx.guild.id]:
                await ctx.send("**Warte bis deine vorherige Runde beendet wurde!**")
                return
            client.queue[ctx.guild.id].append(ctx.author)
            isInKonto = await isKonto(ctx, ctx.author, money)
            if isInKonto:
                await removeMoney(ctx, ctx.author, money)
            else:
                await ctx.author.send("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                return

            embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="**Das Rad wird gedreht...**")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            react = await ctx.send(embed=embed)
            await asyncio.sleep(3)

            await react.edit(content='--      **Glücksrad**    --\n'
                                       '               🔻\n'
                                       '        🔂 ❌ 🔪\n'
                                       ' 🆙                      💜\n'
                                       ' 💛        :radio_button:        ❓\n'
                                       ' 🔪                      ❌\n'
                                       '        🔂 ❌ 💜\n')
            glücksrad = 0
            while glücksrad < 2:
                wheel = ['--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔂 ❌ 🔪\n'
                         ' 🆙                      💜\n'
                         ' 💛        :radio_button:        ❓\n'  # 0 n
                         ' 🔪                      ❌\n'
                         '        🔂 ❌ 💜\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🆙 🔂 ❌\n'
                         ' 💛                      🔪\n'
                         ' 🔪        :radio_button:        💜\n'  # 1 r
                         ' 🔂                      ❓\n'
                         '        ❌ 💜 ❌\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        💛 🆙 🔂\n'
                         ' 🔪                      ❌\n'
                         ' 🔂        :radio_button:        🔪\n'  # 2 u
                         ' ❌                      💜\n'
                         '        💜 ❌ ❓\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔪 💛 🆙\n'
                         ' 🔂                      🔂\n'
                         ' ❌        :radio_button:        ❌\n'  # 3 q
                         ' 💜                      🔪\n'
                         '        ❌ ❓ 💜\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔂 🔪 💛\n'
                         ' ❌                      🆙\n'
                         ' 💜        :radio_button:        🔂\n'  # 4 h
                         ' ❌                      ❌\n'
                         '        ❓ 💜 🔪\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❌ 🔂 🔪\n'
                         ' 💜                      💛\n'
                         ' ❌        :radio_button:        🆙\n'  # 5 r
                         ' ❓                      🔂\n'
                         '        💜 🔪 ❌\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        💜 ❌ 🔂\n'
                         ' ❌                      🔪\n'
                         ' ❓        :radio_button:        💛\n'  # 6 n
                         ' 💜                      🆙\n'
                         '        🔪❌ 🔂\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❌ 💜 ❌\n'
                         ' ❓                      🔂\n'
                         ' 💜        :radio_button:        🔪\n'  # 7 g
                         ' 🔪                      💛\n'
                         '        ❌ 🔂 🆙\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❓ ❌ 💜\n'
                         ' 💜                      ❌\n'
                         ' 🔪        :radio_button:        🔂\n'  # 8 n
                         ' ❌                      🔪\n'
                         '        🔂 🆙 💛\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        💜 ❓ ❌\n'
                         ' 🔪                      💜\n'
                         ' ❌        :radio_button:        ❌\n'  # 9 ?
                         ' 🔂                      🔂\n'
                         '        🆙 💛 🔪\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔪 💜 ❓\n'
                         ' ❌                      ❌\n'
                         ' 🔂        :radio_button:        💜\n'  # 10 g
                         ' 🆙                      ❌\n'
                         '        💛 🔪 🔂\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❌ 🔪 💜\n'
                         ' 🔂                      ❓\n'
                         ' 🆙        :radio_button:        ❌\n'
                         ' 💛                      💜\n'  # end    #11 h
                         '        🔪 🔂 ❌\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔂 ❌ 🔪\n'
                         ' 🆙                      💜\n'
                         ' 💛        :radio_button:        ❓\n'  # 12 n
                         ' 🔪                      ❌\n'
                         '        🔂 ❌ 💜\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🆙 🔂 ❌\n'
                         ' 💛                      🔪\n'
                         ' 🔪        :radio_button:        💜\n'  # 13 r
                         ' 🔂                      ❓\n'
                         '        ❌ 💜 ❌\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        💛 🆙 🔂\n'
                         ' 🔪                      ❌\n'
                         ' 🔂        :radio_button:        🔪\n'  # 14 u
                         ' ❌                      💜\n'
                         '        💜 ❌ ❓\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔪 💛 🆙\n'
                         ' 🔂                      🔂\n'
                         ' ❌        :radio_button:        ❌\n'  # 15 q
                         ' 💜                      🔪\n'
                         '        ❌ ❓ 💜\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔂 🔪 💛\n'
                         ' ❌                      🆙\n'
                         ' 💜        :radio_button:        🔂\n'  # 16 h
                         ' ❌                      ❌\n'
                         '        ❓ 💜 🔪\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❌ 🔂 🔪\n'
                         ' 💜                      💛\n'
                         ' ❌        :radio_button:        🆙\n'  # 17 r
                         ' ❓                      🔂\n'
                         '        💜 🔪 ❌\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        💜 ❌ 🔂\n'
                         ' ❌                      🔪\n'
                         ' ❓        :radio_button:        💛\n'  # 18 n
                         ' 💜                      🆙\n'
                         '        🔪❌ 🔂\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❌ 💜 ❌\n'
                         ' ❓                      🔂\n'
                         ' 💜        :radio_button:        🔪\n'  # 19 g
                         ' 🔪                      💛\n'
                         '        ❌ 🔂 🆙\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❓ ❌ 💜\n'
                         ' 💜                      ❌\n'
                         ' 🔪        :radio_button:        🔂\n'  # 20 n
                         ' ❌                      🔪\n'
                         '        🔂 🆙 💛\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        💜 ❓ ❌\n'
                         ' 🔪                      💜\n'
                         ' ❌        :radio_button:        ❌\n'  # 21 ?
                         ' 🔂                      🔂\n'
                         '        🆙 💛 🔪\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        🔪 💜 ❓\n'
                         ' ❌                      ❌\n'
                         ' 🔂        :radio_button:        💜\n'  # 22 g
                         ' 🆙                      ❌\n'
                         '        💛 🔪 🔂\n',
                         '--      **Glücksrad**    --\n'
                         '               🔻\n'
                         '        ❌ 🔪 💜\n'
                         ' 🔂                      ❓\n'
                         ' 🆙        :radio_button:        ❌\n'  # 23 h
                         ' 💛                      💜\n'
                         '        🔪 🔂 ❌\n']
                i = 0
                r = randint(3, 14)
                res = money
                while i < r:
                    i += 1
                    await asyncio.sleep(0.5)
                    await react.edit(content=wheel[i])
                if (i == 0) or (i == 6) or (i == 8) or (i == 12) or (i == 18) or (i == 20):
                    res = 0
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description="**Das war leider eine Niete**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    break
                elif (i == 1) or (i == 5) or (i == 13) or (i == 17):
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description="**Das Rad dreht noch einmal!!!**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                elif (i == 2) or (i == 14):
                    res += res
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description="**Das Rad dreht noch einmal mit doppeltem Einsatz!!!**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                elif (i == 3) or (i == 15):
                    res += res * 2
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description="**Du bekommst das dreifache von deinem Einsatz!!!**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                    await addMoney(ctx, ctx.author, int(res))
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    break
                elif (i == 7) or (i == 10) or (i == 19) or (i == 22):
                    res += res
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description="**Du bekommst das doppelte von deinem Einsatz!!!**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                    await addMoney(ctx, ctx.author, int(res))
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    break
                elif (i == 9) or (i == 21):
                    mistery = randint(100, 1000)
                    res += mistery
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description=f"**MISTERY!!! DU bekommst {mistery}$$$**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                    await addMoney(ctx, ctx.author, int(res))
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    break
                else:
                    res /= 2
                    embed = discord.Embed(title="Glücksrad", colour=0xff00f6,
                                          url="https://www.Youtube.com",
                                          description="**Du bekommst die hälfte von deinem Einsatz ;(**")
                    embed.set_author(name="Golden Doors Casino",
                                     icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    await react.edit(embed=embed)
                    await asyncio.sleep(3)
                    await addMoney(ctx, ctx.author, int(res))
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    break
            


@client.command(aliases=['slot'])
async def _slot(ctx, arg=None, arg2=None):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239):
        try:
            client.queue[ctx.guild.id]
        except:
            client.queue[ctx.guild.id] = []
        if arg == None:
            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$slot start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$slot help", inline=False)

            rr = await ctx.send(embed=embed)
        elif (arg.lower() == "help") or (arg.lower() == "hilfe") or (arg.lower() == "rules") or (arg.lower() == "regeln"):
            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$slot start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$slot help", inline=False)
            embed.add_field(name="**Einsatz:**",
                            value="???$", inline=True)
            embed.add_field(name="**Gewinn:**",
                            value="**🥇🥇❔ - 0.5x\n"
                                  "💎💎❔ - 2x\n"
                                  "💯💯❔ - 2x\n"
                                  "🥇🥇🥇 - 2.5x\n"
                                  "💎💎💎 - 3x\n"
                                  "💵💵❔ - 3.5x\n"
                                  "💯💯💯 - 4x\n"
                                  "💰💰❔ - 7x\n"
                                  "💵💵💵 - 7x\n"
                                  "💰💰💰 - 15x**", inline=False)

            rr = await ctx.send(embed=embed)
        elif arg2 == None:
            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$slot start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$slot help", inline=False)

            rr = await ctx.send(embed=embed)
            return
          
        elif arg.lower() == "start":
            money=int(arg2)
            if ctx.author in client.queue[ctx.guild.id]:
                await ctx.send("**Warte bis deine vorherige Runde beendet wurde!**")
                return
            client.queue[ctx.guild.id].append(ctx.author)
            isInKonto = await isKonto(ctx, ctx.author, money)
            if isInKonto:
                await removeMoney(ctx, ctx.author, money)
            else:
                await ctx.author.send("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                return
            emojiList = ['🥇', '💎', '💯', '💰', '💵']
            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="**----Jackpot**----")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**------------------**",
                            value="**| <a:slot:904342457980968980> | <a:slot:904342457980968980> | <a:slot:904342457980968980> |**", inline=False)
            embed.add_field(name="**------------------**",
                            value="**-Wird gedreht-**",
                            inline=False)
            rr = await ctx.send(embed=embed)
            await asyncio.sleep(random.uniform(3, 5))
            s1 = random.choice(emojiList)

            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="**----Jackpot**----")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**------------------**",
                            value=f"**| {s1} | <a:slot:904342457980968980> | <a:slot:904342457980968980> |**",
                            inline=False)
            embed.add_field(name="**------------------**",
                            value="**-Wird gedreht-**",
                            inline=False)
            await rr.edit(embed=embed)
            await asyncio.sleep(random.uniform(3, 5))
            s2 = random.choice(emojiList)

            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="**----Jackpot**----")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**------------------**",
                            value=f"**| {s1} | {s2} | <a:slot:904342457980968980> |**",
                            inline=False)
            embed.add_field(name="**------------------**",
                            value="**-Wird gedreht-**",
                            inline=False)
            await rr.edit(embed=embed)
            await asyncio.sleep(random.uniform(3, 5))
            s3 = random.choice(emojiList)

            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="**----Jackpot**----")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**------------------**",
                            value=f"**| {s1} | {s2} | {s3} |**",
                            inline=False)
            embed.add_field(name="**------------------**",
                            value="**-Wird gedreht-**",
                            inline=False)
            await rr.edit(embed=embed)

            if(s1 == "🥇") and (s2 == "🥇") and (s3 == "🥇"):
                gewinn = money * 2.5
            elif (s1 == "💰") and (s2 == "💰") and (s3 == "💰"):
                gewinn = money * 15
            elif (s1 == "💯") and (s2 == "💯") and (s3 == "💯"):
                gewinn = money * 4
            elif (s1 == "💎") and (s2 == "💎") and (s3 == "💎"):
                gewinn = money * 3
            elif (s1 == "💵") and (s2 == "💵") and (s3 == "💵"):
                gewinn = money * 7
            elif (s1 == "💵") and (s2 == "💵") or (s2 == "💵") and (s3 == "💵"):
                gewinn = money * 3.5
            elif (s1 == "💎") and (s2 == "💎") or (s2 == "💎") and (s3 == "💎"):
                gewinn = money * 2
            elif (s1 == "💯") and (s2 == "💯") or (s2 == "💯") and (s3 == "💯"):
                gewinn = money * 2
            elif (s1 == "💰") and (s2 == "💰") or (s2 == "💰") and (s3 == "💰"):
                gewinn = money * 7
            elif (s1 == "🥇") and (s2 == "🥇") or (s2 == "🥇") and (s3 == "🥇"):
                gewinn = money * 0.5
            else:
                embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="**----Jackpot**----")
                embed.set_author(name="Golden Doors Casino",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                embed.add_field(name="**------------------**",
                                value=f"**| {s1} | {s2} | {s3} |**",
                                inline=False)
                embed.add_field(name="**------------------**",
                                value=f"**--YOU LOST--**",
                                inline=False)
                await rr.edit(embed=embed)
                del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                return
            embed = discord.Embed(title="Slot Machine", colour=0xff00f6,
                                  url="https://www.Youtube.com",
                                  description="**----Jackpot**----")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**------------------**",
                            value=f"**| {s1} | {s2} | {s3} |**",
                            inline=False)
            embed.add_field(name="**------------------**",
                            value=f"**--YOU WON--**",
                            inline=False)
            embed.add_field(name="**Profit:**",
                            value=f"**{gewinn}**",
                            inline=False)
            await rr.edit(embed=embed)
            await addMoney(ctx, ctx.author, int(gewinn))
            del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])


@client.command(aliases=['spend', 'sp','Spend', 'Sp'])
async def _spend(ctx, user: discord.User=None, arg2=None):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239) or (ctx.channel.id ==705010192042950726):
        if arg2 == None or user == None:
            embed = discord.Embed(title="Spend", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Summe zu spenden:**",
                            value="$spend (player) (amount)", inline=False)

            rr = await ctx.send(embed=embed)
        elif arg2 != None:
            isInKonto = await isKonto(ctx, ctx.author, int(arg2))
            if isInKonto:
                try:
                    await addMoney(ctx, user, int(arg2))
                    await removeMoney(ctx, ctx.author, int(arg2))
                except:
                    pass
                embed = discord.Embed(title=f"{user}", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Summe erfolgreich überwiesen**",
                            value=f"{arg2}", inline=False)

            rr = await ctx.send(embed=embed)



@client.command(aliases=['z'])
async def z__(ctx, *, thema):
    with open('zitate.txt', 'r') as f:
        users= json.load(f)

    def high(msg):
        return msg.author == ctx.author

    if not str(thema) in users:
        users[str(thema)] = {}

    await ctx.send("Titel")
    client.hput = ctx.message.author
    response = await client.wait_for('message', timeout=180.0, check=high)
    titel = str(response.content)

    users[str(thema)][str(titel)] = ""
  
    await ctx.send("Zitat")
    response = await client.wait_for('message', timeout=180.0, check=high)
    zitat = str(response.content)

    users[str(thema)][str(titel)] = str(zitat)
  
    with open('zitate.txt', 'w') as f:
        json.dump(users, f)



@client.command(aliases=['zitat', 'zt','Zitat', 'Zt'])
async def _zt(ctx, arg=None, arg2=None):
    if (ctx.channel.id == 962079483723124737) or (ctx.channel.id ==673168938351198239):
        try:
            client.queue[ctx.guild.id]
        except:
            client.queue[ctx.guild.id] = []
        if arg == None:
            embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$zt start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$zt help", inline=False)

            rr = await ctx.send(embed=embed)
            return
        elif (arg.lower() == "help") or (arg.lower() == "hilfe") or (arg.lower() == "rules") or (arg.lower() == "regeln"):
            embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$zt start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$zt help", inline=False)
            embed.add_field(name="**Einsatz:**",
                            value="???$", inline=True)
            embed.add_field(name="**Gewinn:**",
                            value="**1.2x**", inline=False)

            rr = await ctx.send(embed=embed)
            return
        elif arg2 == None:
            embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6,
                                  url="https://www.Youtube.com")
            embed.set_author(name="Golden Doors Casino",
                             icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
            embed.add_field(name="**Um eine Runde zu starten:**",
                            value="$zt start (amount)", inline=False)
            embed.add_field(name="**Um Hilfe zum Spiel zu erhalten:**",
                            value="$zt help", inline=False)

            rr = await ctx.send(embed=embed)
            return
          
        elif arg.lower() == "start":
            while True:
                money=int(arg2)
                if ctx.author in client.queue[ctx.guild.id]:
                    await ctx.send("**Warte bis deine vorherige Runde beendet wurde!**")
                    return
                isInKonto = await isKonto(ctx, ctx.author, money)
                if isInKonto:
                    client.queue[ctx.guild.id].append(ctx.author)
                    await removeMoney(ctx, ctx.author, money)
                else:
                    await ctx.author.send("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    return
                with open('zitate.txt', 'r') as f:
                    file = json.load(f)
                randoms = []
                for theme in file:
                    randoms.append(theme) 
                themes = []
                for i in range(0, 3):
                    t = random.choice(randoms)
                    randoms.remove(t)
                    themes.append(t)
                titels = []
                for i in range(0, 3):
                    ts = []
                    for t in file[str(themes[i])]:
                        ts.append(str(t))
                    titels.append(random.choice(ts))
              
                zitate = []
                f = -1
                for titel in titels:
                    f += 1
                    zitate.append(file[str(themes[f])][titel])
    
                choosenZitat = random.choice(zitate)
              
                embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6,
                                      url="https://www.Youtube.com")
                embed.set_author(name="Golden Doors Casino",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                embed.add_field(name="**Aus welcher Serie oder Film stammt dieses Zitat?:**",
                                value=f"{choosenZitat}", inline=False)
                embed.add_field(name="**Serie 1:**",
                                value=f"{titels[0]}", inline=True)
                embed.add_field(name="**Serie 2:**",
                                value=f"{titels[1]}", inline=True)
                embed.add_field(name="**Serie 3:**",
                                value=f"{titels[2]}", inline=True)
    
                try:
                    await rr.edit(embed=embed)
                except:
                    rr = await ctx.send(embed=embed)
                await rr.add_reaction('1\N{COMBINING ENCLOSING KEYCAP}')
                await rr.add_reaction('2\N{COMBINING ENCLOSING KEYCAP}')
                await rr.add_reaction('3\N{COMBINING ENCLOSING KEYCAP}')
    
                def addreaction(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['1\N{COMBINING ENCLOSING KEYCAP}', '2\N{COMBINING ENCLOSING KEYCAP}', '3\N{COMBINING ENCLOSING KEYCAP}']
    
                try:
                    response = await client.wait_for('reaction_add', timeout=40.0, check=addreaction)
                except asyncio.TimeoutError:
                    #print("TimeoutError")
                    await rr.add_reaction('❌')
                    del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                    break
                am = 0
                k = await ctx.channel.fetch_message(rr.id)
                for reactor in k.reactions:
                    async for user in reactor.users():
                        if user == ctx.message.author:
                            if reactor.emoji == '1\N{COMBINING ENCLOSING KEYCAP}':
                                am = 0
                            elif reactor.emoji == '2\N{COMBINING ENCLOSING KEYCAP}':
                                am = 1
                            elif reactor.emoji == '3\N{COMBINING ENCLOSING KEYCAP}':
                                am = 2
                            else:
                                embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6, url="https://www.Youtube.com")
                                embed.set_author(name="Golden Doors Casino", icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                                embed.add_field(name=f"**Falsche Eingabe!**", value=f"ㅤ", inline=False)
                                await rr.edit(embed=embed)
                                await rr.add_reaction('❌')
                                del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)])
                                return
                if am == zitate.index(choosenZitat):
                    embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6,
                                      url="https://www.Youtube.com")
                    embed.set_author(name="Golden Doors Casino",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    embed.add_field(name=f"**{choosenZitat}**",
                                value=f"{titels[zitate.index(choosenZitat)]}", inline=False)
                    embed.add_field(name=f"**Du lagst richtig!**",
                                value=f"Gewinn: **{money * 1.2}**", inline=False)
                    await rr.edit(embed=embed)
                    await addMoney(ctx, ctx.author, money * 1.2)
                else:
                    embed = discord.Embed(title="Zitate-Raten", colour=0xff00f6,
                                      url="https://www.Youtube.com")
                    embed.set_author(name="Golden Doors Casino",
                                 icon_url="https://www.iconexperience.com/_img/g_collection_png/standard/512x512/bank_building.png")
                    embed.add_field(name=f"**Du lagst leider falsch! Richtig wäre:**",
                                value=f"{titels[zitate.index(choosenZitat)]}", inline=False)
                    await rr.edit(embed=embed)
                    await rr.add_reaction('❌')
                await rr.clear_reaction('1\N{COMBINING ENCLOSING KEYCAP}')
                await rr.clear_reaction('2\N{COMBINING ENCLOSING KEYCAP}')
                await rr.clear_reaction('3\N{COMBINING ENCLOSING KEYCAP}')
                await rr.add_reaction('🔁')
                del (client.queue[ctx.guild.id][client.queue[ctx.guild.id].index(ctx.author)]) 
                def addreac(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['🔁', '1⃣']
                  
                try:
                    res = await client.wait_for('reaction_add', timeout=40.0, check=addreac)
                except asyncio.TimeoutError:
                    return
                k = await ctx.channel.fetch_message(rr.id)
                for reactor in k.reactions:
                    async for user in reactor.users():
                        if user == ctx.message.author:
                            if reactor.emoji == '2⃣' or '1⃣':
                                await rr.clear_reaction('🔁')
                                await rr.clear_reaction('❌')
                            else:
                                print(reactor.emoji)
                                return


@client.command(aliases=['watch', 'Watch', 'yt', 'YT'])
async def _watch(ctx):
    voice = ctx.author.voice

    if not voice:
        return await ctx.send(':x: **Not connected to a voice channel!**')

    r = Route('POST', '/channels/{channel_id}/invites', channel_id=voice.channel.id)

    payload = {
        'max_age': 0,
        'target_type': 2,
        'target_application_id': 880218394199220334
    }

    try:
        code = (await client.http.request(r, json=payload))['code']
        print(code)
    except discord.Forbidden:
        return await ctx.send(':x: **Need the `Create Invite` permission.**')

    await ctx.send(embed=discord.Embed(description=f'[Klicke hier um Watch Together zu starten!](https://discord.gg/{code})', color=0x2F3136))

@client.command(aliases=['wordl', 'Wordl'])
async def _wordl(ctx):
    voice = ctx.author.voice

    if not voice:
        return await ctx.send(':x: **Not connected to a voice channel!**')

    r = Route('POST', '/channels/{channel_id}/invites', channel_id=voice.channel.id)

    payload = {
        'max_age': 0,
        'target_type': 2,
        'target_application_id': 879863976006127627
    }

    try:
        code = (await client.http.request(r, json=payload))['code']
        print(code)
    except discord.Forbidden:
        return await ctx.send(':x: **Need the `Create Invite` permission.**')

    await ctx.send(embed=discord.Embed(description=f'[Klicke hier um Wordl zu starten!](https://discord.gg/{code})', color=0x2F3136))

@client.command(aliases=['se'])
async def __se(ctx):
    await ctx.send(file=discord.File(r'video.mp4'))

  
@client.command(aliases=['higherlower', 'hl','Higherlower', 'Hl'])
async def __hl(ctx, arg=None, arg2=None):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239):
        try:
            client.queue[ctx.guild.id]
        except:
            client.queue[ctx.guild.id] = []
          
        if arg == None or arg is not None:
            money, pot, score = 1000, 0, 0 
            if arg is not None:
                money = int(arg)
            randoms = []
            guess, again, emb, emb2 = None, None, None, None
            player = ctx.author.name
          
            embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
            embed.set_author(name="Golden Doors Casino", icon_url=client.link)
            embed.add_field(name="ㅤ", value=f"Wähle eine der dargestellten Optionen", inline=False)

            HelpButton = discord.ui.Button(label="Help", style=discord.enums.ButtonStyle.grey)
            StatsButton = discord.ui.Button(label="Stats", style=discord.enums.ButtonStyle.grey)
            PlayButton = discord.ui.Button(label="Play", style=discord.enums.ButtonStyle.green)
            HigherButton = discord.ui.Button(label="Higher", style=discord.enums.ButtonStyle.green)
            LowerButton = discord.ui.Button(label="Lower", style=discord.enums.ButtonStyle.red)
            AgainButton = discord.ui.Button(label="Erneut Spielen", style=discord.enums.ButtonStyle.blurple)
            CashButton = discord.ui.Button(label="Auszahlung", style=discord.enums.ButtonStyle.green)
          
            async def callbackHelp(interaction: discord.Interaction):
                embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Standart Einsatz | **{money} $**", inline=True)
                embed.add_field(name="ㅤ", value=f"Standart Gewinn | **{money * 0.2} $ pro Score**", inline=True)
                embed.add_field(name="ㅤ", value=f"Runde starten | **Button: Play**", inline=False)
                embed.add_field(name="ㅤ", value=f"Stats einsehen | **Button: Stats**", inline=True)
                embed.add_field(name="ㅤ", value=f"Regelwerk | **...**", inline=False)
                view = discord.ui.View(timeout=120)
                view.add_item(StatsButton)
                view.add_item(PlayButton)
                await emb.edit(embed=embed, view=view)
              
            async def callbackHigher(interaction: discord.Interaction):
                nonlocal guess, player 
                if player != interaction.user.name:
                    return
                if guess is None: guess = True 
              
            async def callbackLower(interaction: discord.Interaction):
                nonlocal guess, player 
                if player != interaction.user.name:
                    return
                if guess is None: guess = False 
              
            async def callbackStats(interaction: discord.Interaction):
                nonlocal player 
                if player != interaction.user.name:
                    return
                print("Stats")

            async def callbackAgain(interaction: discord.Interaction):
                nonlocal again, player
                if player != interaction.user.name:
                    return
                again = True

            async def callbackCash(interaction: discord.Interaction):
                nonlocal emb, emb2, score, money, player
                if player != interaction.user.name:
                    return
              
                gewinn = money * 0.2 * score
              
                embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Score | **{score}**ㅤ Gewinn | **{gewinn - money}**", inline=False)
                  
                view = discord.ui.View(timeout=120)
                await emb2.edit(embed=embed, view=view)
                await emb.delete()

                await addMoney(ctx, interaction.user, gewinn)
                del (client.queue[interaction.guild_id][client.queue[interaction.guild_id].index(interaction.user)])
              
            async def callbackPlay(interaction: discord.Interaction):
                nonlocal money, pot, randoms, guess, again, score, emb, emb2, player
                if player != interaction.user.name:
                    return
                  
                if interaction.user in client.queue[interaction.guild_id]:
                    await interaction.response.send_message(f"**Warte bis deine vorherige Runde beendet wurde!**", ephemeral=True)
                    return
                  
                isInKonto = await isKonto(ctx, interaction.user, money)
                if isInKonto:
                    await removeMoney(ctx, interaction.user, money)
                    client.queue[interaction.guild_id].append(interaction.user)
                else:
                    await interaction.response.send_message("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                    return
                  
                with open('higherlower.txt', 'r') as f:
                    low = json.load(f)
                  
                for title in low:
                    randoms.append(title)
                  
                name = random.choice(randoms)
                while (True):
                    
                    name1 = name 
                    #query = name.replace(' ', '+')
                    #page = [1, 2, 3, 4, 5] 
                    #session = aiohttp.ClientSession()
                    url = low[str(name)]['url']
                    #async with session.get(f'https://pixabay.com/api/?key=26750507-c0e611b2950a26b052e2d1b71'                                                            f'&q={query}&lang=de') as r:
                    #    if r.status in range(200, 299):
                    #        try:
                    #            data = await r.json()
                    #            image_url = data["hits"][0]["webformatURL"]
                    #            url = str(image_url)
                    #        except IndexError:
                    #            print(f"Image not found {name}")
                    #            url = "https://google.de"
                    #    else:
                    #        print("Image status not found")
                    #        url = "https://google.de"
                    #await session.close()
                    #response = google_images_download.googleimagesdownload()
                    #keywords = name
                    #arguments = {"keywords":keywords,"limit":1,"print_urls":True}
                    #paths = response.download(arguments)
                    #print(paths)
                    amount1 = low[str(name)]['amount']

                    embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
                    embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                    embed.add_field(name="ㅤ", value=f"Search | **{name}**ㅤ Monatlich gesucht | **{amount1}**", inline=False)
                    embed.set_image(url=str(url))
                  
                    view = discord.ui.View(timeout=120)
                    await emb.edit(embed=embed, view=view)

                    name = random.choice(randoms)
                    url = low[str(name)]['url']
                    amount2 = low[str(name)]['amount']

                    embed = discord.Embed(title=f"{name} gesucht im Gegensatz zu {name1}", description=f"Score | **{score}**") 
                    embed.add_field(name="ㅤ", value=f"Search | **{name}**ㅤ Monatlich gesucht | **???**", inline=False)
                    embed.set_image(url=str(url))
                  
                    HigherButton.callback, LowerButton.callback = callbackHigher, callbackLower  
                    view = discord.ui.View(timeout=120)
                    view.add_item(HigherButton)
                    view.add_item(LowerButton)
                  
                    try:
                        await emb2.edit(embed=embed, view=view)
                    except:
                        emb2 = await interaction.channel.send(embed=embed, view=view)
  
                    timeout = time.time() + 60*2
                    while (True):
                        if time.time() > timeout:
                            gewinn = money * 0.2 * score
                            await addMoney(ctx, interaction.user, gewinn)
                            embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
                            embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                            embed.add_field(name="ㅤ", value=f"Score | **{score}**ㅤ Gewinn | **{gewinn - money}**", inline=False)
                            view = discord.ui.View(timeout=120)
                            await emb2.edit(embed=embed, view=view)    
                            await emb.delete()
                            del (client.queue[interaction.guild_id][client.queue[interaction.guild_id].index(interaction.user)])
                            return
                        elif guess is not None:
                            break
                        await asyncio.sleep(2) 
                    right = False  
                    if amount1 < amount2:
                        if guess == True:
                            right = True  
                    elif amount1 > amount2:
                        if guess == False:
                            right = True  
                    else: right = True 

                    AgainButton.callback, CashButton.callback = callbackAgain, callbackCash 

                    if right == False:
                        embed = discord.Embed(title=f"Du lagst leider **Falsch**!", description=f"Score | **{score}**") 
                        embed.add_field(name="ㅤ", value=f"{name1} | **{amount1}**ㅤvs.ㅤ{name} | **{amount2}**", inline=False)
                        embed.set_image(url=str(url))

                        view = discord.ui.View(timeout=120)
                        view.add_item(AgainButton)
                        view.add_item(CashButton)
                        await emb2.edit(embed=embed, view=view)

                        again = False
                        timeout = time.time() + 60*2
                        while (True):
                            if time.time() > timeout:
                                gewinn = money * 0.2 * score
                                await addMoney(ctx, interaction.user, gewinn)
                                embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
                                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                                embed.add_field(name="ㅤ", value=f"Score | **{score}**ㅤ Gewinn | **{gewinn - money}**", inline=False)
                                view = discord.ui.View(timeout=120)
                                await emb2.edit(embed=embed, view=view)    
                                await emb.delete()
                                del (client.queue[interaction.guild_id][client.queue[interaction.guild_id].index(interaction.user)])
                                return
                            elif again:
                                guess = None
                                gewinn = money * 0.2 * score
                                score = 0 
                                await addMoney(ctx, interaction.user, gewinn)
                                isInKonto = await isKonto(ctx, interaction.user, money)
                                if isInKonto:
                                    await removeMoney(ctx, interaction.user, money) 
                                else:
                                    await interaction.response.send_message("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                                    return 
                                embed = discord.Embed(title=f"HigherLower | User: {ctx.author}", description=" ")
                                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                                embed.add_field(name="ㅤ", value=f"Score | **{score}**ㅤ Gewinn | **{gewinn - money}**", inline=False)
                                embed.add_field(name="ㅤ", value=f"Die Nächste Runde wird vorbereitet...", inline=False)
                                  
                                view = discord.ui.View(timeout=120)
                                await emb2.edit(embed=embed, view=view)    
                                await asyncio.sleep(3)
                                break
                            await asyncio.sleep(2)
                      
                    else:
                        score += 1
                        guess = None
                        embed = discord.Embed(title=f"Du lagst **Richtig**!", description=f"Score | **{score}**") 
                        embed.add_field(name="ㅤ", value=f"{name1} | **{amount1}**ㅤvs.ㅤ{name} | **{amount2}**", inline=False)
                        embed.set_image(url=str(url))
                      
                        view = discord.ui.View(timeout=120)
                        await emb2.edit(embed=embed, view=view)

                        await asyncio.sleep(5)

            HelpButton.callback, StatsButton.callback, PlayButton.callback = callbackHelp, callbackStats, callbackPlay
        
            view = discord.ui.View(timeout=120)
            view.add_item(HelpButton)
            view.add_item(StatsButton)
            view.add_item(PlayButton)
          
            emb = await ctx.send(embed=embed, view=view)
            return
          
@client.command(aliases=['bj', 'blackjack', 'BJ', 'Blackjack'])
async def __bj(ctx, arg=None, arg2=None):
    if (ctx.channel.id == 705042416348037210) or (ctx.channel.id ==673168938351198239):
        try:
            client.queue[ctx.guild.id]
        except:
            client.queue[ctx.guild.id] = []
          
        if arg == None:
            blackjack_members = []
            card_members = []
            out_members = []
            invCards = {}
            cards = ['2 ♥️', '3 ♥️', '4 ♥️', '5 ♥️', '6 ♥️', '7 ♥️', '8 ♥️', '9 ♥️', '10 ♥️', 'B ♥️', 'D ♥️', 'K ♥️', 'A ♥️', '2 ♣️', '3 ♣️', '4 ♣️', '5 ♣️', '6 ♣️', '7 ♣️',
                     '8 ♣️', '9 ♣️', '10 ♣️', 'B ♣️', 'D ♣️', 'K ♣️', 'A ♣️', '2 ♦️', '3 ♦️', '4 ♦️', '5 ♦️', '6 ♦️', '7 ♦️', '8 ♦️', '9 ♦️', '10 ♦️', 'B ♦️', 'D ♦️', 'K ♦️', 'A ♦️',
                     '2 ♠️', '3 ♠️', '4 ♠️', '5 ♠️', '6 ♠️', '7 ♠️', '8 ♠️', '9 ♠️', '10 ♠️', 'B ♠️', 'D ♠️', 'K ♠️', 'A ♠️']
            money = 100
            if arg is not None:
                money = int(arg)
          
            embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
            embed.set_author(name="Golden Doors Casino",
                             icon_url=client.link)
            embed.add_field(name="ㅤ", value=f"Wähle eine der dargestellten Optionen", inline=False)
          
            HelpButton = discord.ui.Button(label="Help", style=discord.enums.ButtonStyle.grey)
            StatsButton = discord.ui.Button(label="Stats", style=discord.enums.ButtonStyle.grey)
            PlayButton = discord.ui.Button(label="Play", style=discord.enums.ButtonStyle.green)
            JoinButton = discord.ui.Button(label="Runde Beitreten", style=discord.enums.ButtonStyle.green)
            BetButton = discord.ui.Button(label="Auf Spieler Wetten", style=discord.enums.ButtonStyle.blurple)
            GetButton = discord.ui.Button(label="Karte ziehen", style=discord.enums.ButtonStyle.green)
            DontButton = discord.ui.Button(label="Keine Karten mehr", style=discord.enums.ButtonStyle.red)
          
            async def callback(interaction: discord.Interaction):
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino",
                             icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Standart Einsatz | **{money} $**", inline=True)
                embed.add_field(name="ㅤ", value=f"Standart Gewinn | **{money * 2} $**", inline=True)
                embed.add_field(name="ㅤ", value=f"Runde starten | **Button: Play**", inline=False)
                embed.add_field(name="ㅤ", value=f"Stats einsehen | **Button: Stats**", inline=True)
                embed.add_field(name="ㅤ", value=f"Regelwerk | **...**", inline=False)
                view = discord.ui.View(timeout=120)
                view.add_item(StatsButton)
                view.add_item(PlayButton)
                await emb.edit(embed=embed, view=view)
              
            async def callback2(interaction: discord.Interaction):
                print(interaction.user)
                await interaction.response.send_message(f"Stats", ephemeral=True)
              
            async def callback3(interaction: discord.Interaction):
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Thread öffnen um der Runde beizutreten!", inline=True)
              
                view = discord.ui.View(timeout=120)
                await emb.edit(embed=embed, view=view)
              
                thread = await ctx.channel.create_thread(name="Blackjack", type=ChannelType.public_thread, auto_archive_duration=60)
              
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Mitspieler | ", inline=True)
              
                JoinButton.callback = callbackJoin
                view = discord.ui.View(timeout=120)
                view.add_item(JoinButton)
                view.add_item(BetButton)
                threadEmb = await thread.send(embed=embed, view=view)
              
                timeout = time.time() + 60*2
                while (True):
                    if time.time() > timeout or (len(blackjack_members) >= 3): #Spieleranzahl ändern
                        break
                    await asyncio.sleep(5)
                      
                if not blackjack_members:
                    await thread.delete()
                    return
                  
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Die Runde wurde bereits gestartet. Thread öffnen um zuzuschauen!", inline=True)
              
                view = discord.ui.View(timeout=120)
                await emb.edit(embed=embed, view=view)
              
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Herzlich Willkommen im **Golden Doors Casino**,\n Ich bin ihr heutiger Dealer {random.choice(client.dealer)} und"                                       " begrüße sie an diesem Tisch zu einer Runde Black Jack.", inline=True)
              
                view = discord.ui.View(timeout=120)
                await threadEmb.edit(embed=embed, view=view)
              
                await asyncio.sleep(5)
              
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Bitte ziehen sie Ihre Karten!", inline=True)
              
                GetButton.callback = callbackGet
                view = discord.ui.View(timeout=120)
                view.add_item(GetButton)
                await threadEmb.edit(embed=embed, view=view)

                nonlocal card_members, out_members, cards
              
                timeout = time.time() + 60*2
                while (True):
                    if (time.time() > timeout) or (len(card_members) == len(blackjack_members)):
                        break
                    await asyncio.sleep(5)
                      
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Alle haben ihre Karten bekommen!", inline=True)
              
                view = discord.ui.View(timeout=120)
                await threadEmb.edit(embed=embed, view=view)
              
                await asyncio.sleep(5)
              
                Dcards = random.choices(cards, k=2)
                summe = 0
                for card in Dcards:
                    cards.remove(card)
                    if card.split(" ")[0] in ["K","B","D"]:
                        summe += 10
                    elif card.split(" ")[0] == "A":
                        if summe + 11 > 21:
                            summe += 1
                        else:
                            summe += 11
                    else:
                        summe += int(card.split(" ")[0])
                      
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"**Dealer Karten [{summe}]\n{Dcards[0]}    {Dcards[1]}**", inline=True)
              
                await threadEmb.edit(embed=embed)
              
                await asyncio.sleep(5)

                while (True):
                    embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                    embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                    embed.add_field(name="ㅤ", value=f"Wählen sie aus ob sie noch eine weitere Karte ziehen möchten!", inline=True)
                  
                    DontButton.callback = callbackDont
                    view = discord.ui.View(timeout=120)
                    view.add_item(GetButton)
                    view.add_item(DontButton)
                    await threadEmb.edit(embed=embed, view=view)
                  
                    card_members = []
                    timeout = time.time() + 60*2
                    while (True):
                        if (time.time() > timeout) or (len(card_members) == len(blackjack_members) - len(out_members)):
                            break
                        await asyncio.sleep(5)
                          
                    embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                    embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                    embed.add_field(name="ㅤ", value=f"Alle haben ihre Karten bekommen!", inline=True)
                  
                    view = discord.ui.View(timeout=120)
                    await threadEmb.edit(embed=embed, view=view)
                  
                    await asyncio.sleep(5)
                  
                    if int(summe) < 18:
                        embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                        embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                        embed.add_field(name="ㅤ", value=f"Der Dealer zieht noch eine Karte!", inline=False)
                      
                        Dcard = random.choice(cards)
                        Dcards.append(Dcard)
                        cards.remove(Dcard)
                      
                        text2 = ""
                        summe = 0
                      
                        for Dcard in Dcards:
                            if Dcard.split(" ")[0] in ["K","B","D"]:
                                summe += 10
                            elif Dcard.split(" ")[0] == "A":
                                if summe + 11 > 21:
                                    summe += 1
                                else:
                                    summe += 11
                            else:
                                summe += int(Dcard.split(" ")[0])
                              
                            text2 += Dcard + "    "
                      
                        embed.add_field(name="ㅤ", value=f"**Dealer Karten [{summe}]\n{text2}**", inline=False)
                        await threadEmb.edit(embed=embed)
                        await asyncio.sleep(5)
                  
                    else:
                        embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                        embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                        embed.add_field(name="ㅤ", value=f"Der Dealer zieht keine weitere Karte!", inline=False)
                      
                        summe = 0
                        text2 = ""
                      
                        for Dcard in Dcards:
                            if Dcard.split(" ")[0] in ["K","B","A","D"]:
                                summe += 10
                            else:
                                summe += int(Dcard.split(" ")[0])
                            text2 += Dcard + "    "
                          
                        embed.add_field(name="ㅤ", value=f"**Dealer Karten [{summe}]\n{text2}**", inline=False)
                        await threadEmb.edit(embed=embed)
                      
                        await asyncio.sleep(5)
                      
                    if len(out_members) == len(blackjack_members):
                        break
                      
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"Keine weiteren Karten. Kommen wir zur Auflösung!", inline=False)
              
                await threadEmb.edit(embed=embed)
              
                await asyncio.sleep(3)
              
                pSumme = []
              
                for player in invCards:
                    x = 0
                  
                    for card in invCards[str(player)].split(":"):
                        if card == "": pass
                          
                        elif card.split(" ")[0] in ["K","B","A","D"]:
                            x += 10
                        else: x += int(card.split(" ")[0])
                          
                    pSumme.append(x)
                  
                if summe == 21:
                    embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                    embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                    embed.add_field(name="ㅤ", value=f"**Der Dealer** hat gewonnen mit einer Kartensumme von 21!", inline=False)
                  
                elif 21 >= max(pSumme) > summe :
                    embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                    embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                    embed.add_field(name="ㅤ", value=f"Der Spieler **{blackjack_members[pSumme.index(max(pSumme))]}** hat gewonnen mit einer Kartensumme von **{max(pSumme)}**!", inline=False)
                  
                else:
                    embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                    embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                    embed.add_field(name="ㅤ", value=f"**Der Dealer** hat gewonnen mit einer Kartensumme von **{summe}**!", inline=False)
                  
                await threadEmb.edit(embed=embed)
              
                client.queue[ctx.guild.id] = []
                  
            async def callbackDont(interaction: discord.Interaction):
                if not interaction.user.name in blackjack_members:
                    await interaction.response.send_message(f"**Du bist nicht teil dieser Runde!**", ephemeral=True)
                    return
                else:
                    await interaction.response.send_message(f"**Du ziehst keine weiteren Karten mehr!**", ephemeral=True)
                    out_members.append(interaction.user.name)
                  
            async def callbackGet(interaction: discord.Interaction):
                if not interaction.user.name in blackjack_members or out_members:
                    await interaction.response.send_message(f"**Du bist nicht teil dieser Runde!**", ephemeral=True)
                    return
                if interaction.user.name in card_members:
                    await interaction.response.send_message(f"**Du hast bereits deine Karten aufgedeckt!**", ephemeral=True)
                    return
                else:
                    nonlocal invCards, cards
                    summe = 0
                    if len(invCards[str(interaction.user.name)].split(":")) >= 2:
                        Pcard = random.choice(cards)
                        cards.remove(Pcard)
                        invCards[str(interaction.user.name)] += Pcard + ":"
                    else:
                        Pcards = random.choices(cards, k=2)
                        for Pcard in Pcards:
                            cards.remove(Pcard)
                            invCards[str(interaction.user.name)] += Pcard + ":"
                    text2 = ""
                    for invCard in invCards[str(interaction.user.name)].split(":"):
                        if invCard == "": pass
                        elif invCard.split(" ")[0] in ["K","B","A","D"]:
                            summe += 10
                        else:
                            summe += int(invCard.split(" ")[0])
                        text2 += invCard + "    "
                    text1 = "Deine Karten [" + str(summe)+ "]\n"
                    if summe > 21:
                        text2 += "\nDie Summe deiner Karten liegt leider über 21 und damit bist du ausgeschieden!"
                        out_members.append(interaction.user.name)
                        await interaction.response.send_message(f"**{text1}{text2}**", ephemeral=True)
                        return
                    await interaction.response.send_message(f"**{text1}{text2}**", ephemeral=True)
                    card_members.append(interaction.user.name)
                  
            async def callbackJoin(interaction: discord.Interaction):
                if interaction.user in client.queue[interaction.guild_id] or interaction.user.name in blackjack_members:
                    await interaction.response.send_message(f"**Warte bis deine vorherige Runde beendet wurde!**", ephemeral=True)
                    return
                isInKonto = await isKonto(ctx, interaction.user, money)
                if isInKonto:
                    blackjack_members.append(interaction.user.name)
                    await removeMoney(ctx, interaction.user, money)
                    client.queue[interaction.guild_id].append(interaction.user)
                    nonlocal invCards
                    invCards[str(interaction.user.name)] = ""
                else:
                    await interaction.response.send_message("Du besitzt noch kein Konto oder hast nicht genug Geld. Infos in **#Bank**")
                    return
                embeds = interaction.message.embeds
                for embed in embeds:
                    for field in embed.fields:            
                        text = str(field.value)                        
                embed = discord.Embed(title=f"Blackjack | User: {ctx.author}", description=" ")
                embed.set_author(name="Golden Doors Casino", icon_url=client.link)
                embed.add_field(name="ㅤ", value=f"{text} **{interaction.user.name}**,", inline=True)
                await interaction.message.edit(embed=embed)
                return
              
            HelpButton.callback, StatsButton.callback, PlayButton.callback = callback, callback2, callback3
        
            view = discord.ui.View(timeout=120)
            view.add_item(HelpButton)
            view.add_item(StatsButton)
            view.add_item(PlayButton)
          
            emb = await ctx.send(embed=embed, view=view)
            return
  
@client.event
async def on_message(message):
    if message.channel.id == 730913242024640604:
        if message.author == client.user:
            return
        else:
            if client.counter == 0:
                try:
                    client.counter = int(message.content)
                except:
                    await message.delete()
                    await logs(message.author, "User hat kein korrektes Argument in #Counter geschickt!")
                    return
            else:
                try:
                    msg = int(message.content)
                except:
                    await message.delete()
                    await logs(message.author, "User hat kein korrektes Argument in #Counter geschickt!")
                    return
                if int(message.content) == int(client.counter) + 1:
                    client.counter = int(message.content)
                else:
                    await message.delete()
                    await logs(message.author, "User hat kein korrektes Argument in #Counter geschickt!")
    elif message.channel.id == 956289591671943178:
        if message.author == client.user:
            return
        
        else:
            server = message.guild.id
            with open('oneword.txt', 'r') as f:
                storys = json.load(f)

            try:
                storys[str(server)]
            except:
                storys[str(server)] = {}
                storys[str(server)]['story'] = ""
                storys[str(server)]['storyid'] = "" 
          
            client.story = storys[str(server)]['story'] 
            client.storyid = storys[str(server)]['storyid']
          
            if (client.story == "") and (message.content.lower() == "$story start") :
                embed = discord.Embed(title="**One-Word-Story**", colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="Die Story wurde gestartet! In diesem Kanal kannst Du mit anderen Benutzern Geschichten erstellen, indem ihr einen Satz Wort für Wort schreibt. Eine Nachricht darf nur ein Wort enthalten und die Nutzer müssen sich beim Schreiben abwechseln.")
                embed.add_field(name="ㅤ",
                            value="**...**", inline=False)
                
                story = await message.channel.send(embed=embed)
                client.storyid = story.id
            elif (client.story != "") and (message.content.lower() == "$story ende") :
                def isText(msg):
                    return True
          
                embed = discord.Embed(title="**One-Word-Story**", colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="Diese Geschichte wurde beendet. Gebe der Geschichte noch einen Namen:")
                embed.add_field(name="ㅤ",
                            value=f"**{client.story}**", inline=False)
                
                story = await message.channel.send(embed=embed)
                client.storyid = ""
                client.storyauthor = "" 
                client.story = ""
            elif (str(message.author) != client.storyauthor) and (client.storyid != ""): 
                if client.story != "":
                    channel = client.get_channel(message.channel.id)
                    client.story = client.story + " " + message.content
                    try:
                        msg = await channel.fetch_message(client.storyid)
                        await msg.delete()
                    except:
                        async for msg in message.channel.history(limit=10000):
                            if msg.embeds:
                                embeds = msg.embeds
                                for embed in embeds:
                                    for field in embed.fields:
                                        text = str(field.value)
                                        text = text[:-2]
                                        text = text[2:]
                                        client.story = text + " " + message.content
                                break
                
                embed = discord.Embed(title="**One-Word-Story**", colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="Diese Geschichte wurde bisher geschrieben:")
                embed.add_field(name="ㅤ",
                            value=f"**{client.story}**", inline=False)
                
                story =  await message.channel.send(embed=embed)
                client.storyauthor = str(message.author)
                client.storyid = story.id
            elif (str(message.author) == client.storyauthor) and (client.storyid != ""):
                if client.story != "":
                    channel = client.get_channel(message.channel.id)
                    client.story = client.story + " " + message.content
                    try:
                        msg = await channel.fetch_message(client.storyid)
                        await msg.delete()
                    except:
                        async for msg in message.channel.history(limit=10000):
                            if msg.embeds:
                                embeds = msg.embeds
                                for embed in embeds:
                                    for field in embed.fields:
                                        text = str(field.value)
                                        text = text[:-2]
                                        text = text[2:]
                                        client.story = text
                                        await msg.delete()
                                        break
                                break
                              
                embed = discord.Embed(title="**One-Word-Story**", colour=0xff00f6,
                                      url="https://www.Youtube.com",
                                      description="Jemand anderes muss die Geschichte fortsetzen! Dein Wort wird nicht hinzugefügt:")
                embed.add_field(name="ㅤ",
                            value=f"**{client.story}**", inline=False)
                
                story =  await message.channel.send(embed=embed)
                client.storyid = story.id
            storys[str(server)]['story'] = client.story
            storys[str(server)]['storyid'] = client.storyid
            with open('oneword.txt', 'w') as f:
                json.dump(storys, f)
    else:
        await client.process_commands(message)


#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandNotFound):
#        pass
#    elif isinstance(error, commands.MessageNotFound):
#        pass
#    else:
#        pass

token = os.environ['Token']

keep_alive.keep_alive()
client.run(token)
