from discord.ext import commands
from src.fetchData import fetch_data
from src.botUtilities import make_embed


class WhatToWatch(commands.Cog):
    """
    Simple class that allows me to save the shows I want to watch later
    """
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(
        name="watchlater",
        help="Save something to watch later."
    )
    async def watch_later(self, ctx: commands.Context, url: str = ""):
        """
        The user can enter some text, hopefully a show or movie name/url, for them to watch later
        :param ctx:
        :param url:
        :return:
        """
        if url == "":
            await ctx.send(embed=make_embed("Type or paste a URL/show name after the command to save it."))
            return
        member = ctx.author
        user_data, collection = await fetch_data(self.bot, member.id)
        user_data["watchLater"].append(url)
        await ctx.send(embed=make_embed("Collection updated, new show acquired for viewing later."))
        await collection.replace_one({"_id": member.id}, user_data)

    @commands.command(
        name="printwatchlist",
        help="Print your watch list out."
    )
    async def print_watch_later(self, ctx: commands.Context):
        """
        Just grabs the user's list from the database and prints it for them
        :param ctx:
        :return:
        """
        member = ctx.author
        user_data, collection = await fetch_data(self.bot, member.id)
        watch_list = user_data["watchLater"]
        await ctx.send(embed=make_embed(f"Collection: {watch_list}"))
        await collection.replace_one({"_id": member.id}, user_data)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        WhatToWatch(bot)
    )
