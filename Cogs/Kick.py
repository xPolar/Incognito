# Imports
## Libraries that must be installed with pip
import discord
from discord.ext import commands
## Files on this machine
import Config, Utils

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, to_kick : commands.Greedy[discord.Member] = None, reason = None):
        """
        Kick a list of members from the server.
        """
        if to_kick == None:
            embed = discord.Embed(
                title = "Empty Argument",
                description = "Please provide a member to kick!",
                color = Config.ERRORCOLOR
            )
        else:
            kicked_list = []
            for member in to_kick:
                try:
                    await member.kick() if reason == None else await member.kick(reason = reason)
                except discord.Forbidden:
                    continue
                else:
                    kicked_list.append(member)
            if len(kicked_list) == 0:
                embed = discord.Embed(
                    title = "Missing Permissions",
                    description = f"I was not able to kick anyone because they either have the same or a higher role then me!",
                    color = Config.ERRORCOLOR
                )
            elif len(kicked_list) == 1:
                embed = discord.Embed(
                    title = "Member Kicked",
                    description = f"I have kicked {kicked_list[0]}{ f' for: {reason}' if reason != None else '!' }",
                    color = Config.MAINCOLOR
                )
                await Utils.modlog(ctx.guild, "Member Kicked", f"`{kicked_list[0]}` was kicked by `{ctx.author}`{ f' for: {reason}' if reason != None else '!' }")
            else:
                embed = discord.Embed(
                    title = "Members Kicked",
                    description = f"I have kicked {len(kicked_list)} members{ f' for: {reason}' if reason != None else '!' }",
                    color = Config.MAINCOLOR
                )
                await Utils.modlog(ctx.guild, "Members Kicked", f"**{len(kicked_list)}** members were kicked by `{ctx.author}`{ f' for: {reason}' if reason != None else '!' }")
        await ctx.send(embed = embed)
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You need the **Kick Members** permission to kick members!",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "I need the **Kick Members** permission to kick members!",
                color = Config.ERRORCOLOR
            )
            await ctx.send(embed = embed)
                        
def setup(bot):
    bot.add_cog(Moderation(bot))