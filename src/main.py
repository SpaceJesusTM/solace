import discord
from discord.ext import commands
from cogs import discussion

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.add_cog(discussion.discussion(bot))
    print("Bot is ready.")

if __name__ == "__main__":
    bot.run('TOKEN')