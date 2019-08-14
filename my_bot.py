
import discord
import random

list = [1, 2, 3, 4, 5, 6]
hot = ["Heads", "Tails"]
number = int

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello {0.author.mention}'.format(message))

        if message.content.startswith('!creeper'):
            await message.channel.send('Creeper Aw Man')
            await message.channel.send('So we back in the mine')
            await message.channel.send('Got our pickaxe swinging from side to side')
            await message.channel.send('Side-side to side')

        if message.content.startswith('!help'):
            await message.channel.send('Commands:'
                                       '!creeper'
                                       '!hello'
                                       '!help'
                                       '!bismillah'
                                       '!rolldice'
                                       '!flipcoin'
                                       '!memereview'
                                       '!fortnite'
                                       '!bitch')

        if message.content.startswith('!fortnite'):
            await message.channel.send('is trash')

        if message.content.startswith('!bitch'):
            await message.channel.send('lasagna')

        if message.content.startswith('!bismillah'):
            await message.channel.send('Audoo Billahi, Himin Ashaythaan Nira Jeem')

        if message.content.startswith('!rolldice'):
            await message.channel.send(random.choice(list))

        if message.content.startswith('!flipcoin'):
            await message.channel.send(random.choice(hot))

        if message.content.startswith('!memereview'):
            await message.channel.send('👏')
            await message.channel.send('👏')

client = MyClient()
client.run('NjEwODY4OTI2NTY1NDQ5ODY1.XVMG4w.OSUE0MPdGwmtkTyYHGOoZ8xwSSs')