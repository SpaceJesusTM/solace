import discord
import asyncio
import os
import sys
from discord.ext import commands
from cogs import discussion, announcements, channels, mail, chat

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.add_cog(discussion.discussion(bot))
    await bot.add_cog(announcements.announcements(bot))
    await bot.add_cog(channels.channels(bot))
    await bot.add_cog(mail.mail(bot))
    await bot.add_cog(chat.chat(bot))
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == 'general':
                text_channel_list.append(channel)
    for channel in text_channel_list:
        await channel.send("Bot is ready!")
    activity = discord.Game(name="$command_list for info...", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Bot is ready!')


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@bot.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send("Bot is restarting this may take a few moments...")
    restart_program()

if __name__ == "__main__":
    bot.run('TOKEN')
