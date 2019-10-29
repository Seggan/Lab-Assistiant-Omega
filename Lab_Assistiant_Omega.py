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
        if word in msgcontent.lower() and not message.channel.name == "bot-logs":
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
            await channel.send(f'{role.mention}, did you catch that?')
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
        await message.channel.send('''Current Version: 0.5.2
Upcoming Version: 0.5.3''')

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
ChemMixer v0.5.3 (Upcoming)
-------------------------
+Code Restructuring
+Bugfix
+Tools
+2 beakers
-Arrow key temperature changing

ChemMixer v0.5.2
-------------------------
+Code Restructuring
+Music
+Arrow key temperature changing
+Enzymes
-Helium and dihelium

ChemMixer v0.5.1
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
*-* Updates Bulletin *-*
ChemMixer v0.4.0 (DOS)
-------------------------
+Minus memory use
+Arrow keys navigation
+Better UI
+Compatible with all Text-mode compatible graphic cards/drivers
+Tested on MS-DOS 6.22
+Scrollbar (WIP)
-Narrow menu''')

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
            "{0.mention}, you have {1} atoms.".format(message.author, money[message.author.name]))

    if message.content.startswith(prefix + 'atomfile') and "Moderators" in [y.name for y in message.author.roles]:
        with open("money.json", 'r') as f:
            file = f.read()
            await message.channel.send(file)

    if message.content.startswith(prefix + 'buy'):
        if message.content.strip() == prefix + 'buy':
            pass
        else:
            what = message.content.split(' ')[1]
            author = message.author.name
            failed = False
            with open("money.json", 'r') as f:
                money = json.load(f)
            if what.strip() == "alpha":
                if money[author] >= 10000:
                    role = discord.utils.get(message.guild.roles, name="Alpha Testers")
                    await message.author.add_roles(role)
                    money[author] -= 10000
                    with open("money.json", 'w') as f:
                        json.dump(money, f)
                    await message.channel.send("You have successfully bought the Alpha Testers role.")
                else:
                    failed = True

            if failed:
                await message.channel.send("You do not have enough money to buy that.")

    if message.content.startswith(prefix + 'slots'):
        author = message.author.name
        first = random.randint(1, 6)
        second = random.randint(1, 6)
        with open("money.json", 'r') as f:
            money = json.load(f)
        if money[author] >= 50:
            money[author] -= 50
            with open("money.json", 'w') as f:
                json.dump(money, f)
            await message.channel.send("Spinning the slot machine for 50 atoms:")
            time.sleep(1)
            await message.channel.send("First number: " + str(first))
            time.sleep(2)
            await message.channel.send("Second number: " + str(second))
            time.sleep(1)
            if first == second:
                await message.channel.send("You have won 500 atoms!")
                money[author] += 500
                with open("money.json", 'w') as f:
                    json.dump(money, f)
            else:
                await message.channel.send("Sorry, but you have lost. Better luck next time.")

    if message.content.startswith(prefix + 'send') and message.channel.name == "bot-control-panel":
        bad_channels = [
            "announcements",
            "dos-announcements",
            "bot-logs",
            "rules",
            "link",
            "faq",
            "new-videos"
        ]
        argss = message.content.split(' ')[1:]
        try:
            id = int(argss[0])
        except ValueError:
            await message.channel.send("Invalid channel id.")
            return
        text = ' '.join(argss[1:])
        chan = client.get_channel(id)
        if chan.name in bad_channels:
            await message.channel.send("I cannot post in that channel.")
        else:
            await chan.send(text)


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


client.run('NTU0NzIyODU4OTc5NDI2MzI0.XUYq4A.QD1fBWSdN0qGf_dTVbhfYcpv-10')
