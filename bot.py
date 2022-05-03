import discord
import itertools as it
import math
from discord.ext import commands
import os

token = os.environ.get('ONE_TO_ONE_TOKEN')
intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

client = commands.Bot(command_prefix='q.', case_insensitive=True, intents=intents)


#gets number of combinations
def nCr(n,r):
    return int(math.factorial(n)/(math.factorial(r)*math.factorial(n-r)))


#returns the item from the name and a list
def get_x(name, the_set):
    for r in the_set:
        if r.name==name:
            print(r.name)
            return r
    print('Couldnt find one mate')


def llama(member):
    if member.nick:
        return member.nick
    return member.name


@client.event
async def on_ready():
    print('Ok.')


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command(aliases = ["1-to-1","one-to-one"])
@commands.has_permissions(administrator=True)
async def create(ctx, role_name=None, name='1-to-1s'):
    if role_name not in [role.name for role in ctx.guild.roles]:
        await ctx.send('*Cannot find role for "**'+role_name+'**".*')
        return
    target = get_x(role_name, ctx.guild.roles)

    if len(target.members) > 22:
        await ctx.send("***"+target.name+"** has too many members (max **22**).*")
        return

    loading = await ctx.send("```Building...```")
    duos = it.combinations(target.members,2)
    combos = nCr(len(target.members), 2)
    cats = []

    if combos > 50:
        for i in range(combos//50+1):
            cats.append(await ctx.guild.create_category(name+"-"+str(i+1)))
    else:
        cats.append(await ctx.guild.create_category(name))

    for index, d in enumerate(duos):
        this_un = await ctx.guild.create_text_channel(llama(d[0])+'-'+llama(d[1]), category=cats[index//50])
        await this_un.set_permissions(d[0], send_messages=True, read_messages=True)
        await this_un.set_permissions(d[1], send_messages=True, read_messages=True)
        await this_un.set_permissions(ctx.guild.default_role, read_messages=False)

    await loading.edit(content="```Finished.```")


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, category_name):
    if category_name not in [cat.name for cat in ctx.guild.categories]:
        await ctx.send('*Cannot find category for "**'+category_name+'**".')
        return
    target = get_x(category_name, ctx.guild.categories)
    for c in target.channels:
        await c.delete()
    await target.delete()

client.run(token)
