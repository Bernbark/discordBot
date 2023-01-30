import discord
from discord.ext import commands
from discord.ui import Button, View

from src.fetchData import fetch_inventory, add_to_auction_house
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
        we want to move the inventory page back one, and adjust button availability based on the current index
        """
        self.view.interaction = interaction
        self.view.interaction_set = True
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
        we want to move the inventory page forward one, and adjust button availability based on the current index
        """

        self.view.interaction = interaction
        self.view.interaction_set = True
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
    One of the coolest parts about using the View as a class is that we can add behavior to it. Such as tracking
    stats like the embeds list which are our pages, and the current page we are in which is basically the list index
    we want to be at. This helps us control behaviors much more easily.
    """
    def __init__(self, ctx, embeds: [discord.Embed]):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.msg = None
        self.embeds = embeds
        self.MAX_PAGES = len(embeds)
        self.forward_button = ForwardButton(self.embeds)
        self.add_item(self.forward_button)
        self.cur_page = 0
        self.interaction_set = False
        self.interaction = None

    async def on_timeout(self):
        """
        This is what happens when the game is no longer interactable, we want to clear the UI probably
        :return:
        """
        self.clear_items()

        await self.msg.delete()
        await self.ctx.message.delete()
        self.stop()


class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="auctionitem",
        aliases=["aitem"],
        help="Auction from your inventory by ID"
    )
    async def auction_item(self, ctx: commands.Context, _id: str = None, price: int = 500):
        if _id is None:
            await ctx.send("Please use an ID associated with an item you own.")
            return
        inventory, collection = await fetch_inventory(self.bot, ctx.author.id)
        inv = inventory["inventory_weapon"]
        torso_inv = inventory["inventory_torso"]
        for item in inv:
            if item["item_id"] == _id:
                inv.remove(item)
                added = await add_to_auction_house(self.bot,item,price,ctx.author.id)
                if added:
                    await ctx.send(f"Item placed on auction!")
                    inventory["inventory_weapon"] = inv
                    await collection.replace_one({"_id": ctx.author.id}, inventory)
                else:
                    await ctx.send(f"Item was not sent to auction!")
                return
        for item in torso_inv:
            if item["item_id"] == _id:
                torso_inv.remove(item)
                added = await add_to_auction_house(self.bot,item,price,ctx.author.id)
                if added:
                    await ctx.send(f"Item placed on auction!")
                    inventory["inventory_torso"] = torso_inv
                    await collection.replace_one({"_id": ctx.author.id}, inventory)
                else:
                    await ctx.send(f"Item was not sent to auction!")
                return

        await ctx.send(f"Found nothing by that ID.")

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="sell",
        aliases=["sellitem"],
        help="Sell from your inventory by ID"
    )
    async def sell_item(self, ctx: commands.Context, _id: str = None):
        if _id is None:
            await ctx.send("Please use an ID associated with an item you own.")
            return
        inventory, collection = await fetch_inventory(self.bot, ctx.author.id)
        inv = inventory["inventory_weapon"]
        torso_inv = inventory["inventory_torso"]
        for item in inv:
            if item["item_id"] == _id:
                inv.remove(item)
                await ctx.send(f"Sold {item}")
                await collection.replace_one({"_id": ctx.author.id}, inventory)
                return
        for item in torso_inv:
            if item["item_id"] == _id:
                torso_inv.remove(item)
                await ctx.send(f"Sold {item}")
                await collection.replace_one({"_id": ctx.author.id}, inventory)
                return
        await ctx.send(f"Found nothing by that ID.")

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="inventory",
        aliases=["inv"],
        help="Look at your inventory."
    )
    async def inventory(self, ctx: commands.Context, type: str = None):
        user_inventory, collection = await fetch_inventory(self.bot,ctx.author.id)
        weapon_inv, torso_inv = None, None
        if type == "weapon":
            weapon_inv = user_inventory["inventory_weapon"]
            inventory_size = len(weapon_inv)
        elif type == "torso":
            torso_inv = user_inventory["inventory_torso"]
            inventory_size = len(torso_inv)
        else:
            weapon_inv = user_inventory["inventory_weapon"]
            torso_inv = user_inventory["inventory_torso"]
            inventory_size = len(weapon_inv) + len(torso_inv)

        # make multiple pages
        if inventory_size > 10:
            embeds = []
            embed = make_embed(f"{ctx.author.name}'s Inventory")
            count = 0
            if type == "weapon" or type is None:
                for item in weapon_inv:
                    name = item["name"]
                    dmg = item['dmg']
                    description = item['description']
                    rarity = item['rarity']
                    item_id = item['item_id']
                    embed.add_field(name=f"'{name}'", value=f"DMG: {dmg}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Sale: {item_id}")
                    count += 1
                    # every 10 we reset the count, and make a new embed while adding the previous one to the list
                    if count == 10:
                        embeds.append(embed)
                        embed = make_embed(f"{ctx.author.name}'s Inventory")
                        count = 0
            if type == "torso" or type is None:
                for item in torso_inv:
                    name = item["name"]
                    defense = item['def']
                    description = item['description']
                    rarity = item['rarity']
                    item_id = item['item_id']
                    embed.add_field(name=f"'{name}'", value=f"DMG: {defense}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Sale: {item_id}")
                    count += 1
                    # every 10 we reset the count, and make a new embed while adding the previous one to the list
                    if count == 10:
                        embeds.append(embed)
                        embed = make_embed(f"{ctx.author.name}'s Inventory")
                        count = 0
            # make sure to append the final page!
            embeds.append(embed)
            # create the custom view, sending in any info we want
            view = InventoryView(ctx,embeds)
            # start at the first page, embeds[0], the view handles the behavior from then on
            msg = await ctx.send(embed=embeds[0],view=view)
            view.msg = msg
        else:
            embed = make_embed(f"{ctx.author.name}'s Inventory")
            if type == "weapon" or type is None:
                for item in weapon_inv:
                    name = item["name"]
                    dmg = item['dmg']
                    description = item['description']
                    rarity = item['rarity']
                    item_id = item['item_id']
                    embed.add_field(name=f"'{name}'", value=f"DMG: {dmg}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Sale: {item_id}")
            if type == "torso" or type is None:
                for item in torso_inv:
                    name = item["name"]
                    defense = item['def']
                    description = item['description']
                    rarity = item['rarity']
                    item_id = item['item_id']
                    embed.add_field(name=f"'{name}'", value=f"DMG: {defense}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Sale: {item_id}")
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        Inventory(bot)
    )
