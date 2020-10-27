import discord
from discord.ext import commands
import random
import asyncio
from datetime import date
import praw
import prayertimes
from discord.utils import get
from discord import FFmpegPCMAudio
import os
from os import system
import youtube_dl
import qrcode
import requests

bot = commands.Bot(command_prefix="/")
bot.remove_command("help")
TOKEN = "TOKEN"

diceList = [1, 2, 3, 4, 5, 6]

flipCoin = ["Heads", "Tails"]

responses = ["Yes", "No", "Maybe", "Try Again Later", "Perhaps", "My sources say no"]

prayerTimes = prayertimes.PrayTimes()

reddit = praw.Reddit(
  client_id="id",
  client_secret="secret",
  user_agent="agent",
  username="username",
  password="password",
)

memes = reddit.subreddit("dankmemes")
catSubreddit = reddit.subreddit("catpictures")
dogSubreddit = reddit.subreddit("dogpictures")
monkeSubreddit = reddit.subreddit("Monke")

activeGiveaway = False
giveawayMembers = []

@bot.event
async def on_ready():
  print('Logged in as:')
  print(bot.user.name)
  print("Online")
  await bot.change_presence(activity=discord.Game(name="discord.py"), status=None, afk=False)

@bot.event
async def on_message(message: discord.Message):
  dmChannel = bot.get_channel(724786109154066463)
  if message.author.id != 184408626306351104 and not message.author.bot and message.guild is None:
    embed = discord.Embed(title="Message received", description="**From** " + str(message.author.mention) + "\n \n" + str(message.content), color=0x0000ff)
    await dmChannel.send(embed=embed)
  await bot.process_commands(message)

# Help command
@bot.command(pass_context = True)
async def help(ctx):
  helpText = """
  /help - Shows this message


  Fun commands

  /flipcoin - Flips a coin
  /rolldice - Rolls a dice
  /eightball [question] - Gives a random response to the given question
  /tp - Teleports mentioned person
  /e - Sends a ROBLOX GIF
  /russianroulette - Shoots (pings) a random user
  /meme - Sends a random meme from r/dankmemes
  /dog - Sends a random dog picture from r/dogpictures
  /cat - Sends a random cat picture from r/catpictures
  /monke - Sends a random ape picture from r/ape
  /math [operation] [number] [number] - Performs an operation on two numbers
  /prayertimes - Gives the prayer times
  /giveaway [time in minutes] [item] - Starts a giveaway
  /enter - Lets you enter any active giveaway
  /pp - Gives a random PP size
  /animate [emoji] - Animates a message
  /qr [message] - Generates a QR code for the given message


  Voice chat commands

  /join - Bot join voice channel (requires DJ role)
  /play [url] - Plays a song from YouTube with the given URL (requires DJ role)
  /leave - Bot leaves voice channel (requires DJ role)
  /stop - Bot stops playing all audio (requires DJ role)
  /pause - Bot pauses current audio (requires DJ role)
  /resume - Bot resumes current audio (requires DJ role)


  Moderation commands

  /mute [user] [reason] - Mutes a user indefinitely
  /unmute [user] - Unmutes user
  /cancel [user] [reason] - Kicks user from server
  /kill [user] [reason] - Bans user from server
  /cleanse [number] - Deletes a certain number of messages


  Misc commands

  /hello - Says hello and mentions author
  /invite [user] [game] - Bot invites a user to play a game via DMs
  /message [user id] [message] - Bot DMs given user
  /ping - Returns bot latency
  /who [user id] - Returns a user's information with the given ID
  """

  embed = discord.Embed(title="Command usage", description=helpText, color=0x0000ff)
  await ctx.send(embed=embed)

# Says hello
@bot.command(pass_context = True)
async def hello(ctx):
  await ctx.send("Hello " + str(ctx.message.author.mention) + "!")

# Flips a coin
@bot.command(pass_context=True)
async def flipcoin(ctx):
  embed = discord.Embed(title="Flipped coin", description="You got " + str(random.choice(flipCoin)), color=0x0000ff)
  await ctx.send(embed=embed)

