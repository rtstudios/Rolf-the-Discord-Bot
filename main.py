import discord
from discord.ext import commands
import random
import asyncio
import keep_alive
import prayertimes
from datetime import date
import praw
import time

bot = commands.Bot(command_prefix="/")
TOKEN = "TOKEN"

diceList = [1, 2, 3, 4, 5, 6]

flipCoin = ["Heads", "Tails"]

responses = ["Yes", "No", "Maybe", "Try Again Later", "Perhaps", "My sources say no"]

prayerTimes = prayertimes.PrayTimes()

reddit = praw.Reddit(
  client_id="client id",
  client_secret="secret",
  user_agent="agent",
  username="username",
  password="password",
)
subreddit = reddit.subreddit("dankmemes")

activeGiveaway = False
giveawayMembers = []

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print("Online")
    await bot.change_presence(activity=discord.Game(name="sleeping with your goo"), status=None, afk=False)
    keep_alive.keep_alive()

# Says hello
@bot.command(pass_context = True,
            description="Hello")
async def hello(ctx):
    await ctx.send("Hello!")

# Flips a coin
@bot.command(pass_context=True,
             description="Heads or tails")
async def flipcoin(ctx):
    await ctx.send(random.choice(flipCoin))

# Rolls a dice
@bot.command(pass_context=True,
             description="Roll a dice")
async def rolldice(ctx):
    await ctx.send(random.choice(diceList))

# Sends a meme from reddit
@bot.command(pass_context=True,
            description="Sends a meme from reddit")
async def meme(ctx):
  await ctx.send("⚠️ WARNING: Some memes may be inappropriate for ishti ⚠️")
  time.sleep(1)
  await ctx.send("All memes are provided by r/dankmemes!")
  posts = subreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      await ctx.send(post.url)

# This command solves math problems
@bot.command(pass_context = True,
             description='Helps you with your math homework')
async def math(ctx, int1, int2):
    await ctx.send('Added:')
    await ctx.send(int(int1) + int(int2))
    await ctx.send('Subtracted:')
    await ctx.send(int(int1) - int(int2))
    await ctx.send('Multiplied:')
    await ctx.send(int(int1) * int(int2))
    await ctx.send('Divided:')
    await ctx.send(int(int1) / int(int2))

# Magic 8 Ball
@bot.command(pass_context = True,
            description="Ask a question and the discord bot replies with a response")
async def eightball(ctx):
    await ctx.send(random.choice(responses))

# Teleport command
@bot.command(pass_context = True,
            description="Teleports a person")
async def tp(ctx, person):
    await ctx.send(str(person) + " teleported to: " + str(random.randrange(-1000, 1000)) + ", " + str(random.randrange(-1000, 1000)) + ", " + str(random.randrange(-1000, 1000)))

# Sends a roblox emote GIF
@bot.command(pass_context = True,
            description="/e dance")
async def e(ctx):
  await ctx.send("https://vignette.wikia.nocookie.net/roblox/images/7/74/R6dance2.gif/revision/latest/top-crop/width/220/height/220?cb=20190706231444")

# Sends a nice DM to the person who triggered the command
@bot.command(pass_context = True,
            description="Sends a nice DM to the person who triggered the command")
async def trash(ctx):
  await ctx.author.send("shut the goo up you fiend looking talus creature. go whip your goo back and forth and slide it up your a5555 you goon")

# Picks out a random server member
@bot.command(pass_context = True,
            description="Picks out a random server member")
async def russianroulette(ctx):
  user = random.choice(ctx.message.channel.guild.members)
  await ctx.send(f'{ctx.message.author.mention} shot {user.mention}')

# ROLFs bio
@bot.command(pass_context = True,
            description="The story of the bot")
async def about(ctx):
  await ctx.send("Hello, I am the digital manifestation of PewDiePie's late pet, ROLF.")
  await ctx.send("I was created by WAFEEE to manage the discord server of the Faandemic Control Team")
  await ctx.send("Type /help for a list of commands.")

# Bot joins the voice channel
@bot.command(pass_context = True,
            description="Bot joins the voice channel")
async def join(ctx):
  author = ctx.message.author
  channel = author.voice.channel
  vc = await channel.connect()

# Returns the prayer times for that day
@bot.command(pass_context = True,
            description="Returns the prayer times for that day")
async def prayertimes(ctx):
  times = prayerTimes.getTimes(date.today(), (42, 73), 5.7)
  for i in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight']:
    await ctx.send(i + ': ' + times[i.lower()])

# Invites a user to play a game
@bot.command(pass_context = True,
            description="Invites a user to play a game")
async def invite(ctx, member: discord.Member, *, game):
  user = await member.create_dm()
  await user.send("Hello, " + str(ctx.author) + " invited you to play " + str(game))

# Mutes user
@bot.command(pass_context = True,
            description="Mutes user")
@commands.has_role("Admins")
async def mute(ctx, member: discord.Member, *, message):
  role = discord.utils.get(member.guild.roles, name="Muted")
  await member.add_roles(role)
  await ctx.send(str(member) + " has been muted for " + str(message))
  user = await member.create_dm()
  await user.send("You were muted for " + str(message))

# Unmutes a user
@bot.command(pass_context = True,
            description="Unmutes a user")
@commands.has_role("Admins")
async def unmute(ctx, member: discord.Member):
  role = discord.utils.get(member.guild.roles, name="Muted")
  await member.remove_roles(role)
  await ctx.send(str(member) + " has been unmuted!")

# Starts a giveaway
@bot.command(pass_context = True,
            description="Starts a giveaway")
async def giveaway(ctx, duration, *, item):
  global activeGiveaway
  activeGiveaway = True

  embed = discord.Embed(title=item, description=str(ctx.message.author.mention) + " is giving away " + str(item) + "\n" + "\n" + "Type /enter to enter the giveaway", color=0x0000ff)
  await ctx.send(embed=embed)

  await asyncio.sleep(int(duration))

  winner = random.choice(giveawayMembers)
  winEmbed = discord.Embed(title="Winner", description=str(winner + " has won " + item), color=0x0000ff)
  await ctx.send(embed=winEmbed)
  activeGiveaway = False

# Enters a giveaway
@bot.command(pass_context = True,
            description="Enters a giveaway")
async def enter(ctx):
  if activeGiveaway == True:
    giveawayMembers.append(str(ctx.message.author))
    await ctx.send(str(ctx.message.author.mention) + " has entered the giveaway")
  else:
    await ctx.send("There are currently no active giveaways")
    await ctx.send("Type /giveaway [seconds] [item] to start a giveaway")

# PP size
@bot.command(pass_context = True,
            description="Gives PP size")
async def pp(ctx):
  lengthOfPP = []
  lengthOfPPString = ""

  for i in range(random.randrange(1, 20)):
    lengthOfPP.append("=")

  await ctx.send(ctx.message.author.mention + " penis size:")
  await ctx.send("8" + lengthOfPPString.join(lengthOfPP) + "D")

  if len(lengthOfPP) <= 5:
    await ctx.send("haha very small pp")
  elif len(lengthOfPP) <= 14:
    await ctx.send("decent sized pp")
  elif len(lengthOfPP) > 15:
    await ctx.send("VERY BIG PP")

# Shuts down the bot
@bot.command(description="Deactivate bot")
@commands.is_owner()
async def shutdown(ctx):
  await ctx.send("ight imma head out")
  await ctx.bot.logout()

bot.run(TOKEN)
