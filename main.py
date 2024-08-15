import discord
from discord.ext import commands

# Minimal Discord bot
# Add commands as you see fit. 
# Credits: C00zzy
# The is kinda unnecessary mute/ban/kick command due to discord having it built in.
# Most moderation features are actually built into discord so implementing them here is reinventing the wheel
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Ensure to enable the members intent

houdini = commands.Bot(command_prefix='$', intents=intents)
message_cache = {} # Message cache for sniping

@houdini.event
async def on_ready():
    print("Bot is ready!")

@houdini.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument provided, sorry!")
    else:
        await ctx.send("An error occurred. This may be due to missing arguments.")

@houdini.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    if limit > 1000:
        await ctx.send("Too many messages to delete! Limit is 1000.")
        return
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"Purged {limit} messages.", delete_after=1)

@houdini.command()
async def ping(ctx):
    await ctx.send("Pong!")

@houdini.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

@houdini.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@houdini.event
async def on_message_delete(message):
    if message.author == houdini.user:
        return
    message_cache[message.channel.id] = { # Use the message cache for well cache
            'content': message.content,
            'author': message.author,
            'channel': message.channel,
    }
    print(f'{message.author} deleted message in {message.channel}: "{message.content}"')

@houdini.command()
async def snipe(ctx): # If the deleted message is in cache display when snipe command is used
    if ctx.channel.id in message_cache:
        deleted_msg = message_cache[ctx.channel.id]
        await ctx.send(f'Snipped: {deleted_msg["author"]} deleted: "{deleted_msg["content"]}" in {deleted_msg["channel"]}')
    else:
        await ctx.send("No message to snipe.")



@houdini.event
async def on_message(message):
    if message.author == houdini.user:
        return
    print(f'{message.author} said: {message.content}')
    await houdini.process_commands(message)  # This is necessary to ensure commands work after processing on_message

@houdini.event
async def on_message_edit(before, after):
    print(f'Message edited from: {before.content} to: {after.content}')

houdini.run('') # Token Here