# Rolls a dice
@bot.command(pass_context=True)
async def rolldice(ctx):
  embed = discord.Embed(title="Rolled dice", description="You got a " + str(random.choice(diceList)), color=0x0000ff)
  await ctx.send(embed=embed)

# Magic 8 Ball
@bot.command(pass_context = True)
async def eightball(ctx):
  embed = discord.Embed(title="Response", description=str(random.choice(responses)), color=0x0000ff)
  await ctx.send(embed=embed)

# Teleport command
@bot.command(pass_context = True)
async def tp(ctx, person):
  embed = discord.Embed(title="Teleported!", description=str(person) + " **teleported to** " + str(random.randrange(-1000, 1000)) + ", " + str(random.randrange(-1000, 1000)) + ", " + str(random.randrange(-1000, 1000)), color=0x0000ff)
  await ctx.send(embed=embed)

# Sends a roblox emote GIF
@bot.command(pass_context = True)
async def e(ctx):
  await ctx.send("https://media.tenor.com/images/4a129caa23d88c3c63afeef731417473/tenor.gif")

# Picks out a random server member
@bot.command(pass_context = True)
async def russianroulette(ctx):
  user = random.choice(ctx.message.channel.guild.members)
  await ctx.send(f'{ctx.message.author.mention} *shot* {user.mention}')

# Sends a meme from reddit
@bot.command(pass_context=True)
async def meme(ctx):
  posts = memes.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/dankmemes", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# Sends a cat image from reddit
@bot.command(pass_context=True,)
async def cat(ctx):
  posts = catSubreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/catpictures", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# Sends a dog image from reddit
@bot.command(pass_context=True)
async def dog(ctx):
  posts = dogSubreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/dogpictures", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# Sends a monke image from reddit
@bot.command(pass_context=True)
async def monke(ctx):
  posts = monkeSubreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/Monke", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# This command solves math problems
@bot.command(pass_context = True)
async def math(ctx, operation, number1, number2):
  if operation == "add":
    await ctx.send(str(number1) + " + " + str(number2) + " = " + str(int(number1) + int(number2)))
  elif operation == "subtract":
    await ctx.send(str(number1) + " - " + str(number2) + " = " + str(int(number1) - int(number2)))
  elif operation == "multiply":
    await ctx.send(str(number1) + " * " + str(number2) + " = " + str(int(number1) * int(number2)))
  elif operation == "divide":
    await ctx.send(str(number1) + " / " + str(number2) + " = " + str(int(number1) / int(number2)))

# Bot joins the voice channel
@bot.command(pass_context = True)
@commands.has_role("DJ")
async def join(ctx):
  author = ctx.message.author
  channel = author.voice.channel
  vc = await channel.connect()

# Plays audio with the given URL
@bot.command(pass_context = True)
@commands.has_role("DJ")
async def play(ctx, url):
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  embedShortly = discord.Embed(title="Intermission", description="The audio will play shortly" + "\n \n" + "Audio requested by " + str(ctx.message.author.mention), color=0x0000ff)
  await ctx.send(embed=embedShortly)
  voice = get(bot.voice_clients, guild=ctx.guild)
  songThere = os.path.isfile("song.mp3")
  try:
    if songThere:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("Something went wrong :/")
    return
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, 'song.mp3')
  voice.play(discord.FFmpegPCMAudio("song.mp3"))
  voice.volume = 100
  voice.is_playing()
  embedPlaying = discord.Embed(title="Now playing", description=str(url) + "\n \n" + "Audio requested by " + str(ctx.message.author.mention), color=0x0000ff)
  await ctx.send(embed=embedPlaying)

