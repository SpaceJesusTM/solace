import discord
from discord.ext import commands
from twilio.rest import Client


class announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announce_channel = ""

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_announce(self, ctx, channel):
        self.announce_channel = channel
        await ctx.send("Announcement channel set to " + channel)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def text_list(self, ctx):
        total_contacts = 0
        for user in contacts:
            total_contacts += 1
            await ctx.send(user + " : " + contacts[user])
        await ctx.send("Total contacts: " + str(total_contacts))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, lvl, body):
        if self.announce_channel == "":
            await ctx.send("Please set the announcement channel first!")
        
        channel = discord.utils.get(ctx.guild.channels, name=self.announce_channel)
        if lvl == "1":
            await channel.send('@everyone ' + body)
            # await self.announce_channel.send(body)
            await ctx.send(f"Announcement sent via {self.announce_channel}!")
        elif lvl == "2":
            for user in contacts:
                send_sms(body, contacts[user])
            await ctx.send("Announcement sent via text!")
        elif lvl == "3":
            await channel.send('@everyone ' + body)
            for user in contacts:
                send_sms(body, contacts[user])
            await ctx.send(f"Announcement sent via text and {self.announce_channel}!")
        else:
            await ctx.send("Invalid level!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def send_pm(self, ctx, user, body):
        if user in contacts:
            send_sms(body, contacts[user])
            await ctx.send(f"Message sent to {user}!")
        else:
            await ctx.send("Invalid user!")

    @commands.command()
    async def add_number(self, ctx, num):
        name = ctx.message.author
        contacts[name.name] = num
        await ctx.send(str(name)[:-5] + ", your number (" + num + ") has been registered to receive texts!")
    
    @commands.command()
    async def remove_number(self, ctx):
        name = ctx.message.author
        contacts.pop(name.name)
        await ctx.send(str(name)[:-5] + ", you will no longer receive texts.")

# Your Account SID from twilio.com/console
account_sid = "AC9f7e889c258470bae55da4c8e326abc0"
# Your Auth Token from twilio.com/console
auth_token = "35da471ee57c8e5e699e77ef26dd4290"


# Empty dictionary to store usernames and corresponding phone numbers
contacts = {}


def send_sms(body, to_number):
    text_me = Client(account_sid, auth_token)

    message = text_me.messages.create(
        to=to_number,
        from_="+12538678817",
        body=body)

    return message
