import discord
import asyncio
from discord.ext import commands
from cogs import discussion, announcements, channels, mail
# from cogs

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.add_cog(discussion.discussion(bot))
    await bot.add_cog(announcements.announcements(bot))
    await bot.add_cog(channels.channels(bot))
    await bot.add_cog(mail.mail(bot))
    print('Bot is ready!')

if __name__ == "__main__":
    bot.run('TOKEN')