# Bot stops playing audio
@bot.command(pass_context = True)
@commands.has_role("DJ")
async def stop(ctx):
  voice = get(bot.voice_clients, guild=ctx.guild)
  voice.stop()
  embed = discord.Embed(title="Stopped", description="Audio has stopped" + "\n \n" + "Action requested by " + str(ctx.message.author.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Bot pauses current audio
@bot.command(pass_context = True)
@commands.has_role("DJ")
async def pause(ctx):
  voice = get(bot.voice_clients, guild=ctx.guild)
  voice.pause()
  embed = discord.Embed(title="Paused", description="Audio has been paused" + "\n \n" + "Action requested by " + str(ctx.message.author.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Bot resumes playing audio
@bot.command(pass_context = True)
@commands.has_role("DJ")
async def resume(ctx):
  voice = get(bot.voice_clients, guild=ctx.guild)
  voice.resume()
  embed = discord.Embed(title="Resumed", description="Audio has been resumed" + "\n \n" + "Action requested by " + str(ctx.message.author.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Bot disconnects from voice channel
@bot.command(pass_context = True)
@commands.has_role("DJ")
async def leave(ctx):
  voice = ctx.message.guild.voice_client
  await voice.disconnect(force = True)

# Returns the prayer times for that day
@bot.command(pass_context = True,)
async def prayertimes(ctx):
  prayerTimesList = []
  times = prayerTimes.getTimes(date.today(), (42, 73), 5.7)
  for i in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
    prayerTimesList.append(str(i + ': ' + times[i.lower()]))
  prayerTimesStr = prayerTimesList[0] + "\n" + prayerTimesList[1] + "\n" + prayerTimesList[2] + "\n" + prayerTimesList[3] + "\n" + prayerTimesList[4] + "\n"
  embed = discord.Embed(title="Prayer times", description=prayerTimesStr, color=0x0000ff)
  await ctx.send(embed=embed)

# Starts a giveaway
@bot.command(pass_context = True)
async def giveaway(ctx, duration, *, item):
  global activeGiveaway
  activeGiveaway = True

  embed = discord.Embed(title=item, description=str(ctx.message.author.mention) + " is giving away " + str(item) + "\n" + "\n" + "Type /enter to enter the giveaway", color=0x0000ff)
  await ctx.send(embed=embed)

  await asyncio.sleep(int(duration) * 60)

  winner = random.choice(giveawayMembers)
  winEmbed = discord.Embed(title="Winner", description=str(winner + " has won " + item), color=0x0000ff)
  await ctx.send(embed=winEmbed)
  activeGiveaway = False

# Enters a giveaway
@bot.command(pass_context = True)
async def enter(ctx):
  if activeGiveaway == True:
    giveawayMembers.append(str(ctx.message.author))
    await ctx.send(str(ctx.message.author.mention) + " has entered the giveaway")
  else:
    await ctx.send("There are currently no active giveaways" + "\n" + "Type /giveaway [seconds] [item] to start a giveaway")

# PP size
@bot.command(pass_context = True)
async def pp(ctx):
  lengthOfPP = []
  lengthOfPPString = ""

  for i in range(random.randrange(1, 20)):
    lengthOfPP.append("=")

  embed = discord.Embed(title="Penis size", description="8" + lengthOfPPString.join(lengthOfPP) + "D", color=0x0000ff)
  await ctx.send(embed=embed)

# Override command
@bot.command(pass_context = True)
@commands.has_role("kool kid")
async def override(ctx, *, message):
  await ctx.send(message)
  await ctx.message.delete()

# Invites a user to play a game
@bot.command(pass_context = True)
async def invite(ctx, member: discord.Member, *, game):
  user = await member.create_dm()
  await user.send("Hello, " + str(ctx.author) + " invited you to play " + str(game))
  embed = discord.Embed(title="Invite sent", description="**From** " + str(ctx.message.author.mention) + "\n" + "**To** " + str(member.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Message command
@bot.command(pass_context = True)
async def message(ctx, userID, *, message):
  try:
    user = bot.get_user(int(userID))
    await user.send(message)
    embed = discord.Embed(title="Message sent", description="**From** " + str(ctx.message.author.mention) + "\n" + "**To** " + str(bot.get_user(int(userID)).mention), color=0x0000ff)
    await ctx.send(embed=embed)
  except:
    embed = discord.Embed(title="Messsage failed to send", description="Invalid User ID", color=0x0000ff)
    await ctx.send(embed=embed)

# Mutes user
@bot.command(pass_context = True)
@commands.has_role("kool kid")
async def mute(ctx, member: discord.Member, *, message):
  role = discord.utils.get(member.guild.roles, name="Muted")
  await member.add_roles(role)
  embed = discord.Embed(title="User muted", description="**User** " + str(member.mention) + "\n" + "**Reason** " + str(message), color=0x0000ff)
  await ctx.send(embed=embed)
  await ctx.send("https://media.tenor.com/images/ac7f9ffd8f172477e28ab284b1134b76/tenor.gif")
  user = await member.create_dm()
  await user.send("You were muted for " + str(message))

# Unmutes a user
@bot.command(pass_context = True)
@commands.has_role("kool kid")
async def unmute(ctx, member: discord.Member):
  role = discord.utils.get(member.guild.roles, name="Muted")
  await member.remove_roles(role)
  await ctx.send(str(member.mention) + " has been unmuted!")

# Kicks user
@bot.command(pass_context = True)
@commands.has_role("kool kid")
async def cancel(ctx, member: discord.Member, *, message):
  await member.kick(reason=message)
  embed = discord.Embed(title="User kicked", description="**User** " + str(member.mention) + "\n" + "**Reason** " + str(message), color=0x0000ff)
  await ctx.send(embed=embed)
  await ctx.send("https://media1.giphy.com/media/edP47TgaxmTy4OV2cW/giphy.gif")
  user = await member.create_dm()
  await user.send("You were kicked for " + str(message))

# Bans user
@bot.command(pass_context = True)
@commands.has_role("kool kid")
async def kill(ctx, member: discord.Member, *, message):
  await member.ban(reason=message)
  embed = discord.Embed(title="User banned", description="**User** " + str(member.mention) + "\n" + "**Reason** " + str(message), color=0x0000ff)
  await ctx.send(embed=embed)
  await ctx.send("https://media.giphy.com/media/jxqOV4sZ8eM5o4W16H/giphy.gif")
  user = await member.create_dm()
  await user.send("You were banned for " + str(message))

# Deletes messages
@bot.command(pass_context = True)
@commands.has_role("kool kid")
async def cleanse(ctx, number):
  await ctx.message.delete()
  numberPlusOne = int(number) + 1
  await ctx.channel.purge(limit = numberPlusOne)
  await ctx.send("This channel has been cleansed" + "\n" + "https://media.tenor.com/images/00fb44a75f05b234087ed5c1c93763e9/tenor.gif")
  
# Animates message
@bot.command(pass_context = True)
async def animate(ctx, *, message):
  messageSpaces = ""
  botMessage = await ctx.send(message)
  for i in range(20):
    messageSpaces += "⠀" * i
    await botMessage.edit(content = str(messageSpaces) + str(message))
    await asyncio.sleep(0.5)

# Turns a message into a QR code
@bot.command(pass_context = True)
async def qr(ctx, *, message):
  img = qrcode.make(message)
  img.save("./qrcode.png")
  qrcodefile = discord.File("./qrcode.png", filename="qrcode.png")
  embed = discord.Embed(title=message, color=0x0000ff)
  embed.set_image(url="attachment://qrcode.png")
  await ctx.send(file=qrcodefile, embed=embed)

# Returns bot latency
@bot.command(pass_context = True)
async def ping(ctx):
  embed = discord.Embed(title = "Pong!", description = "**Latency** " + str(round(bot.latency * 1000)) + "ms", color=0x0000ff)
  await ctx.send(embed=embed)

# Returns user info
@bot.command(pass_context = True)
async def who(ctx, userID):
  user = await bot.fetch_user(int(userID))
  userInfo = "**User ID** " + str(user.id) + "\n" + "**Is Bot** " + str(user.bot) + "\n" + "**Created** " + str(user.created_at) + "\n"
  embed = discord.Embed(title = user.display_name, description = userInfo, color=0x0000ff)
  embed.set_image(url=user.avatar_url)
  await ctx.send(embed=embed)


bot.run(TOKEN)
