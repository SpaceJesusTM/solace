import discord
from discord.ext import commands
from twilio.rest import Client


class announcments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def announce(self, ctx, body):
        for user in contacts:
            send_sms(body, contacts[user])

    @commands.command()
    async def add_number(self, ctx, num):
        name = ctx.message.author
        contacts[name.name] = num
        await ctx.send(str(name)[:-5] + ", your number (" + num + ") has been registered to receive texts!")
    
    @commands.command()
    async def remove_number(self, ctx):
        name = ctx.message.author
        contacts.pop(name.name)
        print(contacts)
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
