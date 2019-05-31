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
        
    if message.content.startswith(prefix+'ping'):
        await message.channel.send('Pong!')
    if message.content.startswith(prefix+'help'):
        await message.channel.send('''
List of Commands:
dosupdates - N/A - Get latest updates about DOS ChemMixer.
ping - N/A - Sample command.
updates - N/A - Get latest updates about ChemMixer.
verinfo - N/A - Get version information
wikipedia - [article name] - Searches in wikipedia the specified article name.
        ''')
    if message.content.startswith(prefix+'verinfo'):
        await message.channel.send('Current Version: 0.4.0b')
    if message.content.startswith(prefix+'updates'):
        await message.channel.send('''
*-* Updates Bulletin N.1 31/05/2019 *-*
Chemixer v0.4.0b
-------------------------
+Lithium, Flourine and Sodium derivates
+Bugfixes
-Career mode
        ''')
    if message.content.startswith(prefix+'dosupdates'):
        await message.channel.send('''
*-* Updates Bulletin N.1 31/05/2019 *-*
Chemixer v0.4.0 (DOS)
-------------------------
+Minus memory use
+Arrow keys navigation
+Better UI
+Compatible with all Text-mode comaptible graphic cards/drivers
+Tested on MS-DOS 6.22
-Narrow menu
+Scrollbar (WIP)
        ''')
    if message.content.startswith(prefix+'wikipedia'):
        msgcontent=message.content
        msgcontent=msgcontent.split(' ')[1:]
        msgcontent=cap_first_letter('_'.join(msgcontent))
        await message.channel.send('https://en.wikipedia.org/wiki/'+msgcontent)
        
client.run(token)
