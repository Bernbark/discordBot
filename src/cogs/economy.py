import asyncio
import datetime
import random

import discord
from discord import app_commands
from discord.ext import commands, tasks
from fetchData import fetch_data, update_banks
from botUtilities import make_embed


#make cups able to buy a grade up which is defense, make that next tier able to grade up to magic, buy 10 and get 1 of
# the next grade
class economy(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.jobDescriptions = [
            "helping raise awareness for the whales.",
            "singing a sad song in the public square.",
            "singing a happy song in the public square.",
            "winning a bet with a stanger on who had more teeth.",
            "saving the village from Elmo the Destroyer.",
            "grinding out level 2 boars in the beginner forest for 92 days.",
            "defeating a Balrog without saying 'You shall not pass!'",
            "sending bills to random companies you've never interacted with before.",
            "teaching a donkey how to sing happy birthday.",
            "making polite conversation on an hourly basis.",
            "hang gliding a cat to safety.",
            "creating a zip line that goes uphill.",
            "helping the elderly with electronics."
        ]
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=1800)
    async def printer(self):
        await update_banks(self.bot)
        print("Banks updated.")

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="deposit",
        help="Deposit your money for safe keeping.."
    )
    async def deposit(self, ctx: commands.Context, amount: int = 0):
        if amount <= 0:
            await ctx.send("Please choose a positive, non-zero number for the amount of coins to deposit")
            return
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        coins = userData["coins"]
        if amount > coins:
            userData["coins"] = 0
            userData["bank"] += coins
            embed = make_embed("Deposit success", f"You deposited {coins} coins to the bank.")
        else:
            userData["coins"] -= amount
            userData["bank"] += amount
            embed = make_embed("Deposit success", f"You deposited {amount} coins to the bank.")
        await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, userData)

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="withdraw",
        help="Withdraw your money from the bank."
    )
    async def withdraw(self, ctx: commands.Context, amount: int = 0):
        if amount <= 0:
            await ctx.send("Please choose a positive, non-zero number for the amount of coins to deposit")
            return
        member = ctx.author
        user_data, collection = await fetch_data(self.bot, member.id)
        coins_saved = user_data["bank"]
        if amount > coins_saved:
            user_data["bank"] = 0
            user_data["coins"] += coins_saved
            embed = make_embed("Withdraw success", f"You withdrew {coins_saved} coins from the bank.")
        else:
            user_data["bank"] -= amount
            user_data["coins"] += amount
            embed = make_embed("Withdraw success", f"You withdrew {amount} coins from the bank.")
        await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, user_data)

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="oddjob",
        help="Do random things about town for money."
    )
    async def oddJob(self, ctx: commands.Context):

        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        moneyReceived = random.randint(0 , 1000)
        jobDescription = random.choice(self.jobDescriptions)
        userData["coins"] += moneyReceived
        embed = make_embed("Oddjob Complete", f"You earned {moneyReceived} coins by: {jobDescription}")
        await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, userData)

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(
        name="buymysterybox",
        aliases=["bmb","mystery","mysterybox"],
        help="Who knows what's inside?"
    )
    async def buyMysteryBox(self, ctx: commands.Context):
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        totalGold = userData["coins"]
        if userData["coins"] >= 5000:
            userData["coins"] -= 5000
            userData["boxes"] += 1
            currentBoxes = userData["boxes"]
            embed = make_embed("Mystery Box Purchased",f"You've purchased one box. Total boxes = {currentBoxes}")
            await ctx.send(embed=embed)
            await collection.replace_one({"_id": member.id}, userData)
        else:
            self.buyMysteryBox.reset_cooldown(ctx)
            embed = make_embed("Mystery Box Denied", f"You've only got {totalGold} coins :( Need 5000 for boxes.")
            await ctx.send(embed=embed)
            await ctx.send()


    @commands.command(
        name="buycup",
        aliases=["bc","cup"],
        help="Buy another cup to hold your begging money. More cups = more profit right?"
    )
    async def buyCup(self, ctx: commands.Context, amount: int = 1):
        if amount <= 0:
            await ctx.send("Please use a positive, non-zero number for the amount to buy.")
            return
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        totalGold = userData["coins"]
        if userData["coins"] >= (500 * amount):
            userData["coins"] -= 500 * amount
            userData["cups"] += 1 * amount
            cupAmount = userData["cups"]
            if amount == 1:
                embed = make_embed("Bought cup")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()

                await channel.send(f"You currently have {cupAmount} cups")
            else:
                embed = make_embed(f"You've purchased {amount} cups.")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {cupAmount} cups")

        else:
            description = ""
            amountToPurchase = int(totalGold / 500)
            if totalGold >= 500:

                userData["coins"] -= 500 * amountToPurchase
                userData["cups"] += 1 * amountToPurchase
                cupAmount = userData["cups"]
                description=f"You didn't have enough for that, but we purchased {amountToPurchase} instead " \
                            "with the coins you have.\n"
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {cupAmount} cups")
            embed = make_embed(f"Purchased alternate amount", f"{description}"
                                                              f"You only had {totalGold} coins :( Need 500 per cup. ")
            await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, userData)
        channel = await ctx.author.create_dm()

    @commands.command(
        name="buycardboard",
        aliases=["bcb", "cardboard","cb"],
        help="Buy cardboard to protect yourself."
    )
    async def buyCardBoard(self, ctx: commands.Context, amount: int = 1):
        if amount <= 0:
            await ctx.send("Please use a positive, non-zero number for the amount to buy.")
            return
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        cups = userData["cups"]
        if userData["cups"] >= (20 * amount):
            userData["cups"] -= 20 * amount
            userData["cardboard"] += 1 * amount
            cardboardAmount = userData["cardboard"]
            if amount == 1:
                embed = make_embed(f"Bought cardboard.")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {cardboardAmount} cardboard")
            else:
                embed = make_embed(f"Purchase success.", f"You've purchased {amount} cardboard.")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {cardboardAmount} cardboard")

        else:
            description = ""
            amountToPurchase = int(cups / 20)
            if cups >= 20:
                userData["cups"] -= 20 * amountToPurchase
                userData["cardboard"] += 1 * amountToPurchase
                cardboardAmount = userData["cardboard"]
                description = "You didn't have enough for that, but we purchased as many as " \
                              "we could with the coins you have.\n"
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {cardboardAmount} cardboard")
            embed = make_embed(f"Purchased alternate amount.", f"{description}You only had {cups} cups :( "
                                                    f"Need 20 per cardboard piece. "
                                                               f"Purchased {amountToPurchase} instead")
            await ctx.send(embed=embed)

        await collection.replace_one({"_id": member.id}, userData)

    @commands.command(
        name="buyshades",
        aliases=["bs", "shades", "sunglasses"],
        help="Buy sunglasses to blend in with the crowd."
    )
    async def buyGlasses(self, ctx: commands.Context, amount: int = 1):
        if amount <= 0:
            await ctx.send("Please use a positive, non-zero number for the amount to buy.")
            return
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        cardboard = userData["cardboard"]
        if userData["cardboard"] >= (10 * amount):
            userData["cardboard"] -= 10 * amount
            userData["sunglasses"] += 1 * amount
            sunglasses = userData["sunglasses"]
            if amount == 1:
                embed = make_embed("Bought shades")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {sunglasses} sunglasses")
            else:
                embed = make_embed("Bought shades",f"You've purchased {amount} sunglasses.")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {sunglasses} sunglasses")

        else:
            description = ""
            amountToPurchase = int(cardboard / 10)
            if cardboard >= 10:
                userData["cardboard"] -= 10 * amountToPurchase
                userData["sunglasses"] += 1 * amountToPurchase
                sunglasses = userData["sunglasses"]
                description = "You didn't have enough for that, but we purchased as many as " \
                              "we could with the coins you have.\n"
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {sunglasses} sunglasses")
            embed = make_embed("Purchased alternate amount.",f"{description}You only had {cardboard} cardboard :( "
                                                             f"Need 10 per pair of sunglasses. "
                                                             f"Purchased {amountToPurchase} instead")
            await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, userData)

    @commands.command(
        name="buynocs",
        aliases=["bn", "nocs", "binoculars"],
        help="Buy 'nocs to spot the spies. Get it, buy 'nocs? Binoculars?!?"
    )
    async def buyNocs(self, ctx: commands.Context, amount: int = 1):
        if amount <= 0:
            await ctx.send("Please use a positive, non-zero number for the amount to buy.")
            return
        member = ctx.author
        userData, collection = await fetch_data(self.bot, member.id)
        cardboard = userData["cardboard"]
        if userData["cardboard"] >= (10 * amount):
            userData["cardboard"] -= 10 * amount
            userData["binoculars"] += 1 * amount
            nocs = userData["binoculars"]
            if amount == 1:
                embed = make_embed("Bought sweet sweet 'nocs")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {nocs} 'nocs")
            else:
                embed =make_embed("Bought some 'nocs",f"You've purchased {amount} 'nocs. Nice 'nocs bruh.")
                await ctx.send(embed=embed)
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {nocs} 'nocs")

        else:
            description = ""
            amountToPurchase = int(cardboard / 10)
            if cardboard >= 10:
                userData["cardboard"] -= 10 * amountToPurchase
                userData["binoculars"] += 1 * amountToPurchase
                nocs = userData["binoculars"]
                description = "You didn't have enough for that, but we purchased as many as " \
                              "we could with the coins you have.\n"
                channel = await ctx.author.create_dm()
                await channel.send(f"You currently have {nocs} 'nocs")
            embed=make_embed("Purchased alternate amount",f"{description}You only had {cardboard} cardboard :( "
                                                          f"Need 10 per pair of sweet, sweet 'nocs. "
                                                          f"Purchased {amountToPurchase} instead")
            await ctx.send(embed=embed)

        await collection.replace_one({"_id": member.id}, userData)

    @app_commands.command(
        name= "beg",
        description= "Beg for money >:*( Also resets your coins to 0 in case of bankruptcy."
    )
    async def beg(self, interaction: discord.Interaction) -> None:

        userData, collection = await fetch_data(self.bot, interaction.user.id)
        cupAmount = userData["cups"]
        cupBonus = cupAmount * 10
        moneyReceived = random.randint(0+cupBonus, 100+cupBonus)
        descriptionString = ""
        if userData["coins"] < 0:
            userData["coins"] = 0
            descriptionString = "You were saved from loan sharks and now have a clean slate with 0 coins.\n"
        userData["coins"] += moneyReceived
        embed = make_embed("Begged for money",f"{descriptionString}You've received {moneyReceived} coins! "
                                                f"Earned a bonus of {cupBonus}"
                                                f" from cups!")
        await interaction.response.send_message(embed=embed)

        await collection.replace_one({"_id" : interaction.user.id}, userData)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        economy(bot)
    )