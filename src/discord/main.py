import sys
import discord, asyncio
from discord.ext import commands
import random
from src.lib.character import Character
from src.api.dnd5eapi.client import Client

token = sys.argv[1]
if token is None:
    print('No token provided')
    exit(1)

client = Client()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)

_character = None
@bot.event
async def on_ready():
    print('Logged on as', bot.user)

def _class_list_message():
    msg = '```'
    for c in client.list_classes():
        msg += c.name + '\n'
    msg += '```'
    return msg

@bot.command()
async def roll(ctx, dice:str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
    
@bot.command()
async def ronnied(ctx):
    drink = random.randint(1,3)
    if drink == 1:
        await ctx.send('That\'s a drink')
    elif drink == 2:
        await ctx.send('Pass a drink')
    elif drink == 3:
        await ctx.send('Social!')

@bot.command()
async def create(ctx):
    await ctx.send('What is your character\'s name?')
    def check(m):
        return m.channel == ctx.channel
    msg = await bot.wait_for('message', check=check)
    name = msg.content
    _character = Character(name)
    await ctx.send('Choose from the following classes')
    await ctx.send(_class_list_message())
    def check(m):
        return m.channel == ctx.channel
    msg = await bot.wait_for('message', check=check)
    class_name = msg.content
    _character.create({'class': class_name})
    
    await ctx.send('Your character is named ' + _character.name + ' and is a ' + _character.get_class().name)

@bot.command()
async def randomchar(ctx):
    races = client.list_races()
    classes = client.list_classes()

    channel = await bot.fetch_channel(ctx.channel.id)
    name_choices = []
    blacklisted_names = ['dnd53-bot', 'FredBoatPatron']
    
    for member in channel.members:
        if member.name not in blacklisted_names:
            name_choices.append(member.name)

    choices = []
    msgData = '```'
    for i in range(4):
        roll = random.randint(0, len(name_choices)-1)
        name = name_choices[roll]
        del name_choices[roll:roll+1]

        roll = random.randint(0, len(races)-1)
        race = races[roll]
        del races[roll:roll+1]

        roll = random.randint(0, len(classes)-1)
        klass = classes[roll]
        del classes[roll:roll+1]
        choices.append({'name': name, 'class': klass, 'race': race})

        msgData += str(i+1) + ': ' + name + ' the ' + race.name + ' ' + klass.name + '\n'

    votes = {
        '1️⃣': 0,
        '2️⃣': 0,
        '3️⃣': 0,
        '4️⃣': 0
    }
    emoji_index = {
        '1️⃣': 0,
        '2️⃣': 1,
        '3️⃣': 2,
        '4️⃣': 3
    }

    emoji_names = [
        '1️⃣',
        '2️⃣',
        '3️⃣',
        '4️⃣'
    ]
    msgData += '```'
    msg = await ctx.send('Select one of the following characters:\n' + msgData)
    for i in range(4):
        await msg.add_reaction(emoji_names[i])

    def check(reaction, user):
        print(reaction.emoji)
        print(user.name)
        return user == ctx.author and str(reaction.emoji) in emoji_names

    selected = {}
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            print(votes)

            for key, vote in votes.items():
                if vote == max(votes.values()):
                    selected = choices[emoji_index[key]]
                    break
            break
        else:
            await ctx.send('Vote registered')
            votes[reaction.emoji] += 1       

    char = Character(selected['name'])
    char.create({'race': selected['race'].key, 'class': selected['class'].key})

    await ctx.send(f"This is the tale of {char}")

bot.run(token)
