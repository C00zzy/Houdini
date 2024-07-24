import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True


BotClient = commands.Bot(command_prefix='$', intents=intents)

@BotClient.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):

    if ctx.message.author.guild_permissions.manage_messages:
       await ctx.channel.purge(limit=limit + 1)
    else:
        await ctx.send("FAILURE DUE TO LACK OF PERMISSION")

@BotClient.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.message.author.guild_permissions.manage_members:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked! Member: {discord.member}')
    else:
        await ctx.send("FAILURE DUE TO LACK OF PERMISSION")
@BotClient.command()
async def into(ctx, *, member: discord.Member):
    msg = f'{member} joined on {member.joined_at} and has {len(member.roles)} roles.'
    await ctx.send(msg)

@BotClient.command()
async def insult(ctx):
    for i in range(1,100):
        await ctx.send("FUCK YOU!")

@BotClient.command()
async def hello(ctx):
    await ctx.send("Hello, World!")

class myClient(discord.Client):
    async def on_ready(self):
         print(f'Logged on as {self.user}!')


client = myClient(intents=intents)

BotClient.run("") # PUT TOKEN HERE!
