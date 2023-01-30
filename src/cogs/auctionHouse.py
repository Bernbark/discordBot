import asyncio

import discord
from discord.ext import commands
from src.botUtilities import make_embed
from src.cogs.inventory import InventoryView
from src.fetchData import fetch_auction_items, fetch_data, fetch_inventory


class AuctionHouse(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="ahbuy",
        aliases=["auctionhousebuy","buyauctionitem"],
        help="Buy auction house item by ID."
    )
    async def auction_house_buy(self, ctx: commands.Context, item_id: str = None):
        if item_id is None:
            await ctx.send("Please use an ID associated with an item you want to buy.")
            return
        auction_collection = await fetch_auction_items(self.bot)
        user_data, collection = await fetch_data(self.bot, ctx.author.id)
        user_inv, inv_collection = await fetch_inventory(self.bot, ctx.author.id)
        if await auction_collection.find_one({"_id": item_id}) is None:
            await ctx.send("No such ID found.")
            return
        item_to_buy = await auction_collection.find_one({"_id":item_id})
        item = item_to_buy["item"]
        await auction_collection.delete_one({"_id":item_id})
        if user_data["coins"] >= item_to_buy["price"]:
            user_data["coins"] -= item_to_buy["price"]
            if item["type"] == "weapon":
                user_inv["inventory_weapon"].append(item)
            elif item["type"] == "torso":
                user_inv["inventory_torso"].append(item)
            await inv_collection.replace_one({"_id": ctx.author.id}, user_inv)
            await collection.replace_one({"_id": ctx.author.id}, user_data)
            await ctx.send(f"You purchased: {item}")
        else:
            await ctx.send("You don't have the gold for this")


    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="ah",
        aliases=["auctionhouse"],
        help="View auction house items."
    )
    async def auction_house(self, ctx: commands.Context):
        collection = await fetch_auction_items(self.bot)
        await asyncio.sleep(3)
        auction_items = collection.find()

        auction_size = await collection.count_documents({})

        # make multiple pages
        if auction_size > 10:
            embeds = []
            embed = make_embed(f"Auction House")
            count = 0
            async for item in auction_items:
                if item["item"]["type"] == "weapon":
                    name = item["item"]["name"]
                    dmg = item["item"]['dmg']
                    description = item["item"]['description']
                    rarity = item["item"]['rarity']
                    item_id = item["item"]['item_id']
                    cost = item["price"]
                    embed.add_field(name=f"'{name}'", value=f"DMG: {dmg}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Purchase: {item_id}\n"
                                                            f"Cost: {cost}")
                elif item["item"]["type"] == "torso":
                    name = item["item"]["name"]
                    defense = item["item"]['def']
                    description = item["item"]['description']
                    rarity = item["item"]['rarity']
                    item_id = item["item"]['item_id']
                    cost = item["price"]
                    embed.add_field(name=f"'{name}'", value=f"Def: {defense}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Purchase: {item_id}\n"
                                                            f"Cost: {cost}")
                count += 1
                # every 10 we reset the count, and make a new embed while adding the previous one to the list
                if count == 10:
                    embeds.append(embed)
                    embed = make_embed(f"Auction House")
                    count = 0
            # make sure to append the final page!
            embeds.append(embed)
            # create the custom view, sending in any info we want
            view = InventoryView(ctx, embeds)
            # start at the first page, embeds[0], the view handles the behavior from then on
            msg = await ctx.send(embed=embeds[0], view=view)
            view.msg = msg
        else:
            embed = make_embed(f"Auction House")
            async for item in auction_items:
                if item["item"]["type"] == "weapon":
                    name = item["item"]["name"]
                    dmg = item["item"]['dmg']
                    description = item["item"]['description']
                    rarity = item["item"]['rarity']
                    item_id = item["item"]['item_id']
                    cost = item["price"]
                    embed.add_field(name=f"'{name}'", value=f"DMG: {dmg}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Purchase: {item_id}\n"
                                                            f"Cost: {cost}")
                elif item["item"]["type"] == "torso":
                    name = item["item"]["name"]
                    defense = item["item"]['def']
                    description = item["item"]['description']
                    rarity = item["item"]['rarity']
                    item_id = item["item"]['item_id']
                    cost = item["price"]
                    embed.add_field(name=f"'{name}'", value=f"Def: {defense}\nDescription: {description}\n"
                                                            f"Rarity: {rarity}\nID for Purchase: {item_id}\n"
                                                            f"Cost: {cost}")
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        AuctionHouse(bot)
    )