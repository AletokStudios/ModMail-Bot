import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        # Create an embed with the user's message
        embed = discord.Embed(
            title='ModMail Message',
            description=message.content,
            color=discord.Color.blue()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)

        # Check if there is an image attached to the message
        if message.attachments:
            image_url = message.attachments[0].url
            embed.set_image(url=image_url)

        # Send the embed to a modmail channel (replace 'modmail-channel-id' with your channel ID)
        modmail_channel = bot.get_channel(123456789)  # Replace with your channel ID
        if not modmail_channel:
            await message.author.send('Modmail channel not found.')
            return

        await modmail_channel.send(embed=embed)

        await message.author.send('Your message has been sent to the moderators.')

    await bot.process_commands(message)

@bot.command()
async def reply(ctx, user: discord.User, *, response: str):
    # Check if the message is sent in the modmail channel or by a moderator
    modmail_channel_id = 123456789  # Replace with your modmail channel ID
    is_modmail_channel = ctx.channel.id == modmail_channel_id
    is_moderator = any(role.name == 'Moderator' for role in ctx.author.roles)  # Customize as needed

    if not is_modmail_channel or not is_moderator:
        await ctx.send('You can only use this command in the modmail channel as a moderator.')
        return

    # Send a response to the specified user
    try:
        await user.send(response)
        await ctx.send(f'Response sent to {user.mention}.')
    except discord.HTTPException:
        await ctx.send('Failed to send a response to the user.')

bot.run('YOUR-BOT-TOKEN')