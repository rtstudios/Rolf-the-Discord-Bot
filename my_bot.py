import discord
from discord.ext import commands
import random
import tweepy
import asyncio

# This also uses the Tweepy Twitter API for a command

auth = tweepy.OAuthHandler("TOKEN",
                           "TOKEN")

auth.set_access_token("TOKEN",
                      "TOKEN")

api = tweepy.API(auth)

bot = commands.Bot(command_prefix="!")

list = [1, 2, 3, 4, 5, 6]
hot = ["Heads", "Tails"]
img = 'https://i.ytimg.com/vi/wbjUAgtb27g/maxresdefault.jpg'
img2 = 'https://i.ytimg.com/vi/6-ey4j9rrO0/maxresdefault.jpg'
img3 = 'https://meme.xyz/uploads/posts/t/l-32881-pewdiepie-memes-claps-twice-guess-ill-die.jpg'
img4 = 'https://pics.me.me/them-isnt-my-baby-so-cute-their-baby-55986217.png'
img5 = 'https://pics.me.me/memes-2019-memes-2012-has-a-pet-rock-it-runs-57399376.png'
img6 = 'https://i.chzbgr.com/full/9233901568/hB41CDDDE/'
img7 = 'https://i.redd.it/8nf2xnv2so211.jpg'
img8 = 'https://i.kym-cdn.com/photos/images/original/001/522/196/09e.png'

memePicker = [img, img2, img3, img4, img5, img6, img7, img8]

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)

@bot.command(pass_context=True,
             description="Welcome to the Soviet Union")
async def welcome(ctx):
    await ctx.send('добро пожаловать в советский союз! коммунист и гордый')

# Flips a coin
@bot.command(pass_context=True,
             description="Heads or tails")
async def flipcoin(ctx):
    await ctx.send(random.choice(hot))

# Rolls a dice
@bot.command(pass_context=True,
             description="Roll a dice")
async def rolldice(ctx):
    await ctx.send(random.choice(list))

# PewDiePie's meme review
@bot.command(pass_context=True,
             description="This obviously doesn't need a description")
async def memereview(ctx):
    await ctx.send('👏')
    await ctx.send('👏')
    await ctx.send(random.choice(memePicker))

# Discord bot sings CaptainSparklez's song "Revenge"
@bot.command(pass_context = True,
             description="Revenge - CaptainSparklez")
async def creeper(ctx):
    await ctx.send('Creeper, aw man')
    await ctx.send('So we back in the mine')
    await ctx.send('Got our pickaxe swinging from')
    await ctx.send('Side to side')
    await ctx.send('Side-side to side')

# You can use this command to search Twitter for tweets containing a keyword
@bot.command(pass_context=True,
             description="Searches for tweets on Twitter")
async def search(ctx, arg):
    for tweet in api.search(q=arg, lang="en", rpp=5):
        await ctx.send(f"{tweet.user.name}: {tweet.text}")

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

bot.run(TOKEN)
