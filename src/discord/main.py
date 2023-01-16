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
intents.reactions = True


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True

        super().__init__(command_prefix='/', intents=intents)
        self._character = None

        self._events()
        self._commands()

    def get_random_char(self, names, races, classes):
        roll = random.randint(0, len(names)-1)
        name = names[roll]
        del names[roll:roll+1]

        roll = random.randint(0, len(races)-1)
        race = races[roll]
        del races[roll:roll+1]

        roll = random.randint(0, len(classes)-1)
        klass = classes[roll]
        del classes[roll:roll+1]

        return {'name': name, 'class': klass, 'race': race}

    def _events(self):
        @self.event
        async def on_ready():
            print('Logged on as', self.user)

    def _commands(self):
        @self.command()
        async def roll(ctx, dice:str):
            """Rolls a dice in NdN format."""
            try:
                rolls, limit = map(int, dice.split('d'))
            except Exception:
                await ctx.send('Format has to be in NdN!')
                return

            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(result)
            
        @self.command()
        async def ronnied(ctx):
            drink = random.randint(1,3)
            if drink == 1:
                await ctx.send('That\'s a drink')
            elif drink == 2:
                await ctx.send('Pass a drink')
            elif drink == 3:
                await ctx.send('Social!')

        @self.command()
        async def randomchar(ctx):
            races = client.list_races()
            classes = client.list_classes()

            channel = await bot.fetch_channel(ctx.channel.id)
            name_choices = []

            for member in channel.members:
                if not member.bot:
                    name_choices.append(member.name)

            choices = []
            msgData = '```'
            for i in range(4):
                choice = self.get_random_char(name_choices, races, classes)
                choices.append(choice)

                msgData += str(i+1) + ': ' + choice['name'] + ' the ' + choice['race'].name + ' ' + choice['class'].name + '\n'

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
                return user == ctx.author and str(reaction.emoji) in emoji_names

            selected = {}
            user_votes = {}

            def find_winner(votes):
                for key, vote in votes.items():
                    if vote == max(votes.values()):
                        return  choices[emoji_index[key]]

            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
                except asyncio.TimeoutError:

                    selected = find_winner(votes)

                    break
                else:
                    if user.name in user_votes:
                        pervios_vote = user_votes[user.name]
                        await msg.remove_reaction(user_votes[user.name], user)
                        votes[pervios_vote] -= 1       

                    user_votes[user.name] = reaction.emoji

                    votes[reaction.emoji] += 1       

            char = Character(selected['name'])
            char.create({'race': selected['race'].key, 'class': selected['class'].key})
            
            await ctx.send(f"This is the tale of {char}")

            for choice in char.proficiency_choices:
                msgData = '```'
                msgData += 'Choose ' + str(choice.choose) + ' from the following:\n'

                for i in range(len(choice.option_list)):
                    msgData += str(i+1) + ': ' + choice.option_list[i].item.name + '\n'
                
                msgData += '```'

                while True:
                    try:
                        await ctx.send(msgData)
                        background = await bot.wait_for('message', timeout=5.0, check=lambda m: m.author == ctx.author)
                    except asyncio.TimeoutError:
                        await ctx.send('Coming Soon')
                        break
                    else:
                        
                        break


bot = DiscordBot()


# _character = None
# @bot.event
# async def on_ready():
#     print('Logged on as', bot.user)

# def _class_list_message():
#     msg = '```'
#     for c in client.list_classes():
#         msg += c.name + '\n'
#     msg += '```'
#     return msg

# @bot.command()
# async def roll(ctx, dice:str):
#     """Rolls a dice in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return

#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)
    
# @bot.command()
# async def ronnied(ctx):
#     drink = random.randint(1,3)
#     if drink == 1:
#         await ctx.send('That\'s a drink')
#     elif drink == 2:
#         await ctx.send('Pass a drink')
#     elif drink == 3:
#         await ctx.send('Social!')

# @bot.command()
# async def create(ctx):
#     await ctx.send('What is your character\'s name?')
#     def check(m):
#         return m.channel == ctx.channel
#     msg = await bot.wait_for('message', check=check)
#     name = msg.content
#     _character = Character(name)
#     await ctx.send('Choose from the following classes')
#     await ctx.send(_class_list_message())
#     def check(m):
#         return m.channel == ctx.channel
#     msg = await bot.wait_for('message', check=check)
#     class_name = msg.content
#     _character.create({'class': class_name})
    
#     await ctx.send('Your character is named ' + _character.name + ' and is a ' + _character.get_class().name)

# @bot.command()
# async def randomchar(ctx):
#     races = client.list_races()
#     classes = client.list_classes()

#     channel = await bot.fetch_channel(ctx.channel.id)
#     name_choices = []

#     for member in channel.members:
#         if not member.bot:
#             name_choices.append(member.name)

#     choices = []
#     msgData = '```'
#     for i in range(4):
#         roll = random.randint(0, len(name_choices)-1)
#         name = name_choices[roll]
#         del name_choices[roll:roll+1]

#         roll = random.randint(0, len(races)-1)
#         race = races[roll]
#         del races[roll:roll+1]

#         roll = random.randint(0, len(classes)-1)
#         klass = classes[roll]
#         del classes[roll:roll+1]
#         choices.append({'name': name, 'class': klass, 'race': race})

#         msgData += str(i+1) + ': ' + name + ' the ' + race.name + ' ' + klass.name + '\n'

#     votes = {
#         '1️⃣': 0,
#         '2️⃣': 0,
#         '3️⃣': 0,
#         '4️⃣': 0
#     }
#     emoji_index = {
#         '1️⃣': 0,
#         '2️⃣': 1,
#         '3️⃣': 2,
#         '4️⃣': 3
#     }

#     emoji_names = [
#         '1️⃣',
#         '2️⃣',
#         '3️⃣',
#         '4️⃣'
#     ]
#     msgData += '```'
#     msg = await ctx.send('Select one of the following characters:\n' + msgData)
#     for i in range(4):
#         await msg.add_reaction(emoji_names[i])

#     def check(reaction, user):
#         return user == ctx.author and str(reaction.emoji) in emoji_names

#     selected = {}
#     user_votes = {}

#     def find_winner(votes):
#         for key, vote in votes.items():
#             if vote == max(votes.values()):
#                 return  choices[emoji_index[key]]

#     while True:
#         try:
#             reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
#         except asyncio.TimeoutError:

#             selected = find_winner(votes)

#             break
#         else:
#             if user.name in user_votes:
#                 pervios_vote = user_votes[user.name]
#                 await msg.remove_reaction(user_votes[user.name], user)
#                 votes[pervios_vote] -= 1       

#             user_votes[user.name] = reaction.emoji

#             votes[reaction.emoji] += 1       

#     char = Character(selected['name'])
#     char.create({'race': selected['race'].key, 'class': selected['class'].key})

#     await ctx.send(f"This is the tale of {char}")

bot.run(token)
