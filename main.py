import discord
from discord.ext import commands

# Minimal Discord bot
# Add commands as you see fit. 
# Credits: C00zzy
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Ensure to enable the members intent

houdini = commands.Bot(command_prefix='$', intents=intents)

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
    await ctx.send(f"Purged {limit} messages.", delete_after=5)

@houdini.command()
async def ping(ctx):
    await ctx.send("Pong!")

@houdini.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked member: {member}. Reason: {reason}')

@houdini.event
async def on_message(message):
    if message.author == houdini.user:
        return
    await houdini.process_commands(message)  # This is necessary to ensure commands work after processing on_message

@houdini.event
async def on_message_edit(before, after):
    print(f'Message edited from: {before.content} to: {after.content}')

houdini.run('') # Add tokens here.
