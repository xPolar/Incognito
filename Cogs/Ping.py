# Imports
## Libraries that must be installed with pip
from colorama import Style, Fore
import discord, time
from discord.ext import commands
## Files on this machine
import Config

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["latency"])
    async def ping(self, ctx):
        """
        Get the latency between our bot and Discord as well as the latency on our server.
        """
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(
            title = "🏓 Pong!",
            description = f"API latency is { round((t2 - t1) * 1000) }ms\nHost latency is { int(round(self.bot.latency * 1000, 2)) }ms",
            color = Config.MAINCOLOR
        )
        if (round((t2 - t1) * 1000) > 500) or (round(self.bot.latency * 1000, 2) > 500):
            print()
            print(f"{Style.BRIGHT}{Fore.RED}[WARNING]{Fore.WHITE} API latency is { round((t2 - t1) * 1000) }ms & host latency is { int(round(self.bot.latency * 1000, 2)) }ms")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Misc(bot))