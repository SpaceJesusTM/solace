from typing import Optional
import discord
from discord.ext import commands
from neuralintents import GenericAssistant

# global embed variables
help_embed = discord.Embed(title='General Commands', color=discord.Colour.gold())
help_embed.add_field(name='Announcements: `!announce`',
                     value="Send a text to registered phone numbers. Message must be surrounded by \"\".", inline=False)
help_embed.add_field(name='Announcements: `!add_number`',
                     value="Add your phone number to the registered number list. Example: +10009998888", inline=False)
help_embed.add_field(name='Announcements: `!remove_number`',
                     value="Removes your phone number from the registered number list.", inline=False)
help_embed.add_field(name='Temporary Chats: `!new_text_channel`',
                     value="Parameters: name (no spaces) int (number of channels)", inline=False)
help_embed.add_field(name='Temporary Chats: `!new_voice_channel`',
                     value="Parameters: name (no spaces) int (number of channels)", inline=False)
help_embed.add_field(name='Temporary Chats: `!delete_channel`', value="Parameters: name (name of channels to delete)",
                     inline=False)

support_embed = discord.Embed(title='Mental Health Support Resources', colour=discord.Colour.blue())

course_embed_updated = False
course_embed = discord.Embed(title="Course Information", color=discord.Colour.dark_red())
course_embed.add_field(name="No Course Info", value="Instructor has not updated Course Info", inline=False)


def discord_embed(message: discord.Message, tag: str) -> Optional[discord.Embed]:
    if tag == "HC01":
        return help_com_1(message)
    elif tag == "CQ01":
        return course_question_1(message)
    else:
        return None


def extra_line(message: discord.Message, tag: str) -> str:
    if tag == "BI01":
        return bot_intro_1(message)
    else:
        return ""


def bot_intro_1(message: discord.Message) -> str:
    reply = "How's it going, " + message.author.name + "?"
    return reply


def help_com_1(message: discord.Message) -> discord.Embed:
    return help_embed


def course_question_1(message: discord.Message) -> Optional[discord.Embed]:
    return course_embed


discord_functions = {'BotIntro-1': bot_intro_1}

chatbot = GenericAssistant(intents='intents.json', model_name="solace")
chatbot.train_model()
chatbot.save_model()

print("Solace AI running...")


class chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel.name == "solace":
            # if message.content.startswith("$solace"):
            # response = chatbot.request(message.content[6:])
            if not message.content.startswith("!"):
                response = chatbot.request(message.content)
                tag = response[0:4]
                response = response[5:]
                await message.channel.send(response)
                second_line = extra_line(message, tag)
                print("second_line: " + second_line)
                print("tag: " + tag)
                if second_line != "":
                    print(second_line)
                    await message.channel.send(second_line)
                embed = discord_embed(message, tag)
                if embed != None:
                    await message.channel.send(embed=embed)
        # else:
        #   await message.channel.send("sorry wrong channel")

    @commands.command(name="enter_course_info")
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
