from discord.enums import ActivityType
from discord import Activity, Member, client, Intents, File, PermissionOverwrite
from discord.utils import get
from os import getenv, path
from dotenv import load_dotenv
from discord.ext import commands
import json, requests
from e621 import E621
from random import choice
from io import BytesIO
from asyncio import TimeoutError
from time import sleep
from os import remove

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
async def troll(ctx, member: Member, time: int, *, tags):
    if ctx.author.id not in [239376339960856577, 423943556927848449]:
        return
    ctx.send("wait for api response")
    api = E621()
    posts = api.posts.search(tags.split(', ') + ['rating:e'])
    post = choice(posts)
    filename = f"{post.id}.{post.file.ext}"
    with open(filename, "wb") as file:
        file.write(requests.get(post.file.url).content)

    with open(filename, 'rb') as f:
        filebytes = f.read()
    dcfile = File(BytesIO(filebytes), filename=filename)

    await ctx.send('jest git? potwierdź pisząc "t"', file=dcfile)

    try:
        await client.wait_for('message', timeout=5.0, check=lambda m: m.author.id == ctx.author.id and m.content.lower() == 't')
    except TimeoutError:
        await ctx.send('aborting.')
    else:
        with open(filename, 'rb') as f:
            filebytes = f.read()
        dcfile = File(BytesIO(filebytes), filename=filename)
        await ctx.send('👍')
        overwrites = {ctx.guild.default_role: PermissionOverwrite(read_messages=False), member: PermissionOverwrite(read_messages=True)}
        chan = await ctx.guild.create_text_channel(name=member.display_name, overwrites=overwrites)
        await chan.send(member.mention, file=dcfile)
        sleep(time)
        await chan.delete()
    
    remove(filename)

@client.command()
async def crole(ctx, colour, *, name: str,):
    with open('role.json', 'r') as file:
        rolejson = json.loads(file.read())
    
    for i in rolejson:
        if i == str(ctx.author.id):
            await ctx.send('Juź masz role')
            return

    bot_role = get(ctx.guild.roles, name=client.user.name)
    rola = await ctx.guild.create_role(name=name, colour=int(colour, 16))
    await rola.edit(position=bot_role.position-1)
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
