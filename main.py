from discord.enums import ActivityType
from discord import Activity
from discord.utils import find
from os import getenv, path
from dotenv import load_dotenv
from discord import client, Intents
from discord.ext import commands
import json

intents = Intents.all()

client = commands.Bot(command_prefix='.', fetch_offline_members=True, intents=intents)
client.remove_command('help')

load_dotenv('.env')

@client.event
async def on_ready():
    print(f'logged in as {client.user.name}')
    await client.change_presence(activity=Activity(name='.help', type=ActivityType.watching))
    if not path.exists('role.json'):
        with open('role.json', 'w') as file:
            file.write('{}')

@client.command()
async def crole(ctx, colour, *, name: str,):
    with open('role.json', 'r') as file:
        rolejson = json.loads(file.read())
    
    for i in rolejson:
        if i == str(ctx.author.id):
            await ctx.send('Juź masz role')
            return

    bot_role = find(ctx.guild.roles, name=client.user.name)
    rola = await ctx.guild.create_role(name=name, colour=int(colour, 16), position=bot_role.position-1)
    rolejson[ctx.author.id] = rola.id
    await ctx.author.add_roles(rola)
    await ctx.send(f'Pomyślnie stworzyłem i nadałem Ci rolę {rola.name}')

    with open('role.json', 'w') as file:
        file.write(json.dumps(rolejson))

@client.command()
async def erole(ctx, colour, *, name):
    with open('role.json', 'r') as file:
        rolejson = json.loads(file.read())

    if not str(ctx.author.id) in rolejson:
        await ctx.send('Nie masz jeszcze roli')
        return
    
    rola = ctx.guild.get_role(rolejson[str(ctx.author.id)])
    
    await rola.edit(name=name, colour=int(colour, 16))
    await ctx.send('Done')

@client.command()
async def drole(ctx):
    with open('role.json', 'r') as file:
        rolejson = json.loads(file.read())

    if not str(ctx.author.id) in rolejson:
        await ctx.send('Nie masz jeszcze roli')
        return
    
    rola = ctx.guild.get_role(rolejson[str(ctx.author.id)])

    name = rola.name
    await rola.delete()
    del rolejson[str(ctx.author.id)]
    await ctx.send(f'Usunąłem rolę {name}')
    with open('role.json', 'w') as file:
        file.write(json.dumps(rolejson))

@client.command()
async def help(ctx):
    await ctx.send(
        """
crole - tworzy Ci role (.crole <kolor w hex> <nazwa roli>)
erole - edytuje twoją role (.erole <kolor w hex> <nazwa roli>)
drole - usuwa twoją role
        """
    )
    
client.run(getenv('TOKEN'))

# Made By Gilbert#4040 2022 