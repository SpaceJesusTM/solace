import discord
from discord.ext import commands

class mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mail_channel = ""

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mail(self, ctx, channel):
        self.mail_channel = channel
        await ctx.send("Mail channel set to " + channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        empty_array = []
        modmail_channel = discord.utils.get(self.bot.get_all_channels(), name=self.mail_channel) 
        if message.author == self.bot.user:
            return
       
        if str(message.channel.type) == "private":
            if self.mail_channel == "":
                return
            if message.attachments != empty_array:
                files = message.attachments
                await modmail_channel.send("[" + message.author.display_name + "]")
                for file in files:
                    await modmail_channel.send(file.url)
            else:
                await modmail_channel.send("[" + message.author.display_name + "] " + message.content)

        elif str(message.channel) == self.mail_channel and message.content.startswith("<"):
            if self.mail_channel == "":
                return

            member_object = message.mentions[0]
            if message.attachments != empty_array:
                files = message.attachments
                await member_object.send("[" + message.author.display_name + "]")
                for file in files:
                    await member_object.send(file.url)

            else:
                index = message.content.index(" ")
                string = message.content
                mod_message = string[index:]
                await member_object.send("[" + message.author.display_name + " ]" + mod_message)
