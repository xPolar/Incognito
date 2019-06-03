#Imports
from datetime import datetime
import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
import random
import sys
import traceback

#Values
linecount = "1515"
commandcount = ""
blocked_users = [563395266799992843]

#Sets bot prefix to !
client = commands.Bot(command_prefix = "$", case_insensitive = True)

client.launch_time = datetime.utcnow()

#Removes the default help command
client.remove_command("help")

#Check current servers
@client.command()
async def servers(ctx):
    if ctx.message.author.id == 229695200082132993:
        await ctx.send(f"{client.guilds}")

#Purge command
@client.command(aliases = ["clear"])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 10):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        max_purge = 500
        if amount != 1:
            if amount < max_purge:
                embed1 = discord.Embed(
                    title = f"Purged {amount} message(s)",
                    color = 0x00cc1b
                )
                await ctx.channel.purge(limit=amount+1)
                await ctx.send(embed=embed1, delete_after = 4.0)
            if amount == max_purge:
                embed1 = discord.Embed(
                    title = f"Purged {amount} message(s)",
                    color = 0x00cc1b
                )
                await ctx.channel.purge(limit=amount+1)
                await ctx.send(embed=embed1, delete_after = 4.0)
            if amount > max_purge:
                embed2 = discord.Embed(
                    title = f"You can only purge a max of 500 messages!",
                    color = 0xdd0000
                )
                await ctx.send(embed=embed2, delete_after = 4.0)
                await ctx.message.delete()
        else:
                embed1 = discord.Embed(
                    title = f"Purged {amount} message",
                    color = 0x00cc1b
                )
                await ctx.channel.purge(limit=amount+1)
                await ctx.send(embed=embed1, delete_after = 4.0)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "You are missing the **Manage Messages(s)** permission!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed, delete_after = 4.0)
        await ctx.message.delete()

#Kick command
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member = None, *, reason = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            embed = discord.Embed(
                title = "Please specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed=embed, delete_after = 4.0)
            await ctx.message.delete()
        if ctx.author.id != member.id:
            if reason != None:
                embed = discord.Embed(
                    description = f"{member.mention} has been kicked!",
                    color = 0x00cc1b
                )
                await member.kick(reason=f"{ctx.message.author.name}#{ctx.message.author.discriminator}:No reason has been provided.")
                await ctx.send(embed=embed)
                await ctx.message.delete()
            else:
                embed = discord.Embed(
                    description = f"{member.mention} has been kicked for {reason}!",
                    color = 0x00cc1b
                )
                await member.kick(reason=f"{ctx.message.author.name}#{ctx.message.author.discriminator}:{reason}")
                await ctx.send(embed=embed)
                await ctx.message.delete()
        else:
            embed = discord.Embed(
                title = "You can't kick yourself!",
                color = 0xdd0000
            )
            await ctx.send(embed=embed, delete_after = 4.0)
            await ctx.message.delete()

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "You are missing the **Kick Members** permission!",
            color = 0xdd0000
        )
        await ctx.send(embed=embed, delete_after = 4.0)
        await ctx.message.delete()

#Ban command
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member = None, reason = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            embed = discord.Embed(
                title = "Please specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed=embed, delete_after = 4.0)
            await ctx.message.delete()
        if ctx.author.id != member.id:
            if reason == None:
                embed = discord.Embed(
                    description = f"{member.mention} has been banned!!",
                    color = 0x00cc1b
                )
                await member.ban(reason=f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}\nRulebreaker - {member.name}#{member.discriminator}\nReason - No reason has been provided.")
                await ctx.send(embed=embed)
                await ctx.message.delete()
            else:
                embed = discord.Embed(
                    description = f"{member.mention} has been banned!",
                    color = 0x00cc1b
                )
                await member.ban(reason=f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}\nRulebreaker - {member.name}#{member.discriminator}\nReason - {reason}")
                await ctx.send(embed=embed)
                await ctx.message.delete()
        else:
            embed = discord.Embed(
                title = "You can't ban yourself!",
                color = 0xdd0000
            )
            await ctx.send(embed=embed, delete_after = 4.0)
            await ctx.message.delete()

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "You are missing the **Ban Members** permission!",
            color = 0xdd0000
        )
        await ctx.send(embed=embed, delete_after = 4.0)
        await ctx.message.delete()

#Unban command
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        banned_users = await ctx.guild.bans()
        if member == None:
            embed = discord.Embed(
                title = "Please specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed=embed, delete_after = 4.0)
            await ctx.message.delete()
        else:
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    embed = discord.Embed(
                        title = f"Unbanned {user.name}#{user.discriminator}",
                        color = 0x00cc1b
                    )
                    await ctx.guild.unban(user)
                    await ctx.send(embed=embed)
                    await ctx.message.delete()
                    return
            embed = discord.Embed(
                title = "That user is not banned!",
                color = 0xdd0000
            )
            await ctx.send(embed=embed, delete_after = 4.0)
            await ctx.message.delete()

@unban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "You are missing the **Ban Members** permission!",
            color = 0xdd0000
        )
        await ctx.send(embed=embed, delete_after = 4.0)
        await ctx.message.delete()

