from typing import Optional
import discord
from discord.ext import commands
from neuralintents import GenericAssistant

# global embed variables
help_embed = discord.Embed(title='All Commands', color=discord.Colour.gold())
help_embed.add_field(name='Set-up (before usage): `!restart`',
                     value="ADMIN CMD. Restart the bot before first use, or if bugs are encountered.", inline=False)
help_embed.add_field(name='Set-up (before usage): `!set_announce <channel>`',
                     value="ADMIN CMD. Sets the announcement channel.", inline=False)
help_embed.add_field(name='Set-up (before usage): `!set_chat <channel>`',
                     value="ADMIN CMD. Sets the chat with Solace channel.", inline=False)
help_embed.add_field(name='Set-up (before usage): `!set_threads <channel>`',
                     value="ADMIN CMD. Sets the threads post channel.", inline=False)
help_embed.add_field(name='Set-up (before usage): `!set_mail <channel>`',
                     value="ADMIN CMD. Sets the instructor mail channel.", inline=False)
help_embed.add_field(name='Announcements: `!announce <level> <message>`',
                     value="ADMIN CMD. Send a text to the Announcement channel and/or registered "
                           "phone numbers based on level (1, 2, 3). Message must be surrounded by "
                           "\"\".", inline=False)
help_embed.add_field(name='Announcements: `!text_list`',
                     value="ADMIN CMD. Displays all registered users and numbers", inline=False)
help_embed.add_field(name='Announcements: `!send_pm <user> <message>`',
                     value="ADMIN CMD. Send a private text to a registered user. Message must be surrounded by "
                           "\"\".")
help_embed.add_field(name='Announcements: `!add_number <number>`',
                     value="Add your phone number to the registered number list. Example: +10009998888", inline=False)
help_embed.add_field(name='Announcements: `!remove_number`',
                     value="Removes your phone number from the registered number list.", inline=False)
help_embed.add_field(name='Channels: `!new_text_channels <name> <num>`',
                     value="ADMIN CMD. Create num number of text channels named name.", inline=False)
help_embed.add_field(name='Channels: `!new_voice_channels <name> <num>`',
                     value="ADMIN CMD. Create num number of voice channels named name.", inline=False)
help_embed.add_field(name='Channels: `!delete_channels <name>`',
                     value="ADMIN CMD. Delete all channels named name.", inline=False)
help_embed.add_field(name='General: `!command_list`',
                     value="Produce this list of all solace-bot commands.", inline=False)
help_embed.add_field(name='General: `!enter_course_info`',
                     value="Triggers the updating of course information embed with message input and prompts.",
                     inline=False)
help_embed.add_field(name='Discussion Threads: `!reply_threads <thread_id>`',
                     value="Adds your reply to the chain of messages in the thread.", inline=False)
help_embed.add_field(name='Discussion Threads: `!view_thread <thread_id>`',
                     value="Displays the thread given by thread_id", inline=False)
help_embed.add_field(name='Discussion Threads: `!new_thread`',
                     value="Triggers the creation of a new discussion thread through message input and prompts.",
                     inline=False)


support_embed = discord.Embed(title='Mental Health Support Resources', colour=discord.Colour.blue())
support_embed.add_field(name="If at immediate risk, call `911`",
                        value="Call immediately if you are worried about hurting yourself or others "
                              "or if you have the means to and have done so before", inline=False)
support_embed.add_field(name="U of T My Student Support Program: call `1-844-451-9700`",
                        value="For confidential 24/7 emergency mental health counselling in 146 languages",
                        inline=False)
support_embed.add_field(name="Good2Talk Ontario Student Helpline: call `1-866-925-5454`",
                        value="24/7 professional counseling, information and referrals helpline for "
                              "mental health, addictions and well-being.",
                        inline=False)
support_embed.add_field(name="U of T Student Life Contacts",
                        value="If you feel distressed, please reach out to one of these resources:"
                              "https://studentlife.utoronto.ca/task/support-when-you-feel-distressed/ for solace.",
                        inline=False)

course_embed_updated = False
course_embed = discord.Embed(title="Course Information", color=discord.Colour.dark_red())
course_embed.add_field(name="No Course Info", value="Instructor has not updated Course Info", inline=False)


