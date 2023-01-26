import random

import discord
from discord.ext import commands
from discord.ui import Button, View

from src.fetchData import fetch_inventory
from src.botUtilities import make_embed


class BackButton(Button):
    """
    The subclass responsible for templating back buttons and their behavior
    """
    def __init__(self, embeds: [discord.Embed],label: str = ""):
        super().__init__(label=label, emoji="◀")
        self.colors = { "red": discord.ButtonStyle.red,
                        "blurple": discord.ButtonStyle.blurple,
                        "green": discord.ButtonStyle.green,
                        "grey": discord.ButtonStyle.grey}
        self.embeds = embeds
        self.style = self.colors["blurple"]

    async def callback(self, interaction: discord.Interaction):
        """
        A necessary method for buttons in Discord.py UI, this is what the button should do when clicked, in this case
        we want to create more dynamite when dynamite is clicked, or decide if the game is over due to clicking it.
        """
        if self.view.cur_page == 0:
            await self.view.ctx.send("You can't go negative pages. C'mon now!")
        else:
            self.view.cur_page -= 1
            if self.view.cur_page == 0:
                self.view.clear_items()
                button = ForwardButton(self.embeds)
                self.view.add_item(button)
            elif self.view.cur_page != len(self.embeds)-1:
                self.view.clear_items()
                button = BackButton(self.embeds)
                self.view.add_item(button)
                button = ForwardButton(self.embeds)
                self.view.add_item(button)
        await interaction.response.edit_message(embed=self.embeds[self.view.cur_page], view=self.view)


class ForwardButton(Button):
    """
    The subclass responsible for templating forward buttons and their behavior
    """
    def __init__(self, embeds: [discord.Embed],label: str = ""):
        super().__init__(label=label, emoji="▶")
        self.colors = { "red": discord.ButtonStyle.red,
                        "blurple": discord.ButtonStyle.blurple,
                        "green": discord.ButtonStyle.green,
                        "grey": discord.ButtonStyle.grey}
        self.embeds = embeds
        self.style = self.colors["blurple"]

    async def callback(self, interaction: discord.Interaction):
        """
        A necessary method for buttons in Discord.py UI, this is what the button should do when clicked, in this case
        we want to create more dynamite when dynamite is clicked, or decide if the game is over due to clicking it.
        """
        if self.view.cur_page == len(self.embeds):
            await self.view.ctx.send("You can't go beyond the pages you have. C'mon now!")
        else:
            self.view.cur_page += 1
            if self.view.cur_page == len(self.embeds)-1:
                self.view.clear_items()
                button = BackButton(self.embeds)
                self.view.add_item(button)
            elif self.view.cur_page != 0:
                self.view.clear_items()
                button = BackButton(self.embeds)
                self.view.add_item(button)
                button = ForwardButton(self.embeds)
                self.view.add_item(button)

        await interaction.response.edit_message(embed=self.embeds[self.view.cur_page], view=self.view)


class InventoryView(View):
    """
    One of the coolest parts about using the View as a class is that we can add behavior to it. Such as tracking game
    stats like the count variable that will tell us how many times the user clicked a "correct" button in the main
    function calling the game, dynamite().
    """
    def __init__(self, ctx, embeds: [discord.Embed]):
        super().__init__(timeout=100)
        self.ctx = ctx
        self.embeds = embeds
        self.MAX_PAGES = len(embeds)
        self.forward_button = ForwardButton(self.embeds)
        self.add_item(self.forward_button)
        self.cur_page = 0


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

        inventorySize = len(inv)
        if inventorySize > 10:
            embeds = []
            embed = make_embed(f"{ctx.author.name}'s Inventory")
            count = 0
            for item in inv:
                name = item["name"]
                dmg = item['dmg']
                description = item['description']
                rarity = item['rarity']
                embed.add_field(name=f"'{name}'", value=f"DMG: {dmg}\nDescription: {description}\n"
                                                        f"Rarity: {rarity}")
                count += 1
                if count == 10:
                    embeds.append(embed)
                    embed = make_embed(f"{ctx.author.name}'s Inventory")
                    count = 0
            embeds.append(embed)
            view = InventoryView(ctx,embeds)
            print(f"Length of inv: {len(inv)}")
            print(f"Amount of embed: {len(embeds)}")
            await ctx.send(embed=embeds[0],view=view)
        else:
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
