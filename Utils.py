import Config, discord, datetime

async def modlog(guild : discord.Guild, title : str, description : str):
    """Send a modlog to the guilds's modlog channel if it exists.

    Args:
        guild (discord.Guild): A guild object.
        title (str): The title that should be put on the embed.
        description (str): The description that should be put on the embed.
    """
    document = Config.CLUSTER["servers"]["modlogs"].find_one({"_id": guild.id})
    if document != None:
        channel = discord.utils.get(guild.text_channels, id = document["channel"])
        if channel != None:
            embed = discord.Embed(
                title = title,
                description = description,
                color = Config.MAINCOLOR
            )
            await channel.send(embed = embed)