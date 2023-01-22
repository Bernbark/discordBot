# A good template for cogs
import random

import aiohttp
import discord

from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import bot
from fetchData import fetchData, removeAccount


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

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="picture", help="Change your profile picture. Must be a link to an image, use http in front.\n"
                                           "You need to right click the image/gif and copy the image address/location, then"
                                           "paste that after !picture")
    async def changePicture(self, ctx: commands.Context, url : str = ""):

        userData, collection = await fetchData(self.bot, ctx.author.id)
        userData["picUrl"] = url

        await ctx.send("Your picture has been changed.")
        await collection.replace_one({"_id": ctx.author.id}, userData)

    @commands.command(name="resetplease", help="Reset your own profile to default. THERE IS NO WARNING, IT WILL JUST"
                                               " HAPPEN FOR NOW, BEWARE")
    async def resetAccount(self, ctx: commands.Context):
        await removeAccount(self.bot,ctx.author.id)
        userData, collection = await fetchData(self.bot, ctx.author.id)
        myPic = userData["picUrl"]
        coins = userData["coins"]

        ownProfileEmbed = await makeEmbed(
            str(ctx.message.author.name) + "'s profile'",
            f"**Username:** {ctx.message.author}\n**User ID:** {ctx.message.author.id}"
                f"\nCurrent coins: {coins}",myPic)

        await ctx.send("Your profile has been reset to default. That means no more coins, cups, or cardboard...for now")
        await ctx.send(embed=ownProfileEmbed)



    @commands.command(name="profile", help="View someone's profile")
    async def profile(self,ctx: commands.Context, user: discord.User = None):

        userData, collection = await fetchData(self.bot,ctx.author.id)
        if user is not None:
            other, collection = await fetchData(self.bot, user.id)
            otherUser = self.bot.get_user(other["_id"])
            otherCoins = other["coins"]
            otherImage = other["picUrl"]
            otherProfileEmbed = await makeEmbed(
                str(otherUser.name) + "'s profile",
                f"**Username:** {otherUser.name}\n**User ID:** {otherUser.id}"
                            f"\nCurrent coins: {otherCoins}", otherImage
                )

        coins = userData["coins"]


        channel = await ctx.author.create_dm()
        totalCups = userData["cups"]
        totalCardboard = userData["cardboard"]
        totalSunglasses = userData["sunglasses"]
        totalBinoculars = userData["binoculars"]
        myPic = userData["picUrl"]
        ownProfileEmbed = await makeEmbed(
                str(ctx.author.name) + "'s profile",
                f"**Username:** {ctx.author.name}\n**User ID:** {ctx.author.id}"
                            f"\nCurrent coins: {coins}", myPic
                )



        if (user is None):
            await ctx.send(embed=ownProfileEmbed)
            await channel.send(f"**Username:** {ctx.message.author}\n**User ID:** {ctx.message.author.id}"
                        f"\nCurrent coins: {coins}\n"
                               f"Current Cups: {totalCups}\n"
                               f"Current Cardboard: {totalCardboard}\n"
                               f"Current Sunglasses: {totalSunglasses}\n"
                               f"Current 'nocs: {totalBinoculars}")
        else:
            await ctx.send(embed=otherProfileEmbed)


    @app_commands.command(
        name= "introduce",
        description= "Introduce yourself!"
    )
    async def introduce(self,
                        interaction: discord.Interaction,
                        name: str,
                        age: int) -> None:
        await interaction.response.send_message(
            f"My name is {name} and my age is {age}"
        )

async def setup(bot: commands.Bot):

    await bot.add_cog(
        test(bot)
    )