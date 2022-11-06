import discord
import asyncio
from discord.ext import commands

class discussion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.thread_id = 0
        self.threads = {}
        self.threads_channel = ""
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_threads(self, ctx, channel):
        self.threads_channel = channel
        await ctx.send("Threads channel set to " + channel)

    @commands.command()
    async def reply_thread(self, ctx, th_id):
        if self.threads_channel == "":
            await ctx.send("Please set the threads channel first!")
            return
        dict_key = int(th_id)
        dict_value = self.threads[dict_key]

        def check(m):
            return m.author.id == ctx.author.id

        await ctx.send("Please enter the title of your reply (or type 'cancel'):")
        title = await self.bot.wait_for('message', check=check)
        if title.content == 'cancel':
            await ctx.send('Reply Thread Cancelled.')
            return
    
        await ctx.send("Please enter the content of your reply (or type 'cancel'):")
        content = await self.bot.wait_for('message', check=check)
        if content.content == 'cancel':
            await ctx.send('Reply Thread Cancelled.')
            return
        
        embed = discord.Embed(title=title.content, color=discord.Colour.gold())
        embed.add_field(name=f"Reply to Thread {th_id}:", value=content.content, inline=False)
        embed.add_field(name="Reply by:", value=ctx.author, inline=False)
        await ctx.send(embed=embed)

        await ctx.send("Are you sure you want to create this thread? (y/n):")
        possible = ['y', 'n']
        confirm = 0
        while confirm == 0 or confirm.content not in possible:
            confirm = await self.bot.wait_for('message', check=check)
            if confirm.content not in possible:
                await ctx.send("Please enter 'y' or 'n'.")
        
        if confirm.content == 'y':
            channel = discord.utils.get(ctx.guild.channels, name=self.threads_channel)
            # channel_id = channel.id
            dict_value[2].append(embed)

            embeds = dict_value[2]
            cur_page = 1
            pages = len(embeds)
            embed = await channel.fetch_message(dict_value[0])
            message = await channel.fetch_message(dict_value[1])
            await message.edit(content=f"Page {cur_page}/{pages}")
            # print(self.threads)
            await ctx.send(f"Reply to Thread {th_id} created.")
            # getting the message object for editing and reacting
    
    @commands.command()
    async def view_thread(self, ctx, th_id):
        if self.threads_channel == "":
            await ctx.send("Please set the threads channel first!")
            return
        # curr_id = th_id
        # if not curr_id.is_digit():
        #     return await ctx.send("Please input an integer.")
        dict_key = int(th_id)
        dict_value = self.threads[dict_key]
        embeds = dict_value[2]
        pages = len(embeds)
        cur_page = 1

        embed = await ctx.send(embed=embeds[0])
        message = await ctx.send(f"Page {cur_page}/{pages}")

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await embed.edit(embed=embeds[cur_page-1])
                    await message.edit(content=f"Page {cur_page}/{pages}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await embed.edit(embed=embeds[cur_page-1])
                    await message.edit(content=f"Page {cur_page}/{pages}")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await embed.delete()
                await message.delete()
                await ctx.send('View Timeout...')
                break
        
    
    @commands.command()
    async def new_thread(self, ctx):
        if self.threads_channel == "":
            await ctx.send("Please set the threads channel first!")
            return
        def check(m):
            return m.author.id == ctx.author.id

        await ctx.send("Please enter the title of your thread (or type 'cancel'):")
        title = await self.bot.wait_for('message', check=check)
        if title.content == 'cancel':
            await ctx.send('New Thread Cancelled.')
            return
    
        await ctx.send("Please enter the content of your thread (or type 'cancel'):")
        content = await self.bot.wait_for('message', check=check)
        if content.content == 'cancel':
            await ctx.send('New Thread Cancelled.')
            return
        
        self.thread_id += 1
        embed = discord.Embed(title=title.content, color=discord.Colour.gold())
        embed.add_field(name=f"Thread ID: {self.thread_id}", value=content.content, inline=False)
        embed.add_field(name="Thread by:", value=ctx.author, inline=False)
        await ctx.send(embed=embed)

        await ctx.send("Are you sure you want to create this thread? (y/n):")
        possible = ['y', 'n']
        confirm = 0
        while confirm == 0 or confirm.content not in possible:
            confirm = await self.bot.wait_for('message', check=check)
            if confirm.content not in possible:
                await ctx.send("Please enter 'y' or 'n'.")
        
        if confirm.content == 'y':
            channel = discord.utils.get(ctx.guild.channels, name=self.threads_channel)
            # channel_id = channel.id
            thread_list = [embed]

            embeds = thread_list
            pages = len(thread_list)
            cur_page = 1
            embed = await channel.send(embed=embeds[cur_page-1])
            message = await channel.send(f"Page {cur_page}/{pages}")

            dict_key = self.thread_id
            dict_value = [embed.id, message.id, thread_list]
            self.threads[dict_key] = dict_value 
            # print(self.threads)
            await ctx.send("Thread created.")
            # getting the message object for editing and reacting
        else:
            await ctx.send('New Thread Cancelled')
    