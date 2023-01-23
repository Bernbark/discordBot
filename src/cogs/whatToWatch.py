# A good template for cogs
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import bot
from fetchData import fetch_data


async def makeEmbed(title, description, url):

    colorOne = random.randint(0, 255)
    colorTwo = random.randint(0, 255)
    colorThree = random.randint(0, 255)
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.from_rgb(colorOne, colorTwo, colorThree)
    )
    embed.set_image(url=url)
    embed.add_field(name="GAME NAME UNIMPLEMENTED", value="-----------------------")
    embed.set_footer(text="Bot written by Kory Stennett")


    #embed.set_thumbnail(url=url)
    return embed

class whatToWatch(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(
        name="watchlater",
        help="Save something to watch later."
    )
    async def watchLater(self, ctx: commands.Context, url: str = ""):
        if url == "":
            await ctx.send("Type or paste a URL/show name after the command to save it.")
            return
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        userData["watchLater"].append(url)
        await ctx.send("Collection updated, new show acquired for viewing later.")
        await collection.replace_one({"_id": member.id}, userData)

    @commands.command(
        name="printwatchlist",
        help="Print your watch list out."
    )
    async def printWatchLater(self, ctx: commands.Context):

        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        watchList = userData["watchLater"]
        await ctx.send(f"Collection: {watchList}")
        await collection.replace_one({"_id": member.id}, userData)

async def setup(bot: commands.Bot):

    await bot.add_cog(
        whatToWatch(bot)
    )
