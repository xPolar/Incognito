# Imports
## Libraries that are already part of Python.
import typing
## Libraries that must be installed with pip
import discord
from discord.ext import commands
## Files on this machine
import Config, Utils


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def modlog(self, ctx, channel : typing.Union[ discord.TextChannel, str ] = None):
        if channel == None:
            embed = discord.Embed(
                title = "Empty Argument",
                description = "Please provide a channel or say `remove` to remove the current modlog channel!",
                color = Config.ERRORCOLOR
            )
        else:
            if isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    title = "Modlog Channel Updated",
                    description = f"Modlogs will now be sent to `{channel}`!",
                    color = Config.MAINCOLOR
                )
                Config.CLUSTER["servers"]["modlogs"].update_one({"_id": ctx.guild.id}, {"$set": {"channel": channel.id}}, upsert = True)
            elif isinstance(channel, str) and ( channel.lower() == "reset" or channel.lower() == "remove" ):
                embed = discord.Embed(
                    title = "Modlog Channel Updated",
                    description = "Modlogs will no longer be sent anywhere!",
                    color = Config.MAINCOLOR
                )
                Config.CLUSTER["servers"]["modlogs"].delete_one({"_id": ctx.guild.id})
        await ctx.send(embed = embed)
    
    @modlog.error
    async def modlog_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You need the **Manage Server** permission to set this server's modlog!",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        elif isinstance(error, commands.BadUnionArgument):
            embed = discord.Embed(
                title = "Empty Argument",
                description = "Please provide a valid channel or say `remove` to remove the current modlog channel!",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
                        
def setup(bot):
    bot.add_cog(Moderation(bot))
