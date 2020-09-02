import discord
from discord.ext import commands
import Config

class HelpCommand(commands.HelpCommand):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.verify_checks = False
		self.failure = "<:RedTick:690059875337764865>"
		self.success = "<:GreenTick:690059820300369959>"

	async def command_callback(self, ctx, *, command=None):
		await self.prepare_help_command(ctx, command)
		bot = ctx.bot

		if command is None:
			mapping = self.get_bot_mapping()
			return await self.send_bot_help(mapping)

		cog = bot.get_cog(command.lower())
		if cog is not None:
			return await self.send_cog_help(cog)

		maybe_coro = discord.utils.maybe_coroutine

		keys = command.split(' ')
		cmd = bot.all_commands.get(keys[0])
		if cmd is None:
			string = await maybe_coro(self.command_not_found, self.remove_mentions(keys[0]))
			return await self.send_error_message(string)

		for key in keys[1:]:
			try:
				found = cmd.all_commands.get(key)
			except AttributeError:
				string = await maybe_coro(self.subcommand_not_found, cmd, self.remove_mentions(key))
				return await self.send_error_message(string)
			else:
				if found is None:
					string = await maybe_coro(self.subcommand_not_found, cmd, self.remove_mentions(key))
					return await self.send_error_message(string)
				cmd = found

		if isinstance(cmd, commands.Group):
			return await self.send_group_help(cmd)
		else:
			return await self.send_command_help(cmd)

	async def send_bot_help(self, mapping):
		await self.context.trigger_typing()
		prefix = self.context.prefix
		embed=discord.Embed(description=f"Hello **{self.context.author.name}**, I heard you needed some help with me? Well, you've ran the correct command in order to get help. If you do the follow commands listed down below you will be successful with getting help from my help menu. If you still cannot get the help you needed from my help menu, please feel free to [Join the Support Server](https://discord.gg/Q27U4pZ) and ask all your questions.", color=Config.MAINCOLOR)
		embed.set_author(name=f"Welcome to {self.context.bot.user.name} [{len(self.context.bot.commands):,d}]", icon_url=self.context.bot.user.avatar_url_as(static_format="png"))
		embed.add_field(name=f"**🎉 Giveaways [{len(set(self.context.bot.cogs['misc'].walk_commands()))}]**", value=f"`{prefix}help giveaways`", inline=True)
		embed.add_field(name=f"**💠 Important Information**", value=f"**+**This is the [`Official Invite Link`](https://discordapp.com/api/oauth2/authorize?client_id={self.context.bot.user.id}&permissions=8&scope=bot) to invite Astro to your server. \n**+**This is the [`Official Discord Link`](https://discord.gg/Q27U4pZ) to the Astro support server. \n**+**This is the [`Official Vote Page`](https://top.gg/bot/{self.context.bot.user.id}/vote) for Astro on [top.gg](https://top.gg/{self.context.bot.user.id}). \n\nIf you are having issues [Join the Support Server](https://discord.gg/XkrsPHh) Server you can use the command `{prefix}help (command)` to get more help. Note that it only gives you a little information.", inline=False)
		await self.context.send(embed=embed)

	async def send_command_help(self, command):
		await self.context.trigger_typing()
		prefix = self.context.prefix

		embed = discord.Embed(color=Config.MAINCOLOR, description=f"{command.help if command.help else self.no_brief()}")
		embed.set_author(name=f"{command.name.title()} Command • {command.cog.qualified_name.title()} Category", icon_url=self.context.bot.user.avatar_url_as(static_format="png"))
		embed.add_field(name=f"Aliases", value=f"{prefix}{f'**,** {prefix}'.join(command.aliases)}" if command.aliases != [] else "None to be Found.")
		embed.add_field(name=f"Usage", value=f"Please do `{prefix}{command.name}{command.usage if command.usage else ''}`")
		await self.context.send(embed=embed)

	async def send_group_help(self, group):
		await self.context.trigger_typing()
		prefix = self.context.prefix

		embed = discord.Embed(color=Config.MAINCOLOR, description=f"{group.brief if group.brief else self.no_brief()}")
		embed.set_author(name=f"{group.name.title()} Command • {group.cog.qualified_name} Category", icon_url=self.context.bot.user.avatar_url_as(static_format="png"))
		embed.add_field(name=f"{group.name.title()} Alias", value=f"{prefix}{f', {prefix}'.join(group.aliases)}" if group.aliases != [] else "None to be Found.")
		embed.add_field(name=f"{group.name.title()} Usage", value=f"Please do `{prefix}{group.name} <{'|'.join([c.name for c in group.commands])}>`")
		embed.add_field(name=f"{group.name.title()} Subcommands", value="**,** ".join([f'`{c.name}`' for c in group.commands]))
		await self.context.send(embed=embed)

	def no_brief(self):
		return "No description has been provided"

	async def send_cog_help(self, cog):
		await self.context.trigger_typing()
		prefix = self.context.prefix

		commands = '`**,** `'.join([c.qualified_name for c in cog.get_commands()])
		embed = discord.Embed(description=f"`{commands}`", color=Config.MAINCOLOR)
		embed.set_author(name=f"{cog.qualified_name.title()} Commands [{len(set(self.context.bot.cogs[f'{cog.qualified_name.lower()}'].walk_commands()))}]", icon_url=self.context.bot.user.avatar_url_as(static_format="png"))
		await self.context.send(embed=embed)

def setup(bot):
	bot.help_command = HelpCommand()
