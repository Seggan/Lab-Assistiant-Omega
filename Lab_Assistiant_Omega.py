import json
import random
import time

import discord
from bs4 import BeautifulSoup

prefix = '?'
filtered_words = [
    'shit',
    'fuck',
    'fucking',
    'f*ck',
    'f**k',
    'f***ing',
    'fu**ing',
    'f*****g',
    'f****ng',
    'f\u016Bck',
    'f\u016B*k',
    'f\u016B**ing',
    '|= |_| ( |<',
    'holy crap'
]
bot_logs = 607013134254735363
client = discord.Client()


def html_request(page, header={"User-Agent": "Google Chrome"}):
    import urllib.request as url
    query = url.Request(page, headers=header)
    page = url.urlopen(query)
    return page


def cap_first_letter(word):
    word2 = str()
    try:
        word2 = word[0].upper()
    except:
        pass
    for char in word[1:]:
        word2 = word2 + char
    return word2


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="ChemMixer"))


@client.event
async def on_message(message):
    global msgcontent
    msgcontent = str(message.content)
    channel = message.channel
    with open("money.json", 'r') as f:
        money = json.load(f)
    try:
        money[message.author.name] += 1
        with open("money.json", 'w') as f:
            json.dump(money, f)
    except KeyError:
        money[message.author.name] = 1

    for word in filtered_words:
        if word in msgcontent.lower():
            await message.delete()
            role = discord.utils.get(message.guild.roles, name="Moderators")
            await channel.send('You said a filtered word! Let me get my ban hammer...')
            time.sleep(3)
            await channel.send('...')
            time.sleep(3)
            await channel.send(
                '''I can\'t find my ban hammer. I\'ll leave you with a warning this time, but next time, I\'ll be more 
                serious.''')
            time.sleep(3)
            await channel.send('{0.mention}, did you catch that?'.format(role))
    if message.author == client.user:
        return
    log = client.get_channel(bot_logs)
    await log.send(
        '`' + message.author.name + " sent this in " + message.channel.name + ':`\n' + message.content + '\n')
    if not message.content.startswith(prefix + "iagree") and message.channel.name == "rules":
        await message.delete()

    if message.content.startswith(prefix + 'ping'):
        await message.channel.send('Pong!')
    if message.content.startswith(prefix + 'help'):
        await message.channel.send('''
Command Prefix: ''' + prefix + '''
List of Commands:
chemsearch - [name of chemical] [(optional) number of results to print; defaults to 10] - Searches PubChem for the specified chemical.
dosupdates - N/A - Get latest updates about ChemMixer DOS.
eval - [expression] - evaluates the given expression.
ping - N/A - Sample command.
randnum - [two numbers separated by a dash (-)] - gives a random integer between the two specified numbers.
updates - N/A - Get the latest updates about ChemMixer.
verinfo - N/A - Get version information.
wikipedia - [article name] - Searches Wikipedia for the specified article name.
        ''')

    if message.content.startswith(prefix + 'verinfo'):
        await message.channel.send('''Current Version: 0.5.0
Upcoming Version: 0.5.1''')

    if message.content.startswith(prefix + 'eval'):
        evalstr = message.content
        evalstr = evalstr.replace(prefix + 'eval', '')
        await message.channel.send('The answer is: ' + str(eval(evalstr.strip())))

    if message.content.startswith(prefix + 'randnum'):
        msgcontent = message.content
        msgcontent = msgcontent.replace(prefix + 'randnum', '').strip()
        msgcontent = msgcontent.split('-')
        await message.channel.send(
            'Your random number is: ' + str(random.randint(int(msgcontent[0]), int(msgcontent[1]))))

    if message.content.startswith(prefix + 'updates'):
        await message.channel.send('''
*-* Updates Bulletin *-*
ChemMixer v0.5.2 (Upcoming)
-------------------------
+Russian translation

ChemMixer v0.5.1 (Upcoming)
-------------------------
+GUI changes
+Bugfix

ChemMixer v0.5.0
-------------------------
+GUI changes
+Amount indicator
+Reaction tweaks
+Bugfixes
+State of matter algorithm tweaks
+Aqueous solutions
+Advanced exception catching
+Chloramine reaction
+Tutorial
+Function moves
-Frame inheritances

ChemMixer v0.4.1 
-------------------------
+Bugfixes

ChemMixer v0.4.0 
-------------------------
+Lithium and Fluorine
+Bugfixes
+GUI
+Credits
+Logo
+Categories
+Modding editor
+Easter egg
-Numerical selection
-Most text
-Discovery mode
-Numerical selection

ChemMixer v0.3.0
-------------------------
+Aluminum derivatives
+Bugfixes
+Credits

ChemMixer v0.2.2
-------------------------
+Bugfixes''')
    if message.content.startswith(prefix + 'dosupdates'):
        await message.channel.send('''
*-* Updates Bulletin N.1 31/05/2019 *-*
ChemMixer v0.4.0 (DOS)
-------------------------
+Minus memory use
+Arrow keys navigation
+Better UI
+Compatible with all Text-mode compatible graphic cards/drivers
+Tested on MS-DOS 6.22
-Narrow menu
+Scrollbar (WIP)''')

    if message.content.startswith(prefix + 'wikipedia'):
        msgcontent = message.content
        msgcontent = msgcontent.replace(prefix + 'wikipedia', '').strip()
        msgcontent = cap_first_letter(msgcontent.replace(' ', '_'))
        await message.channel.send('https://en.wikipedia.org/wiki/' + msgcontent)

    if message.content.startswith(prefix + 'iagree'):
        if message.channel.name == "rules":
            await message.delete()
            role = discord.utils.get(message.guild.roles, name="Apprentices")
            await message.author.add_roles(role)
            await message.channel.send("You can now use the rest of the server.", delete_after=30)

    if message.content.startswith(prefix + 'chemsearch'):
        vals = 10
        msgcontent = message.content
        msgcontent = msgcontent.replace(prefix + 'chemsearch', '').strip()
        msgcontent = msgcontent.split(' ')
        try:
            vals = int(msgcontent[-1])
            args = 2
        except ValueError:
            args = 1
        if args == 2:
            msgcontent = msgcontent[:-1]
        msgcontent = '_'.join(msgcontent)
        page = html_request(
            'https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound/' + msgcontent + '/json?limit=' + str(vals))
        soup = BeautifulSoup(page, 'html.parser')
        chemdict = json.loads(str(soup))
        chemlist = chemdict["dictionary_terms"]["compound"]
        ans = "Here are the PubChem search results:```\n"
        for chem in chemlist:
            ans += chem + '\n'
        ans += '```'
        await message.channel.send(ans)

    if message.content.startswith(prefix + 'atoms'):
        await message.channel.send(
            "{0.name}, you have {1} atoms.".format(message.author, money[message.author.name]))

    if message.content.startswith(prefix + 'atomfile') and "Moderators" in [y.name for y in message.author.roles]:
        with open("money.json", 'r') as f:
            await message.channel.send(file=discord.File(fp=f, filename="money.json"))


@client.event
async def on_message_delete(message):
    log = client.get_channel(bot_logs)
    await log.send(
        '`' + message.author.name + " deleted this in " + message.channel.name + ':`\n' + message.content + '\n')


@client.event
async def on_message_edit(before, after):
    log = client.get_channel(bot_logs)
    await log.send(
        '`' + before.author.name + " edited a message from:`\n" + before.content + "\n` to `\n" + after.content +
        "\n`in " + before.channel.name + "`")


@client.event
async def on_member_join(member):
    channel = client.get_channel(554716924215558158)
    chan = client.get_channel(583366808539496448)
    await channel.send(
        "Welcome " + member.mention + " to the ChemMixer Official server! To get started, go to " + chan.mention + '.')


@client.event
async def on_member_remove(member):
    channel = client.get_channel(554716924215558158)
    await channel.send("See you later " + member.mention + '.')


client.run('NTU0NzIyODU4OTc5NDI2MzI0.XPXAng._7EcJgjlWKEaxf04-RI1JTHbt_s')
