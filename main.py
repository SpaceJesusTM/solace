import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

if __name__ == "__main__":
    client.run('MTAzODQ4MjAwOTU0MDAxMDA5OA.GibVJb.cIdNMgAt6n5xe5RpAJPPCh4Xn4ZqRcYqvDzlME')