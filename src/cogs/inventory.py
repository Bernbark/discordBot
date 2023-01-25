from discord.ext import commands
from src.fetchData import fetch_inventory
from src.botUtilities import make_embed


class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="inventory",
        help="Look at your inventory."
    )
    async def inventory(self, ctx: commands.Context):
        user_inventory, collection = await fetch_inventory(self.bot,ctx.author.id)
        inv = user_inventory["inventory"]
        embed = make_embed(f"{ctx.author.name}'s Inventory")
        for item in inv:
            name = item["name"]
            dmg = item['dmg']
            description = item['description']
            rarity = item['rarity']
            embed.add_field(name=f"'{name}'", value=f"DMG: {dmg}\nDescription: {description}\n"
                                                    f"Rarity: {rarity}")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        Inventory(bot)
    )
