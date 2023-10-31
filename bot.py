import discord
import itertools as it
import os
from discord.ext import commands

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

client = commands.Bot(command_prefix='q.', case_insensitive=True, intents=intents)


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
async def create(ctx, role_name=None, name='1-to-1s'):
    if role_name not in [role.name for role in ctx.guild.roles]:
        await ctx.send('*Cannot find role for "**'+role_name+'**".*')
        return
    target = get_x(role_name, ctx.guild.roles)

    if len(target.members) > 22:
        await ctx.send("***"+target.name+"** has too many members (max **22**).*")
        return

    duos = it.combinations(target.members,2)

    cat = await ctx.guild.create_category(name)
    for d in duos:
        this_un = await ctx.guild.create_text_channel(llama(d[0])+'-'+llama(d[1]), category=cat)
        await this_un.set_permissions(d[0], send_messages=True, read_messages=True)
        await this_un.set_permissions(d[1], send_messages=True, read_messages=True)
        await this_un.set_permissions(ctx.guild.default_role, read_messages=False)


@client.command()
async def clear(ctx, category_name):
    if category_name not in [cat.name for cat in ctx.guild.categories]:
        await ctx.send('*Cannot find category for "**'+category_name+'**".')
        return
    target = get_x(category_name, ctx.guild.categories)
    for c in target.channels:
        await c.delete()
    await target.delete()

client.run(os.environ.get("DISCORD_API_KEY"))
