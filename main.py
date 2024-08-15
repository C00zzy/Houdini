import discord
from discord.ext import commands

# Minimal Discord bot
# Credits: C00zzy
# This is fine for now.
# Comments by AI
# Define intents to manage the bot's interactions
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable members intent to access member-related events

# Initialize the bot with a command prefix and intents
houdini = commands.Bot(command_prefix='$', intents=intents)

# Dictionary to cache deleted messages for the snipe command
message_cache = {}

@houdini.event
async def on_ready():
    # Event triggered when the bot is ready and online
    print("Bot is ready!")

@houdini.event
async def on_command_error(ctx, error):
    # Handle command errors gracefully
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument provided, sorry!")
    else:
        await ctx.send("An error occurred. This may be due to missing arguments.")

@houdini.command()
@commands.has_permissions(manage_messages=True)  # Restrict this command to users with manage_messages permission
async def purge(ctx, limit: int):
    # Command to delete a specified number of messages from the channel
    if limit > 1000:
        await ctx.send("Too many messages to delete! Limit is 1000.")
        return
    # Purge the specified number of messages (limit + 1 to include the command message itself)
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"Purged {limit} messages.", delete_after=1)  # Confirmation message will delete after 1 second

@houdini.command()
async def ping(ctx):
    # Simple command to check if the bot is responsive
    await ctx.send("Pong!")

@houdini.command()
@commands.has_permissions(ban_members=True)  # Restrict this command to users with ban_members permission
async def ban(ctx, member: discord.Member, *, reason=None):
    # Command to ban a specified member with an optional reason
    await member.ban(reason=reason)

@houdini.command()
@commands.has_permissions(kick_members=True)  # Restrict this command to users with kick_members permission
async def kick(ctx, member: discord.Member, *, reason=None):
    # Command to kick a specified member with an optional reason
    await member.kick(reason=reason)

@houdini.event
async def on_message_delete(message):
    # Event triggered when a message is deleted
    if message.author == houdini.user:
        return  # Ignore messages deleted by the bot itself
    # Cache the deleted message's content, author, and channel
    message_cache[message.channel.id] = {
        'content': message.content,
        'author': message.author,
        'channel': message.channel,
    }
    # Print deleted message details to the console
    print(f'{message.author} deleted message in {message.channel}: "{message.content}"')

@houdini.command()
async def snipe(ctx):
    # Command to retrieve the last deleted message in the channel
    if ctx.channel.id in message_cache:
        deleted_msg = message_cache[ctx.channel.id]  # Get the cached deleted message
        await ctx.send(f'Snipped: {deleted_msg["author"]} deleted: "{deleted_msg["content"]}" in {deleted_msg["channel"]}')
    else:
        await ctx.send("No message to snipe.")  # Notify if there are no cached messages

@houdini.event
async def on_message(message):
    # Event triggered when a message is sent
    if message.author == houdini.user:
        return  # Ignore messages sent by the bot itself
    # Print the message content to the console
    print(f'{message.author} said: {message.content}')
    await houdini.process_commands(message)  # Process commands after handling the message

@houdini.event
async def on_message_edit(before, after):
    # Event triggered when a message is edited
    print(f'Message edited from: {before.content} to: {after.content}')

# Run the bot with the specified token (replace '' with your bot token)
houdini.run('')  # Token Here