#Update channels for mute
@client.command()
@commands.has_permissions(manage_guild = True)
async def channelupdate(ctx, *, role: discord.Role = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if role == None:
            embed = discord.Embed(
            title = "Please specify a role!",
            color = 0xdd0000
            )
            await ctx.send(embed = embed)
        else:
            for channel in ctx.message.guild.text_channels:
                await channel.set_permissions(role, send_messages = False)
                embed = discord.Embed(
                    title = f"{channel.name} has been updated!",
                    color = 0x00cc1b
                )
                await ctx.send(embed = embed, delete_after = 4.0)

#Mute command
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, *, member: discord.Member = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member.id != ctx.message.author.id:
            if member == None:
                embed = discord.Embed(
                    title = "Please specify a user!",
                    color = 0xdd0000
                )
                await ctx.send(embed = embed, delete_after  = 4.0)
                await ctx.message.delete()
                return
            else:
                    role = discord.utils.get(ctx.guild.roles, name = "Muted")
                    await member.add_roles(role)
                    embed = discord.Embed(
                        description = f"{member.mention} has been muted!",
                        color = 0x00cc1b
                    )
                    await ctx.send(embed = embed)
                    await ctx.message.delete()
                    return
        else:
            embed = discord.Ember(
                title  = "You can't mute yourself!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)
            await ctx.message.delete()

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "You are missing the **Manage Role(s)** permission!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
        await ctx.message.delete()

#Unmute command
@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, *, member: discord.Member = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            embed = discord.Embed(
                title = "Please specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)
            return
        if member != None:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(role)
            embed = discord.Embed(
                description = f"{member.mention} has been unmuted!",
                color = 0x00cc1b
            )
            await ctx.send(embed = embed)

@mute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "You are missing the **Manage Role(s)** permission!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
        await ctx.message.delete()

#Dadjoke command
@client.command()
async def dadjoke(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        jokes = ["Did you hear about the restaurant on the moon? Great food, no atmosphere.",
                "What do you call a fake noodle? An Impasta.",
                "How many apples grow on a tree? All of them.",
                "Want to hear a joke about paper? Nevermind it's tearable.",
                "I just watched a program about beavers. It was the best dam program I've ever seen.",
                "Why did the coffee file a police report? It got mugged.",
                "How does a penguin build it's house? Igloos it together.",
                "Dad, did you get a haircut? No I got them all cut.",
                "What do you call a Mexican who has lost his car? Carlos.",
                "Dad, can you put my shoes on? No, I don't think they'll fit me.",
                "Why did the scarecrow win an award? Because he was outstanding in his field.",
                "Why don't skeletons ever go trick or treating? Because they have no body to go with.",
                "Ill call you later. Don't call me later, call me Dad.",
                "What do you call an elephant that doesn't matter? An irrelephant.",
                "Want to hear a joke about construction? I'm still working on it.",
                "What do you call cheese that isn't yours? Nacho Cheese.",
                "Why couldn't the bicycle stand up by itself? It was two tired.",
                "What did the grape do when he got stepped on? He let out a little wine.",
                "I wouldn't buy anything with velcro. It's a total rip-off.",
                "The shovel was a ground-breaking invention.",
                "Dad, can you put the cat out? I didn't know it was on fire.",
                "This graveyard looks overcrowded. People must be dying to get in there.",
                "Whenever the cashier at the grocery store asks my dad if he would like the milk in a bag he replies, 'No, just leave it in the carton!'",
                "5/4 of people admit that they’re bad with fractions.",
                "Two goldfish are in a tank. One says to the other, 'do you know how to drive this thing?'",
                "What do you call a man with a rubber toe? Roberto.",
                "What do you call a fat psychic? A four-chin teller.",
                "I would avoid the sushi if I was you. It’s a little fishy.",
                "To the man in the wheelchair that stole my camouflage jacket... You can hide but you can't run.",
                "The rotation of earth really makes my day.",
                "I thought about going on an all-almond diet. But that's just nuts.",
                "What's brown and sticky? A stick.",
                "I’ve never gone to a gun range before. I decided to give it a shot!",
                "Why do you never see elephants hiding in trees? Because they're so good at it.",
                "Did you hear about the kidnapping at school? It's fine, he woke up.",
                "A furniture store keeps calling me. All I wanted was one night stand.",
                "I used to work in a shoe recycling shop. It was sole destroying.",
                "Did I tell you the time I fell in love during a backflip? I was heels over head.",
                "I don’t play soccer because I enjoy the sport. I’m just doing it for kicks.",
                "People don’t like having to bend over to get their drinks. We really need to raise the bar."]
        embed = discord.Embed(
            title = "Here's a dad joke!",
            description = f"{random.choice(jokes)}",
            color = 0x5627d8
        )
        embed.set_author(name = "Dad joke")
        await ctx.send(embed = embed)

#Eightball command
@client.command(aliases = ["eightball", "8ball"])
async def eball(ctx, *, question):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        embed = discord.Embed(
            color = 0x2f302f
        )
        embed.set_author(name = "Eightball", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/581649634561097733/ball-pool-png-open-2000.png")
        embed.add_field(name = "Question", value = f"{question} ", inline = True)
        embed.add_field(name = "Answer", value = f"{random.choice(responses)}", inline = False)
        await ctx.send(embed=embed)

#Funfact command
@client.command()
async def funfact(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        funfacts = [f"This bot currently has {linecount} lines of code.",
                    "There are currently 18 useable commands for this bot.",
                    "The beta of this bot was made in about 2-3 days with little to no understanding of discord.py (The coding language used for this bot).",
                    "This bot is coded in discord.py.",
                    "December 12th, 2012 was the last day that the date, month, and year were the same number for the 21st century. (12/12/12)",
                    "Banging your head against a wall for one hour burns 150 calories.",
                    "In Switzerland it is illegal to own just one guinea pig.",
                    "Pteronophobia is the fear of being tickled by feathers.",
                    "A flock of crows is known as a murder.",
                    "The oldest “your mom” joke was discovered on a 3,500 year old Babylonian tablet.",
                    "29th May is officially “Put a Pillow on Your Fridge Day”.",
                    "Cherophobia is an irrational fear of fun or happiness.",
                    "7 percent of American adults believe that chocolate milk comes from brown cows.",
                    "If you lift a kangaroo’s tail off the ground it can’t hop.",
                    "Bananas are curved because they grow towards the sun.",
                    "Billy goats urinate on their own heads to smell more attractive to females.",
                    "The inventor of the Frisbee was cremated and made into a Frisbee after he died.",
                    "During your lifetime, you will produce enough saliva to fill two swimming pools.",
                    "Polar bears could eat as many as 86 penguins in a single sitting…",
                    "King Henry VIII slept with a gigantic axe beside him.",
                    "An eagle can kill a young deer and fly away with it.",
                    "In 2017 more people were killed from injuries caused by taking a selfie than by shark attacks.",
                    "A lion’s roar can be heard from 5 miles away.",
                    "Approximately 10-20 percent of U.S. power outages are caused by squirrels.",
                    "While trying to find a cure for AIDS, the Mayo Clinic made glow in the dark cats.",
                    "A swarm of 20,000 bees followed a car for two days because their queen was stuck inside.",
                    "J.K. Rowling chose the unusual name ‘Hermione’ so young girls wouldn’t be teased for being nerdy.",
                    "Los Angeles’s full name is 'El Pueblo de Nuestra Senora la Reina de los Angeles de Porciuncula.",
                    "It snowed in the Sahara desert for 30 minutes on the 18th February 1979.",
                    "Mike Tyson once offered a zoo attendant 10,000 dollars to let him fight a gorilla.",
                    "ABBA turned down 1 billion dollars to do a reunion tour.",
                    "There has never been a verified snow leopard attack on a human being.",
                    "The first alarm clock could only ring at 4 a.m.",
                    "Dying is illegal in the Houses of Parliaments.",
                    "The most venomous jellyfish in the world is the Irukandji.",
                    "The 20th of March is Snowman Burning Day.",
                    "Vincent van Gogh only sold one painting in his lifetime.",
                    "The average person walks the equivalent of five times around the world in their lifetime.",
                    "Michael Jackson offered to make a Harry Potter musical, but J.K. Rowling rejected the idea.",
                    "The world record for stuffing drinking straws into your mouth at once is 459.",
                    "In 2011, more than 1 in 3 divorce filings in the U.S. contained the word 'Facebook'.",
                    "George W. Bush was once a cheerleader.",
                    "Coca-Cola owns all website URLs that can be read as ahh, all the way up to 62 h’s.",
                    "Samuel L. Jackson requested to have a purple lightsaber in Star Wars in order for him to accept the part as Mace Windu.",
                    "Kleenex tissues were originally used as filters in gas masks.",
                    "In 1998, Sony accidentally sold 700,000 camcorders that had the technology to see through people’s clothes.",
                    "During your lifetime, you will spend around thirty-eight days brushing your teeth.",
                    "Ketchup was a medicine in the early 1800s.",
                    "The Longest Wedding Veil Was the Same Length as 63.5 Football Fields.",
                    "The Total Weight of Ants on Earth Once Equaled the Total Weight of People.",
                    "A Dozen Bodies Were Found in Benjamin Franklin’s Basement.",
                    "Chinese Police Use Geese Squads.",
                    "For 100 Years, Maps Have Shown an Island That Doesn’t Exist.",
                    ]

        embed = discord.Embed(
            title = "Here's a funfact!",
            description = f"{random.choice(funfacts)}",
            color = 0x9b037d
        )
        embed.set_author(name = "Fun fact")
        await ctx.send(embed=embed)

#Cat command
@client.command()
async def cat(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        choices = ["http://i.imgur.com/vTbe1VL.jpg",
                  "https://i.redd.it/5a2b5t3zv6zx.jpg",
                  "https://i.reddituploads.com/beb4181f5ad54ea396a4c16f48dda6a1?fit=max&h=1536&w=1536&s=d6725e107cac20a2d63c17ceed41cadc",
                  "http://i.imgur.com/54ZNGsq.jpg",
                  "http://i.imgur.com/avo5CE2.gifv",
                  "https://i.imgur.com/74oEb8a.jpg",
                  "https://i.imgur.com/mUm8RkG.jpg",
                  "https://i.reddituploads.com/21738376035841e8a435a7aa1781f1a2?fit=max&h=1536&w=1536&s=b30153a27838ee69dbfbf6b6a53952b6",
                  "http://i.imgur.com/729sGVJ.gifv",
                  "https://i.redd.it/hpqurtsrb6qy.jpg",
                  "http://i.imgur.com/GyEeYt8.gifv",
                  "http://i.imgur.com/OlTgWUD.jpg",
                  "https://i.redd.it/hzxejchmn9yy.jpg",
                  "https://i.redd.it/lslm1romx5jy.jpg",
                  "https://i.redd.it/x3kdiz7u9u2z.jpg",
                  "http://i.imgur.com/XwgNL3n.gifv",
                  "https://i.imgur.com/gallery/rWyFWmR.jpg",
                  "http://i.imgur.com/2mbzfWq.jpg",
                  "https://i.reddituploads.com/7e6fbe4ce57e450e833bcd2737d65e2c?fit=max&h=1536&w=1536&s=5e7014cfe4baad5afff0df1ce459c584",
                  "https://i.reddituploads.com/bb1a7d55ff184458b39cf3e3deb819c1?fit=max&h=1536&w=1536&s=7afe46b4fe8e90e38e4b5ba6464ca1db",
                  "http://i.imgur.com/jfsHXUV.gifv",
                  "https://i.imgur.com/sI8AJqR.jpg",
                  "https://i.imgur.com/18D2DjF.jpg",
                  "https://i.imgur.com/CrSttq4.jpg",
                  "https://i.imgur.com/J2DwMXw.jpg",
                  "http://i.imgur.com/nGDUUhY.jpg",
                  "http://i.imgur.com/IDFyJ4x.gifv",
                  "https://i.redd.it/x7rsfzcrouyy.jpg",
                  "https://i.redd.it/2tinfjwyb1iy.jpg",
                  "https://i.redd.it/mnwbovkwsvzy.gif",
                  "https://i.redd.it/3rcut5hqn5oy.jpg",
                  "https://i.redd.it/t5orvjahk30z.jpg",
                  "http://i.imgur.com/m5HjhY1.gif",
                  "https://i.reddituploads.com/7a3a8ba46ee7436a8f1288a5c003946a?fit=max&h=1536&w=1536&s=241ccd5f8c688411c4e11350cfe6259a",
                  "https://i.reddituploads.com/ac8fc17c17404b2f80700a2c2a9ed20f?fit=max&h=1536&w=1536&s=d02059c1fd931118921373cf3ce3ecc8",
                  "https://i.redd.it/5mefhrz4nqoy.jpg",
                  "http://i.imgur.com/6c7QM8W.png",
                  "http://i.imgur.com/2gmDAnm.jpg",
                  "http://i.imgur.com/9My4X1v.jpg",
                  "https://i.reddituploads.com/a60b53b7694440c6a4b969334a74b9ae?fit=max&h=1536&w=1536&s=a79a1467a3bf4760201b7c816dcea456",
                  "http://i.imgur.com/vCh7XNd.gif",
                  "https://i.imgur.com/BtlL2JX.jpg",
                  "http://i.imgur.com/xmLJFy8.jpg",
                  "http://i.imgur.com/vCh7XNd.gif",
                  "http://i.imgur.com/zTzCybb.png",
                  "http://i.imgur.com/VLmihnM.gifv",
                  "https://i.imgur.com/3opZ020.jpg",
                  "http://i.imgur.com/w5oJxQZ.gifv",
                  "http://i.imgur.com/3xnCwVD.jpg",
                  "http://i.imgur.com/vTbe1VL.jpg",
                  "https://i.redd.it/ebdfl0tg64ny.jpg",
                  "https://i.imgur.com/rSRcGti.gifv",
                  "https://i.imgur.com/a/OBY8r.jpg",
                  "http://i.imgur.com/WS3peGa.jpg",
                  "https://i.imgur.com/PkIO1ul.jpg"]
        choice = random.choice(choices)
        embed = discord.Embed(
            title = "Cat",
            url = f"{choice}",
            color = 0xe24646
        )
        embed.set_image(url = f"{choice}")
        await ctx.send(embed = embed)

#Dog command
@client.command()
async def dog(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        choices = ["https://i.imgur.com/HE1U0VT.jpg",
                   "http://i.imgur.com/EpqYB9k.jpg",
                   "http://i.imgur.com/Km1bsfg.jpg",
                   "https://i.imgur.com/sHmmiu1.jpg",
                   "http://i.imgur.com/9f2up2N.jpg",
                   "https://i.redd.it/nbwlt4ny8w6z.jpg",
                   "http://i.imgur.com/wYWCpSw.jpg",
                   "https://i.imgur.com/qbZXaOJ.jpg",
                   "https://i.reddituploads.com/48c314206ad64b8dbb823b0b88e91ff8?fit=max&h=1536&w=1536&s=38650b4ccdaf2ef959bfc2a3fa44e483",
                   "http://i.imgur.com/PP4Ua3e.jpg",
                   "https://i.imgur.com/gZRYFxZ.jpg",
                   "https://i.redd.it/im9ksyjw5j0z.jpg",
                   "https://i.imgur.com/8U4TpO2.jpg",
                   "https://i.reddituploads.com/d3880620f4494722b9018d4b94a3ee33?fit=max&h=1536&w=1536&s=d702664cb72de6c3560a2158ca31df53",
                   "http://i.imgur.com/15JO3RI.jpg",
                   "https://i.imgur.com/Rb3kfIi.jpg",
                   "http://i.imgur.com/ndDWJBT.jpg",
                   "http://i.imgur.com/88C6sGg.gifv",
                   "https://i.reddituploads.com/e3a400c4b893423c84d92a3a6cafa679?fit=max&h=1536&w=1536&s=1b7ce9359e66a690ddc941f323c0eae6",
                   "https://i.redd.it/40tudj1le67z.",
                   "https://i.reddituploads.com/fbbcba8521fc45d5bd2516500dbc57c9?fit=max&h=1536&w=1536&s=a7d1c115ef7664cae73817686915f2d4",
                   "https://i.reddituploads.com/e6ec337b392a49be9eab05babb5d7712?fit=max&h=1536&w=1536&s=b9e80c7e0d724db25fa284fb9d231899",
                   "https://i.imgur.com/U9yHXIb.jpg",
                   "https://i.imgur.com/iixtzvW.jpg",
                   "https://i.reddituploads.com/7e8b85cbd79b46f38f33957be9000f66?fit=max&h=1536&w=1536&s=e1bb51bd4ace1bc88c8bb1be2658410f",
                   "https://i.redd.it/jedufst1dy8y.jpg",
                   "https://i.imgur.com/O9SuTXk.jpg",
                   "http://i.imgur.com/bRrk2hc.jpg",
                   "https://i.imgur.com/Xi5CSC7.jpg",
                   "https://i.redd.it/71wt3wssbw5z.jpg",
                   "http://i.imgur.com/E5CfwdF.jpg",
                   "https://i.redd.it/xnsodxwvpmiy.jpg",
                   "https://i.imgur.com/0L95gP0.jpg",
                   "https://i.reddituploads.com/4f858baa9ced4a0e9188b05f02b53569?fit=max&h=1536&w=1536&s=54e5b7d7aa71317fe554349fe209d0c6",
                   "https://i.imgur.com/upavcb6.jpg",
                   "https://i.redd.it/qeq6u2tvzc2y.jpg",
                   "https://i.imgur.com/ZgWsQIK.jpg",
                   "https://i.imgur.com/1KaYCKa.jpg",
                   "https://i.redd.it/eieguisu55vy.jpg",
                   "http://i.imgur.com/ef25y11.jpg",
                   "http://i.imgur.com/wI9BQXu.jpg",
                   "https://i.redd.it/mnc10w90ln6z.jpg",
                   "https://i.imgur.com/B0sDssw.jpg",
                   "http://i.imgur.com/33HL7Zd.jpg",
                   "http://i.imgur.com/BxO2Zoi.jpg",
                   "http://i.imgur.com/J1m5fgv.jpg",
                   "https://i.imgur.com/gallery/F9Zi8PG.jpg",
                   "https://i.redd.it/dd54g2foc0ly.jpg",
                   "https://i.redd.it/fuqaxzodohuy.jpg",
                   "http://i.imgur.com/FZ0Ngxr.jpg",
                   "https://i.imgur.com/09Gwa5a.jpg",
                   "https://i.reddituploads.com/ce47d2c46be24a0689bf3b43942e920a?fit=max&h=1536&w=1536&s=792384b6a138f5ad61cc5046995e12e6",
                   "https://i.redd.it/biond94mq8jy.jpg",
                   "http://i.imgur.com/c2tOO8h.jpg",
                   "http://m.imgur.com/d13JoUg",
                   "https://i.redd.it/m4i2b3fusvnx.jpg"]
        choice = random.choice(choices)
        embed = discord.Embed(
            title = "Dog",
            url = f"{choice}",
            color = 0xe24646
        )
        embed.set_image(url = f"{choice}")
        await ctx.send(embed = embed)

#RPS command
@client.command()
async def rps(ctx, choice = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        choice = choice.lower()
        correctchoices = ["rock",
                          "paper",
                          "scissors"]
        if choice == None:
            embed = discord.Embed(
                title = "You need to choose either rock paper or scissors!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)
        if choice in correctchoices:
            possible = ["rock",
                        "paper",
                        "scissors"]
            chosen = random.choice(possible)
            if choice == "rock":
                if chosen == "rock":
                    embed = discord.Embed(
                        title = "Rock VS Rock",
                        description = "It's a tie!",
                        color = 0x07999b
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445464264114186/rock.png")
                    await ctx.send(embed = embed)
                if chosen == "paper":
                    embed = discord.Embed(
                        title = "Rock VS Paper",
                        description = "You lost!",
                        color = 0xdd0000
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445464264114186/rock.png")
                    await ctx.send(embed = embed)
                if chosen == "scissors":
                    embed = discord.Embed(
                        title = "Rock VS Scissors",
                        description = "You won!",
                        color = 0x00cc1b
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445464264114186/rock.png")
                    await ctx.send(embed = embed)
            if choice == "paper":
                if chosen == "rock":
                    embed = discord.Embed(
                        title = "Paper VS Rock",
                        description = "You won!",
                        color = 0x00cc1b
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445487798353937/paper.png")
                    await ctx.send(embed = embed)
                if chosen == "paper":
                    embed = discord.Embed(
                        title = "Paper VS Paper",
                        description = "It's a tie!",
                        color = 0x07999b
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445487798353937/paper.png")
                    await ctx.send(embed = embed)
                if chosen == "scissors":
                    embed = discord.Embed(
                        title = "Paper VS Scissors",
                        description = "You lost!",
                        color = 0xdd0000
                    )
                    embed.set_author(name = "Rock Paper Scisors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445487798353937/paper.png")
                    await ctx.send(embed = embed)
            if choice == "scissors":
                if chosen == "rock":
                    embed = discord.Embed(
                        title = "Scissors VS Rock",
                        description = "You lost!",
                        color = 0xdd0000
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445467170766874/scissors.png")
                    await ctx.send(embed = embed)
                if chosen == "paper":
                    embed = discord.Embed(
                        title = "Scissors Vs Paper",
                        description = "You won!",
                        color = 0x00cc1b
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445467170766874/scissors.png")
                    await ctx.send(embed = embed)
                if chosen == "scissors":
                    embed = discord.Embed(
                        title = "Scissors VS Scissors",
                        description = "It's a tie!",
                        color = 0x07999b
                    )
                    embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581288417619607552/582445467170766874/scissors.png")
                    await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = "You need to choose either rock paper or scissors!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)

#Hug command
@client.command()
async def hug(ctx, member : discord.Member = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            embed = discord.Embed(
                title = "You need to specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)
        else:
            choices = ["https://media1.tenor.com/images/18474dc6afa97cef50ad53cf84e37d08/tenor.gif?itemid=12375072",
                       "https://media1.tenor.com/images/506aa95bbb0a71351bcaa753eaa2a45c/tenor.gif?itemid=7552075",
                       "https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif?itemid=9200935",
                       "https://media1.tenor.com/images/074d69c5afcc89f3f879ca473e003af2/tenor.gif?itemid=4898650",
                       "https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif?itemid=5166500",
                       "https://media1.tenor.com/images/6db54c4d6dad5f1f2863d878cfb2d8df/tenor.gif?itemid=7324587",
                       "https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif?itemid=11074788",
                       "https://media1.tenor.com/images/40aed63f5bc795ed7a980d0ad5c387f2/tenor.gif?itemid=11098589",
                       "https://media1.tenor.com/images/b77fd0cfd95f89f967be0a5ebb3b6c6a/tenor.gif?itemid=7864716",
                       "https://media1.tenor.com/images/7e30687977c5db417e8424979c0dfa99/tenor.gif?itemid=10522729",
                       "https://media1.tenor.com/images/b0de026a12e20137a654b5e2e65e2aed/tenor.gif?itemid=7552093",
                       "https://media1.tenor.com/images/54e97e0cdeefea2ee6fb2e76d141f448/tenor.gif?itemid=11378437",
                       "https://media1.tenor.com/images/b4ba20e6cb49d8f8bae81d86e45e4dcc/tenor.gif?itemid=5634582",
                       "https://media1.tenor.com/images/45b1dd9eaace572a65a305807cfaec9f/tenor.gif?itemid=6238016",
                       "https://media1.tenor.com/images/af76e9a0652575b414251b6490509a36/tenor.gif?itemid=5640885",
                       "https://media1.tenor.com/images/11889c4c994c0634cfcedc8adba9dd6c/tenor.gif?itemid=5634578",
                       "https://media1.tenor.com/images/d3dca2dec335e5707e668b2f9813fde5/tenor.gif?itemid=12668677"]

            embed = discord.Embed(
                title = f"{ctx.message.author.name} hugged {member.name}!",
                color = 0xad29c4
            )
            embed.set_image(url = f"{random.choice(choices)}")
            await ctx.send(embed = embed)

#Pat command
@client.command()
async def pat(ctx, member : discord.Member = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            embed = discord.Embed(
                title = "You need to specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)
        else:
            choices = ["https://media1.tenor.com/images/116fe7ede5b7976920fac3bf8067d42b/tenor.gif?itemid=9200932",
                       "https://media1.tenor.com/images/54722063c802bac30d928db3bf3cc3b4/tenor.gif?itemid=8841561",
                       "https://media1.tenor.com/images/005e8df693c0f59e442b0bf95c22d0f5/tenor.gif?itemid=10947495",
                       "https://media1.tenor.com/images/183ff4514cbe90609e3f286adaa3d0b4/tenor.gif?itemid=5518321",
                       "https://media1.tenor.com/images/1e92c03121c0bd6688d17eef8d275ea7/tenor.gif?itemid=9920853",
                       "https://media1.tenor.com/images/f330c520a8dfa461130a799faca13c7e/tenor.gif?itemid=13911345",
                       "https://media1.tenor.com/images/266e5f9bcb3f3aa87ba39526ee202476/tenor.gif?itemid=5518317",
                       "https://media1.tenor.com/images/60991d021f0f2d4f065ac9b4f00948dc/tenor.gif?itemid=11728232",
                       "https://media1.tenor.com/images/5466adf348239fba04c838639525c28a/tenor.gif?itemid=13284057",
                       "https://media1.tenor.com/images/282cc80907f0fe82d9ae1f55f1a87c03/tenor.gif?itemid=12018857",
                       "https://media1.tenor.com/images/71e74263a48a6e9a2c53f3bc1439c3ac/tenor.gif?itemid=12434286",
                       "https://media1.tenor.com/images/c2232aec426d8b5e85e026cbca410463/tenor.gif?itemid=11648944",
                       "https://media1.tenor.com/images/5a692dc246f2468ca0e37446b4964054/tenor.gif?itemid=13949497",
                       "https://media1.tenor.com/images/078599227bc087959b79ea111fbc0f3a/tenor.gif?itemid=13596135",
                       "https://media1.tenor.com/images/cf9a587a3fc4ef2e8f9f92bae63cb0d0/tenor.gif?itemid=13793739",
                       "https://media1.tenor.com/images/4b52ac769cbef524ee000ba3f84afab0/tenor.gif?itemid=13758199",
                       "https://media1.tenor.com/images/13f385a3442ac5b513a0fa8e8d805567/tenor.gif?itemid=13857199",
                       "https://media1.tenor.com/images/857aef7553857b812808a355f31bbd1f/tenor.gif?itemid=13576017",
                       "https://media1.tenor.com/images/e71e45362fccc0b9a2ccce97bff93780/tenor.gif?itemid=11115628",]

            embed = discord.Embed(
                title = f"{ctx.message.author.name} patted {member.name}!",
                color = 0xad29c4
            )
            embed.set_image(url = f"{random.choice(choices)}")
            await ctx.send(embed = embed)

#Coinflip command
@client.command()
async def coinflip(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        choices = ["Heads",
                   "Tails"]
        embed = discord.Embed(
            title = f"The coin landed on {random.choice(choices)}",
            color = 0xc1c113
        )
        embed.set_author(name = "Coinflip")
        await ctx.send(embed = embed)

#Dice command
@client.command()
async def dice(ctx, sides = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if sides == None:
            land = random.randint(1, 6)
            embed = discord.Embed(
                title = f"The dice landed on {land}!",
                color = 0xFFFFFF
            )
            await ctx.send(embed = embed)
        else:
            digit = sides.isdigit()
            if digit == True:
                sides = float(sides)
                land = random.randint(1, sides)
                embed = discord.Embed(
                    title = f"The dice landed on {land}!",
                    color = 0xFFFFFF
                )
                await ctx.send(embed = embed)

#Invite command
@client.command()
async def invite(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(
            title = "🔗 Invite me!",
            url = "https://discordapp.com/api/oauth2/authorize?client_id=580553153376944159&permissions=8&scope=bot",
            color = 0x07999b
        )
        await ctx.send(embed=embed)

#Support command
@client.command()
async def support(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(
            title = "🔗 Join the support server!",
            url = "https://discord.gg/DrH5Zny",
            color = 0x07999b
        )
        await ctx.send(embed=embed)

#Trello command
@client.command()
async def trello(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(
            title = "🔗 Check out the trello!",
            url = "https://trello.com/b/QPvgdzL3/incognito-bot",
            color = 0x07999b
        )
        await ctx.send(embed=embed)

#Nickname command
@client.command()
async def nick(ctx, member : discord.Member = None, *, nickname = None):
    if ctx.message.author.id in blocked_users:
        nickname1 = nickname.lower()
        nickname = nickname
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            if nickname1 == "reset":
                embed = discord.Embed(
                    title = "Your nickname has been reset!",
                    color = 0x00cc1b
                )
                await ctx.message.author.edit(nick = None)
                await ctx.send(embed = embed)

            if len(nickname) > 38:
                embed = discord.Embed(
                    title = "Your nickname can not be longer then 32 charecters!",
                    color = 0xdd0000
                )
                await ctx.send(embed = embed)

            if len(nickname) < 33 and nickname1 != "reset":
                if nickname == None:
                    embed = discord.Embed(
                        title = "You must choose a nickname!",
                        color = 0xdd0000
                    )
                    await ctx.send(embed = embed, delete_after = 4.0)

                else:
                    embed = discord.Embed(
                        title = f"Your nickname has been changed to {nickname}!",
                        color = 0x00cc1b
                    )
                    await ctx.message.author.edit(nick = nickname)
                    await ctx.send(embed = embed)

        else:
            if nickname1 == "reset":
                embed = discord.Embed(
                    title = f"{member.name}'s nickname has been reset!",
                    color = 0x00cc1b
                )
                await member.edit(nick = None)
                await ctx.send(embed = embed)

            if len(nickname) > 33:
                embed = discord.Embed(
                    title = f"The chosen nickname can not be longer then 32 charecters!",
                    color = 0xdd0000
                )
                await ctx.send(embed = embed)
            if len(nickname) < 33 and nickname1 != "reset":
                embed = discord.Embed(
                    title = f"{member.name}'s nickname has been changed to {nickname}!",
                    color = 0x00cc1b
                )
                await member.edit(nick = nickname)
                await ctx.send(embed = embed)

#Suggestion command
@client.command()
async def suggest(ctx, *, suggestion = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if suggestion == None:
            embed = discord.Embed(
                title = "You must suggest something to use this command!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed, delete_after = 4.0)
            await ctx.message.delete()
        else:
            suggester = ctx.message.author.name + "#" + ctx.message.author.discriminator
            embed = discord.Embed(
                title = f"Suggestion by {suggester}",
                description = f"{suggestion}",
                color = 0x07999b
            )
            embed2 = discord.Embed(
                title = "Your suggestion has been submitted!",
                color = 0x00cc1b
            )
            embed.set_author(name = "Suggestion")
            channel = client.get_channel(581962745998606355)
            message = await channel.send(embed = embed)
            await message.add_reaction("✅")
            await message.add_reaction("<:XMark:563176622501527552>")
            await ctx.message.delete()
            await ctx.send(embed = embed2, delete_after = 4.0)

#Ping command
@client.command()
async def ping(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(
            title = f"Pong! {round(client.latency * 1000)} ms",
            color = 0x00cc1b
        )
        await ctx.send(embed = embed)

#Poll command
@client.command()
@commands.has_permissions(manage_guild = True)
async def poll(ctx, *, pollcontent = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if pollcontent == None:
            embed = discord.Embed(
                title = "You must have something to poll to use this command!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed, delete_after = 4.0)
            await ctx.message.delete()
        else:
            embed = discord.Embed(
                 title = f"{ctx.message.author.name} has created a poll!",
                 description = f"{pollcontent}",
                 color = 0x15ea83
            )
            message = await ctx.send(embed = embed)
            await message.add_reaction("✅")
            await message.add_reaction("<:XMark:563176622501527552>")
            await ctx.message.delete()

#Help command
@client.command()
async def help(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        content = ctx.message.content.lower()
        if content == "$help":
            embed = discord.Embed(
                color = 0x07999b
            )
            embed.set_author(name = "Help", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Purge", value = "\u200b", inline = False)
            embed.add_field(name = "Kick", value = "\u200b", inline = False)
            embed.add_field(name = "Ban", value = "\u200b", inline = False)
            embed.add_field(name = "Unban", value = "\u200b", inline = False)
            embed.add_field(name = "Channelupdate", value = "\u200b", inline = False)
            embed.add_field(name = "Mute", value = "\u200b", inline = False)
            embed.add_field(name = "Unmute", value = "\u200b", inline = False)
            embed.add_field(name = "Eightball", value = "\u200b", inline = False)
            embed.add_field(name = "Ping", value = "\u200b", inline = False)
            embed.add_field(name = "Invite", value = "\u200b", inline = False)
            embed.add_field(name = "Support", value = "\u200b", inline = False)
            embed.add_field(name = "Funfact", value = "\u200b", inline = False)
            embed.add_field(name = "Suggest", value = "\u200b", inline = False)
            embed.add_field(name = "Poll", value = "\u200b", inline = False)
            embed.add_field(name = "Nick", value = "\u200b", inline = False)
            embed.add_field(name = "Rps", value = "\u200b", inline = False)
            embed.add_field(name = "Coinflip", value = "\u200b", inline = False)
            embed.add_field(name = "Dice", value = "\u200b", inline = False)
            embed.add_field(name = "Info", value = "\u200b", inline = False)
            embed.add_field(name = "Stats", value = "\u220b", inline = False)
            embed.add_field(name = "Pat", value = "\u200b", inline = False)
            embed.add_field(name = "Hug", value = "\u200b", inline = False)
            embed.set_footer(text = "For more information on each command do $help (Command)")
            await ctx.send(embed = embed)
        if content == "$help purge":
            embed = discord.Embed(
                title = "Description",
                description = "A command that deletes messages in bulk.\nDefault purge is 10 messages.\nMax purge is 500 messages.",
                color = 0x07999b
            )
            embed.set_author(name = "Purge", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$purge (Amount)``")
            embed.add_field(name = "Example usage", value = "``$purge 123`` or ``$purge``")
            embed.add_field(name = "Requirements", value = "The **Manage Message(s)** permission is required to use this command.")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help kick":
            embed = discord.Embed(
                title = "Description",
                description = "A command that kicks users.",
                color = 0x07999b
            )
            embed.set_author(name = "Kick", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$kick (User)`` or ``$kick (User) (Reason)``")
            embed.add_field(name = "Example usage", value = "``$kick @Incognito User#0000`` or ``$kick @Incognito User#0000 Example reason``")
            embed.add_field(name = "Requirements", value = "The **Kick Member(s)** permission is required to use this command.")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help ban":
            embed = discord.Embed(
                title = "Description",
                description = "A command that bans users.",
                color = 0x07999b
            )
            embed.set_author(name = "Ban")
            embed.add_field(name = "Usage", value = "``$ban (User)`` or ``$ban (User) (Reason)``")
            embed.add_field(name = "Example usage", value = "``$ban @Incognito User#0000`` or ``$ban @Incognito User#0000 Example reason``")
            embed.add_field(name = "Requirements", value = "The **Ban Member(s)** permission is required to use this command.")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help unban":
            embed = discord.Embed(
                title = "Description",
                description = "A command that unbans users.",
                color = 0x07999b
            )
            embed.set_author(name = "Unban", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$unban (User)``")
            embed.add_field(name = "Example usage", value = "``$unban Incognito User#0000``")
            embed.add_field(name = "Requirements", value = "The **Ban Member(s)** permission is required to use this command.")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help eightball":
            embed = discord.Embed(
                title = "Description",
                description = "The eightball game.",
                color = 0x07999b
            )
            embed.set_author(name = "Eightball", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "$8ball (Question)")
            embed.add_field(name = "Example usage", value = "$8ball Should I get nitro??")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help ping":
            embed = discord.Embed(
                title = "Description",
                description = "Shows the bot's current latency",
                color = 0x07999b
            )
            embed.set_author(name = "Ping", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$ping``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help invite":
            embed = discord.Embed(
                title = "Description",
                description = "Sends a link to invite the Incognito bot.",
                color = 0x07999b
            )
            embed.set_author(name = "Invite")
            embed.add_field(name = "Usage", value = "``$invite``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help support":
            embed = discord.Embed(
                title = "Description",
                description = "Sends an invite link to join the support server.",
                color = 0x07999b
            )
            embed.set_author(name = "Support", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$support``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help funfact":
            embed = discord.Embed(
                title = "Description",
                description = "Sends a funfact.",
                color = 0x07999b
            )
            embed.set_author(name = "Fun fact", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$funfact``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help suggest":
            embed = discord.Embed(
                title = "Description",
                description = "Sends a suggestion to be voted on by the devs.",
                color = 0x07999b
            )
            embed.set_author(name = "Suggest", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$suggest (Suggestion)``")
            embed.add_field(name = "Example usage", value = "``$suggest Make more commands``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help nick":
            embed = discord.Embed(
                title = "Description",
                description = "Allows you to change your nickname quickly.\nLike normally the max charecters you can set your nickname is 32.",
                color = 0x07999b
            )
            embed.set_author(name = "Nick", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$nick (Nickname)``")
            embed.add_field(name = "Example usage", value = "``$nick Incognito``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help rps":
            embed = discord.Embed(
                title = "Description",
                description = "Rock Paper Scissors command.",
                color = 0x07999b
            )
            embed.set_author(name = "Rock Paper Scissors", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$rps (Choice)``")
            embed.add_field(name = "Example usage", value = "``$rps Rock``, ``$rps Paper`` or ``$rps Scissors``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help channelupdate":
            embed = discord.Embed(
                title = "Description",
                description = "Updates all the channels in the server so the mute command works properly",
                color = 0x07999b
            )
            embed.set_author(name = "Channelupdate", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$channelupdate (Role [Either mention the role or send the role id])``")
            embed.add_field(name = "Example usage", value = "``$channelupdate @Muted`` or ``$channelupdate 582623298962325504``")
            embed.add_field(name = "Requirements", value = "You must have a role called 'Muted' (Must have a capitol m or else it wont work)\nThe **Manage Server** permission is required to use this command")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help mute":
            embed = discord.Embed(
                title = "Description",
                description = "Mutes a user.",
                color = 0x07999b
            )
            embed.set_author(name = "Mute", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$mute (User)``")
            embed.add_field(name = "Example usage", value = "``$mute @Incognito User#0000``")
            embed.add_field(name = "Requirements", value = "You must have a role called 'Muted' (Must have a capitol m or else it wont work)\nThe **Manage Role(s)** permission is required to use this command")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help unmute":
            embed = discord.Embed(
                title = "Description",
                description = "Unmutes a user.",
                color = 0x07999b
            )
            embed.set_author(name = "Unmute", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$unmute (User)``")
            embed.add_field(name = "Example usage", value = "``$unmute @Incognito User#0000``")
            embed.add_field(name = "Requirements", value = "You must have a role called 'Muted' (Must have a capitol m or else it wont work)\nThe **Manage Role(s)** permission is required to use this command")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help coinflip":
            embed = discord.Embed(
                title = "Description",
                description = "Flips a coin.",
                color = 0x07999b
            )
            embed.set_author(name = "Coinflip", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$coinflip``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help poll":
            embed = discord.Embed(
                title = "Description",
                description = "A command that creates polls.",
                color = 0x07999b
            )
            embed.set_author(name = "Poll", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$poll (Poll)``")
            embed.add_field(name = "Example usage", value = "``$poll What command should I make next?``")
            embed.add_field(name = "Requirements", value = "The **Manage Server** permission is required to use this command.")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help dice":
            embed = discord.Embed(
                title = "Description",
                description = "A command that spins a die.",
                color = 0x0799b
            )
            embed.set_author(name = "Dice", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$dice (Sides)``")
            embed.add_field(name = "Example usage", value = "``$dice 86``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help cat":
            embed = discord.Embed(
                title = "Description",
                description = "Sends a picures of a cat.",
                color = 0x0799b
            )
            embed.set_author(name = "Cat", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$cat``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help dog":
            embed = discord.Embed(
                title = "Description",
                description = "Sends a picures of a dog.",
                color = 0x0799b
            )
            embed.set_author(name = "Dog", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$dog``")
            embed.set_footer(text = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help info":
            embed = discord.Embed(
                title = "Description",
                description = "Shows some information about a selected user.",
                color = 0x0799b
            )
            embed.set_author(name = "Info", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$info (User)``")
            embed.add_field(name = "Example usage", value = "``$info @Incognito User#0000``")
            embed.set_footer(tex = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help stats":
            embed = discord.Embed(
                title = "Description",
                description = "Shows some information about a selected user.",
                color = 0x0799b
            )
            embed.set_author(name = "Stats", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$stats``")
            embed.set_footer(tex = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help pat":
            embed = discord.Embed(
                title = "Description",
                description = "Shows some information about a selected user.",
                color = 0x0799b
            )
            embed.set_author(name = "Pat", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$pat (User)``")
            embed.add_field(name = "Example usage", value = "``$pat @Incognito User#0000``")
            embed.set_footer(tex = "For more help join the support server.")
            await ctx.send(embed = embed)
        if content == "$help hug":
            embed = discord.Embed(
                title = "Description",
                description = "Shows some information about a selected user.",
                color = 0x0799b
            )
            embed.set_author(name = "Hug", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
            embed.add_field(name = "Usage", value = "``$hug (User)``")
            embed.add_field(name = "Example usage", value = "``$hug @Incognito User#0000``")
            embed.set_footer(tex = "For more help join the support server.")
            await ctx.send(embed = embed)

#Information commnad
@client.command(aliases = ["information"])
async def info(ctx, member : discord.Member = None):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        if member == None:
            embed = discord.Embed(
                title = "Please specify a user!",
                color = 0xdd0000
            )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = "Username",
                description = f"{member.name}",
                color = 0x0799b
            )
            embed.set_author(name = f"{member.name}#{member.discriminator}'s Info")
            embed.add_field(name = "Discriminator", value = f"{member.discriminator}")
            embed.add_field(name = "ID", value = f"{member.id}")
            embed.add_field(name = "Account creation date", value = f"{member.created_at}")
            embed.add_field(name = "Profile picture", value = "\u200b", inline = False)
            embed.set_image(url = f"{member.avatar_url}")
            await ctx.send(embed = embed)

#Stats command
@client.command()
async def stats(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        delta_uptime = datetime.utcnow() - client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            title = "Users",
            description = f"{len(client.users)}",
            color = 0x07999b
        )
        embed.set_author(name = "Stats")
        embed.add_field(name = "Servers", value = f"{len(client.guilds)}")
        embed.add_field(name = "Lines of code", value = f"{linecount}")
        embed.add_field(name = "Amount of commands", value = "18")
        embed.add_field(name = "Uptime", value = f"{days}d, {hours}h, {minutes}m, {seconds}s")
        await ctx.send(embed = embed)

#Uptime command
@client.command()
async def uptime(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        delta_uptime = datetime.utcnow() - client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            title = f"{days}d, {hours}h, {minutes}m, {seconds}s",
            color = 0x0799b
        )
        embed.set_author(name = "Uptime")
        await ctx.send(embed = embed)


#Quick shiz
@client.command()
async def fdsjfksdjkfsdhhjdsiuoeuisfjdsdjdhfhfsddjhdfhjdsuiwerywreyudfshdsfsdfu(ctx):
    if ctx.message.author.id in blocked_users:
        embed = discord.Embed(
            title = "You are blocked from using this bot!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(
            title = "**Make sure to check out the trello to see what is currently being done with the bot!**",
            url = "https://trello.com/b/QPvgdzL3/incognito-bot",
            color = 0x07999b
        )
        embed.set_author(name = "Information", icon_url = "https://cdn.discordapp.com/attachments/581663784431779840/581933914923466764/9c73792d3e85a72f8dacdce09db31c1d.png")
        embed.add_field(name = "Online times and expected down times", value = "As I'm not hosting this bot on a VPS and I don't have a good computer the bot will be probably be down over night. The bot will also be down while I am at school.")
        embed.add_field(name = "Devs", value = "This bot was entirley made by <@229695200082132993>.")
        embed.add_field(name = "Self hosting", value = "As of this time self hosting is not possible.")
        embed.add_field(name = "Donations", value = "As of this time donations are not accepted, later on some features might be for people who donate only.")
        embed.add_field(name = "Staff applications", value = "Feel free to apply to join the staff team in <#581966106160267264>.")
        embed.set_footer(text = "If you think something should be added feel free to contant Polar!")
        await ctx.send(embed = embed)

#When bot joins a server lets me know
@client.event
async def on_guild_join(guild):
    print(f"Joined {guild.name}!\nServer ID - {guild.id}\nMember Count - {len(guild.members)}\nOwner Name - {guild.owner.name}#{guild.owner.discriminator}\nNow in {len(client.guilds)} servers and moderating {len(client.users)} users.")

#Welcome messages for support server
@client.event
async def on_member_join(member):
    if member.guild.id == 580553533158326272:
        channel = client.get_channel(582685809241489416)
        embed = discord.Embed(
            title = "Welcome!",
            description = f"Hey {member.mention} welcome to the {member.guild.name}!\nFor support head on over to <#581958844695969802>.\nTo report a bug head on over to <#581965865587834881>.\nMake sure to read <#581993631854886966>!",
            color = 0x1b8450
        )
        await channel.send(embed = embed)

#Command not found error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = "That is a non-existent command!",
            color = 0xdd0000
        )
        await ctx.send(embed = embed, delete_after = 4.0)
        await ctx.message.delete()

#On client start
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("$help | Moderating " + str((len(client.users))) + " users!"))
    print("Opened a new Incognito tab!")
    print(f"Currently running in {len(client.guilds)} servers.")

#Sets the bot token
client.run('NTgwNTUzMTUzMzc2OTQ0MTU5.XOSYdw.pK9mDjYwk_m73fyhL3I20bhibdg')
