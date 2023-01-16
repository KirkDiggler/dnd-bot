import sys
import discord, asyncio
from discord.ext import commands
import random
from src.discord.poll import UserPoll
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

    # mutates input and removes the item selected
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

        @self.event
        async def on_message(message):
            if message.author == self.user:
                return

            responses = ['you know it bro', '💯', 'right back at ya bro', 'this guy gets it']
            if message.content.startswith('thank\'s ronnie'):
                await message.channel.send(random.choice(responses))
            elif message.content.startswith('thanks ronnie'):
                await message.channel.send(random.choice(responses))
            elif message.content.startswith('thanks Ronnie'):
                await message.channel.send(random.choice(responses))
            elif message.content.startswith('Thanks Ronnie'):
                await message.channel.send(random.choice(responses))

            await self.process_commands(message)

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

            channel = await self.fetch_channel(ctx.channel.id)
            name_choices = []
            emoji_index = {
                '🇦': 0,
                '🇧': 1,
                '🇨': 2,
                '🇩': 3,
                '🇪': 4,
                '🇫': 5,
                '🇬': 6,
                '🇭': 7,
                '🇮': 8,
                '🇯': 9,
                '🇰': 10,
                '🇱': 11,
                '🇲': 12,
                '🇳': 13,
                '🇴': 14,
                '🇵': 15,
                '🇶': 16,
                '🇷': 17,
                '🇸': 18,
                '🇹': 19,
                '🇺': 20,
            }

            emoji_names = [
                '🇦',
                '🇧',
                '🇨',
                '🇩',
                '🇪',
                '🇫',
                '🇬',
                '🇭',
                '🇮',
                '🇯',
                '🇰',
                '🇱',
                '🇲',
                '🇳',
                '🇴',
                '🇵',
                '🇶',
                '🇷',
                '🇸',
                '🇹',
                '🇺',
            ]

            for member in channel.members:
                if not member.bot:
                    name_choices.append(member.name)

            choices = []
            msgData = '```'
            for i in range(4):
                choice = self.get_random_char(name_choices, races, classes)
                choices.append(choice)

                msgData += emoji_names[i] + ': ' + choice['name'] + ' the ' + choice['race'].name + ' ' + choice['class'].name + '\n'

            msgData += '```'
            msg = await ctx.send('Select one of the following characters:\n' + msgData)
            for i in range(4):
                await msg.add_reaction(emoji_names[i])

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in emoji_names

            selected = {}

            char_votes = UserPoll(votes_per_user=1)
            while True:
                try:
                    print('reaction_add')
                    reaction, user = await self.wait_for('reaction_add', timeout=5.0)
                except asyncio.TimeoutError:
                    winners = char_votes.get_winners()
                    if len(winners) == 0:
                        await ctx.send('No votes detected')
                        return

                    selected = choices[emoji_index[winners[0]]]
                    break
                else:
                    print("voting")
                    if char_votes.vote(user, reaction.emoji) == False:
                        await msg.remove_reaction(char_votes.pop_vote(user), user)
                
                try:
                    reaction, user = await self.wait_for('reaction_remove', timeout=5.0, check=check)
                except:
                    pass
                else:
                    char_votes.remove_vote(user, reaction.emoji)

            char = Character(selected['name'])
            char.create({'race': selected['race'].key, 'class': selected['class'].key})
            
            await ctx.send(f"This is the tale of {char}")

            # for choice in char.proficiency_choices:
            #     msgData = '```'
            #     msgData += 'Choose ' + str(choice.choose) + ' from the following:\n'

            #     for i in range(len(choice.option_list)):
            #         msgData += emoji_names[i] + ': ' + choice.option_list[i].item.name + '\n'
                
            #     msgData += '```'
            #     msg = await ctx.send(msgData)
            #     for i in range(len(choice.option_list)):
            #         await msg.add_reaction(emoji_names[i])
            #     prof_votes = UserVote(votes_per_user=choice.choose)
            #     winners = []
            #     while True:
            #         try:
            #             reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
            #         except asyncio.TimeoutError:
            #             winners = prof_votes.get_winners()
            #             print(winners)

            #             break
            #         else:
            #             if prof_votes.vote(user, reaction.emoji) == False:
            #                 prof_votes.remove_vote(user, reaction.emoji)

            #             prof_votes.vote(user, reaction.emoji)
                            
            #     for winner in winners:
            #         await ctx.send(f'{choice.option_list[emoji_index[winner]].item.name} chosen')

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
