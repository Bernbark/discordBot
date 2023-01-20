# A good template for cogs
import os
import random


import discord

from discord.ext import commands, tasks


from dotenv import load_dotenv


load_dotenv()
ART_TOKEN = os.getenv('ART_API')

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

class artsy(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot



async def setup(bot: commands.Bot):

    await bot.add_cog(
        artsy(bot)
    )
