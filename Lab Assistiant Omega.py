import discord
import random

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Awaiting your command"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?hello'):
        if random.randint(0,1)==0:
            await message.channel.send('Hello!')
        else:
            await message.channel.send('Hi!')

client.run('NTU0NzIyODU4OTc5NDI2MzI0.XPAAKg.pCNApp-JNVyQb63A4whXDuJY3WQ')
