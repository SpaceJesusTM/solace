import discord
from discord.ext import commands

class channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def new_text_channels(self, ctx, channel_name, num_channels):
        for i in range(int(num_channels)):
            await ctx.guild.create_text_channel(channel_name + str(i))

        await ctx.send(num_channels + " new text channels were made!")


    @commands.command()
    async def new_voice_channels(self, ctx, channel_name, num_channels):
        for i in range(int(num_channels)):
            await ctx.guild.create_voice_channel(channel_name + str(i))

        await ctx.send(num_channels + " new voice channels were made!")


    @commands.command()
    async def delete_channels(self, ctx, channel_name):
        count = 0
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name.startswith(channel_name):
                    count += 1
                    await channel.delete()

        await ctx.send(str(count) + " channels were deleted!")