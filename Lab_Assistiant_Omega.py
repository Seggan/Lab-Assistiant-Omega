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
Command Prefix: ?
List of Commands:
dosupdates - N/A - Get latest updates about DOS ChemMixer.
eval-[expression; can include words instead of signs]-evaluates the given expression.
ping - N/A - Sample command.
randnum-[two numbers seperated by a dash (-)]-gives a random integer between the two specified numbers.
updates - N/A - Get latest updates about ChemMixer.
verinfo - N/A - Get version information
wikipedia - [article name] - Searches in wikipedia the specified article name.
        ''')
    if message.content.startswith(prefix+'verinfo'):
        await message.channel.send('''Current Version: 0.3.0
Upcoming Version: 0.4.0''')
    if message.content.startswith(prefix+'eval'):
        evalstr=message.content
        evalstr=evalstr.split(' ')[1:]
        if "^" in evalstr:
            evalstr=evalstr.replace("^","**")
        if "to the power of" in evalstr:
            evalstr=evalstr.replace("to the power of","**")
        if "modulo" in evalstr:
            evalstr=evalstr.replace("modulo","%")
        if "mod" in evalstr:
            evalstr=evalstr.replace("mod","%")
        if "times" in evalstr:
            evalstr=evalstr.replace("times","*")
        if "multiplied by" in evalstr:
            evalstr=evalstr.replace("multiplied by","*")
        if "plus" in evalstr:
            evalstr=evalstr.replace("plus","+")
        if "added to" in evalstr:
            evalstr=evalstr.replace("added to","+")
        if "add" in evalstr:
            evalstr=evalstr.replace("add","+")
        if "minus" in evalstr:
            evalstr=evalstr.replace("minus","-")
        if "subtracted by" in evalstr:
            evalstr=evalstr.replace("subtracted by","-")
        if "subtract" in evalstr:
            evalstr=evalstr.replace("subtract","-")
        if "divided by" in evalstr:
            evalstr=evalstr.replace("divided by","/")
        if "divide" in evalstr:
            evalstr=evalstr.replace("divide","/")
        await message.channel.send('The answer is: '+eval(evalstr))
    if message.content.startswith(prefix+'randnum'):
        msgcontent=message.content
        msgcontent=msgcontent.split(' ')[1:]
        msgcontent=msgcontent.split('-')
        await message.channel.send('Your random number is: '+random.randint(msgcontent[0], msgcontent[1])
    if message.content.startswith(prefix+'updates'):
        await message.channel.send('''
*-* Updates Bulletin *-*
Chemixer v0.4.0 (Upcoming)
-------------------------
+Lithium, Nitrogen, Flourine and Carbon derivates
+Bugfixes
+GUI
+Credits
+Logo

Chemixer v0.3.0
-------------------------
+Aluminum derivates
+Bugfixes
+Credits

Chemixer v0.2.2
-------------------------
+Bugfixes''')
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
+Scrollbar (WIP)''')
    if message.content.startswith(prefix+'wikipedia'):
        msgcontent=message.content
        msgcontent=msgcontent.split(' ')[1:]
        msgcontent=cap_first_letter('_'.join(msgcontent))
        await message.channel.send('https://en.wikipedia.org/wiki/'+msgcontent)
        
client.run(token)
