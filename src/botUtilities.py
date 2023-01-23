import random
import discord


def make_embed(title: str = "", description: str = "", url: str = "") -> discord.Embed:
    """
    Utility function to create an embed for messages sent to public channels.
    :param title: the header text
    :param description: the body test
    :param url: optional image url
    :return: Discord embed
    """

    color_one = random.randint(0, 255)
    color_two = random.randint(0, 255)
    color_three = random.randint(0, 255)
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.from_rgb(color_one, color_two, color_three)
    )
    embed.set_image(url=url)
    embed.add_field(name="**CRUDBot**", value="-----------------------")
    embed.set_footer(text="'Bot written by Kory Stennett'")
    return embed
