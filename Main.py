# Imports
## Default libraries on Python
import sys, traceback
from datetime import datetime
from itertools import cycle
## Libraries that need to be installed with pip
from colorama import Style, Fore
import discord, aiohttp
from discord.ext import commands, tasks
## Files on this machine
import Config

def get_prefix(ctx):
    """Retrive document from database and return the stored prefix if it exists, if not return the default prefix.

    Args:
        ctx (context): discord.py's context object

    Returns:
        str: The prefix that will be returned.
    """
    if ctx.guild == None:
        return Config.PREFIX
    else:
        document = Config.CLUSTER["servers"]["prefixes"].find_one({"_id": ctx.guild.id})
        return document["prefix"] if document != None else Config.PREFIX
    
bot = commands.AutoShardedBot(command_prefix = "$", case_insensitive = True)

# All of the cogs within the bot that we want to load
COGS = ["Ping"]

# Loads all of our cogs
for COG in COGS:
    bot.load_extension(f"Cogs.{COG}")
    print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Loaded Cogs.{COG}")

async def owner(ctx):
    return ctx.author.id in Config.OWNER_IDS

@bot.command()
@commands.check(owner)
async def restart(ctx):
    """
    Restart the bot's cogs.
    """
    print()
    for COG in COGS:
        bot.reload_extension(f"Cogs.{COG}")
        print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Reloaded Cogs.{COG}")
    embed = discord.Embed(
        title = "Bot Restarted",
        description = "All cogs have been reloaded!",
        color = Config.MAINCOLOR
    )
    await ctx.send(embed = embed)
    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-RESTARTED]{Fore.WHITE} Restart by {ctx.author} - {ctx.author.id}, I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadArgument):
        return
    elif isinstance(error, commands.CheckFailure):
        return
    elif isinstance(error, commands.BadUnionArgument):
        return
    else:
        try:
            embed = discord.Embed(
                    title = "Error",
                    description = f"**```\n{error}\n```**",
                    color = Config.ERRORCOLOR
            )
            embed.set_footer(text = "Please report this to Polar#6880")
            await ctx.send(embed = embed)
        finally:
            raise error

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title = "Joined a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0x77DD77
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner", value = f"{guild.owner.name}#{guild.owner.discriminator}")
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(Config.WEBHOOK, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Joined a server")

@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
        title = "Left a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0xFF6961
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner", value = f"{guild.owner.name}#{guild.owner.discriminator}")
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(Config.WEBHOOK, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Left a server")

@bot.event
async def on_shard_ready(shard_id):
    print(f"{Style.BRIGHT}{Fore.CYAN}[SHARD-STARTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has started!")

@bot.event
async def on_ready():
    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-STARTED]{Fore.WHITE} I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(f"with {Config.PREFIX}help"))

bot.run(Config.TOKEN)