import discord
import random
import json
import urllib.request as url
prefix='?'
client = discord.Client()

def cap_first_letter(word):
    word2=str()
    try:
        word2=word[0].upper()
    except:
        pass
    for char in word[1:]:
        word2=word2+char
    return word2
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="ChemMixer"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix+'hello'):
        if random.randint(0,1)==0:
            await message.channel.send('Hello!')
        else:
            await message.channel.send('Hi!')
    if message.content.startswith(prefix+'ping'):
        await message.channel.send('Pong!')
    if message.content.startswith(prefix+'wikipedia'):
        msgcontent=message.content
        msgcontent=msgcontent.split(' ')[1:]
        msgcontent=cap_first_letter('_'.join(msgcontent))
        await message.channel.send('https://en.wikipedia.org/wiki/'+msgcontent)
client.run('NTU0NzIyODU4OTc5NDI2MzI0.XPAAKg.pCNApp-JNVyQb63A4whXDuJY3WQ')
