import re
import api
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
  intents=intents,
	command_prefix="sk!"
)

warns_list = {}

@bot.event 
async def on_ready(): 
    print("Bot is Online")
    for guild in bot.guilds:
        for member in guild.members:
          if member.id not in warns_list:
            warns_list[str(member.id)] = 0
    print(warns_list)

@bot.command(name = 'warns', help = 'To fetch the number of warns a user has got.')
async def warns(ctx, member: discord.Member):
  if ctx.message.author.guild_permissions.administrator:
    await ctx.channel.send("<@!" + str(member.id) + "> has " + str(warns_list[str(member.id)]) + " warns.")
  else:
    await ctx.channel.send("You are not authorized to use this command")

@bot.command(name = 'removewarns', help = 'To remove the warns for a user.')
async def removewarns(ctx, member: discord.Member):
  if ctx.message.author.guild_permissions.administrator:
    warns_list[str(member.id)] = 0
    await ctx.channel.send("Warns for <@!" + str(member.id) + "> removed.")
  else:
    await ctx.channel.send("You are not authorized to use this command")
  

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('sk!'):
        res = None
    else:
        res = api.api_response(text= message.content)
    print(res)
    print(message.content)
    if res != None:
        warns_list[str(message.author.id)] += 1
        rem = 5 - warns_list[str(message.author.id)]
        await message.delete()
        if rem > 0:
            await message.channel.send(message.author.mention + " You are warned because your last message contained **" + res + "** related content. \nThe total number of warns you have are " + str(5-rem) + ". \nYou have " + str(rem) + " remaining warns.")
        else:
            reason = "You have received 5 warnings till now, you can no longer be part of the server so as to maintain the safe environment of the server."
            await message.author.kick(reason=reason)
            await message.author.dm_channel.send(reason)
            await message.channel.send(message.author.mention + " was kicked due to reaching the warning limit.")
    await bot.process_commands(message)


token = os.getenv('DISCORD_BOT_SECRET')
bot.run(token)