def discord_embed(tag: str) -> Optional[discord.Embed]:
    if "HC" in tag:
        return help_com()
    elif "CQ" in tag:
        return course_question()
    elif "DT" in tag:
        return dark_times()
    else:
        return None


def help_com() -> discord.Embed:
    return help_embed


def course_question() -> Optional[discord.Embed]:
    return course_embed


def dark_times() -> Optional[discord.Embed]:
    return support_embed


def extra_line(message: discord.Message, tag: str) -> str:
    if tag == "BC01":
        return bot_convo_1(message)
    if tag == "BC07":
        return bot_convo_7()
    else:
        return ""


def bot_convo_1(message: discord.Message) -> str:
    reply = "How's it going, " + message.author.name + "?"
    return reply

def bot_convo_7() -> str:
    reply = "https://tenor.com/view/love-laughing-cute-gif-14468800"
    return reply


chatbot = GenericAssistant(intents='intents.json', model_name="solace")
chatbot.train_model()
chatbot.save_model()

print("Solace AI running...")


class chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_channel = ""

    @commands.command()
    async def command_list(self, ctx):
        await ctx.send(embed=help_embed)
        await ctx.send("See https://github.com/SpaceJesusTM/solace for more details!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_chat(self, ctx, channel):
        self.chat_channel = channel
        await ctx.send("Chat channel set to " + channel)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel.name == self.chat_channel:
            # if message.content.startswith("$solace"):
            # response = chatbot.request(message.content[6:])
            if not message.content.startswith("!"):
                response = chatbot.request(message.content)
                tag = response[0:4]
                response = response[5:]
                await message.channel.send(response)
                second_line = extra_line(message, tag)
                if second_line != "":
                    await message.channel.send(second_line)
                embed = discord_embed(tag)
                if embed != None:
                    await message.channel.send(embed=embed)
        # else:
        #   await message.channel.send("sorry wrong channel")

    @commands.command(name="enter_course_info")
    @commands.has_permissions(administrator=True)
    async def enter_course_info(self, ctx):
        def check(m):
            return m.author.id == ctx.author.id

        await ctx.send("Please enter the course name (or type 'cancel'):")
        title = await self.bot.wait_for('message', check=check)
        if title.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        await ctx.send("Please enter the course description (or type 'cancel'):")
        description = await self.bot.wait_for('message', check=check)
        if description.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        await ctx.send("Please enter the course website link (or type 'cancel'):")
        website = await self.bot.wait_for('message', check=check)
        if website.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        await ctx.send("Please enter the course email (or type 'cancel'):")
        email = await self.bot.wait_for('message', check=check)
        if email.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        await ctx.send("Please enter the instructor names (or type 'cancel'):")
        instructors = await self.bot.wait_for('message', check=check)
        if instructors.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        await ctx.send("Please enter assignment details (or type 'cancel'):")
        assignments = await self.bot.wait_for('message', check=check)
        if assignments.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        await ctx.send("Please enter test details (or type 'cancel'):")
        tests = await self.bot.wait_for('message', check=check)
        if tests.content == 'cancel':
            await ctx.send("Course Information not Updated.")
            return

        new_embed = discord.Embed(title=title.content, color=discord.Colour.magenta())
        new_embed.add_field(name="course description", value=description.content, inline=False)
        new_embed.add_field(name="website link", value=website.content, inline=False)
        new_embed.add_field(name="course email", value=email.content, inline=False)
        new_embed.add_field(name="instructor names", value=instructors.content, inline=False)
        new_embed.add_field(name="assignment details", value=assignments.content, inline=False)
        new_embed.add_field(name="test details", value=assignments.content, inline=False)
        await ctx.send(embed=new_embed)

        await ctx.send("Is this the correct information for your course? (y/n):")
        possible = ['y', 'n']
        confirm = 0
        while confirm == 0 or confirm.content not in possible:
            confirm = await self.bot.wait_for('message', check=check)
            if confirm.content not in possible:
                await ctx.send("Please enter 'y' or 'n'.")

        if confirm.content == 'y':
            global course_embed
            course_embed = new_embed
            global course_embed_updated
            course_embed_updated = True
            await ctx.send("Course information saved.")
        else:
            await ctx.send("Course information cancelled.")
