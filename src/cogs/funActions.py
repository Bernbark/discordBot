# A good template for cogs
import asyncio
import random
import requests
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from fetchData import fetchData, findByAttackID, updateAttackID, fetchMeme, addMeme, removeMeme
import pymongo
import magic
import os

class funActions(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.acceptedGenres = [
            "confused",
            "happy",
            "sad",
            "test",
        ]

    @commands.cooldown(5, 120, commands.BucketType.user)
    @commands.command(
        name="stealitem",
        help="Steal items from random people. An advanced technique."
    )
    async def stealItem(self, ctx: commands.Context):
        member = ctx.author

        userData, collection = await fetchData(self.bot, member.id)
        async for doc in collection.aggregate([{"$sample": {"size": 1}}]):
            randomUser = doc
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            await ctx.send(f"Your theft failed. Good!")
            return
        theftPower = random.randint(0, userData["sunglasses"])
        theftDefense = randomUser["binoculars"]
        if theftDefense > theftPower:
            moneyLost = random.randint(0, 1000)
            userData["coins"] -= moneyLost
            randomUser["coins"] += moneyLost
            await ctx.send(f"Your theft attempt failed miserably. Lost {moneyLost} coins in your scramble to get away"
                           f" from {user.name}.")
        elif theftPower > theftDefense:
            cupsGained = random.randint(0, (theftPower-theftDefense))
            userData["cups"] += cupsGained
            randomUser["cups"] -= cupsGained
            if randomUser["cups"]<0:
                randomUser["cups"] = 0
            await ctx.send(f"Your theft was very successful. Stole {cupsGained} cups from {user.name}.")
            channel = await ctx.author.create_dm()
            totalCups = userData["cups"]
            await channel.send(f"You currently have {totalCups} cups")
        # both stats are equal, so go to random chance
        else:
            chance = random.randint(0,100)
            if chance > 50:
                moneyLost = random.randint(0, 1000)
                userData["coins"] -= moneyLost
                randomUser["coins"] += moneyLost
                await ctx.send(
                    f"Your theft attempt failed miserably. Lost {moneyLost} coins in your scramble to get away from"
                    f" your equal in espionage, {user.name}.")
            else:
                cupsGained = 1
                userData["cups"] += cupsGained
                randomUser["cups"] -= cupsGained
                if randomUser["cups"] < 0:
                    randomUser["cups"] = 0
                await ctx.send(f"Your theft was minimally successful because your spy power was the same as their spy"
                               f" resistance. Stole 1 cup from your equal in espionage, {user.name}.")
                channel = await ctx.author.create_dm()
                totalCups = userData["cups"]
                await channel.send(f"You currently have {totalCups} cups")

        await collection.replace_one({"_id": member.id}, userData)
        await collection.replace_one({"_id": user.id}, randomUser)

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="scout",
        help="Scout potential targets for future purposes."
    )
    async def scout(self, ctx: commands.Context):
        member = ctx.author

        userData, collection = await fetchData(self.bot, member.id)
        async for doc in collection.aggregate([{"$sample": {"size": 1}}]):
            randomUser = doc
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            await ctx.send(f"Your scout failed. Good!")
            return

        myCupAmount = userData["cups"]

        cupsAmount = randomUser["cups"]
        coinsHeld = randomUser["coins"]
        cardboard = randomUser["cardboard"]
        attackID = randomUser["attackID"]
        sunglasses = randomUser["sunglasses"]
        binoculars = randomUser["binoculars"]
        if myCupAmount > cupsAmount:
            oddsOfWinningNumerator = (myCupAmount/2)/cupsAmount/2
        else:
            oddsOfWinningNumerator = (cupsAmount/2)/myCupAmount/2
        oddsOfWinning = oddsOfWinningNumerator/(myCupAmount+1)
        channel = await member.create_dm()
        await channel.send(f"You found {user.name}'s information on the dark web. They currently hold {cupsAmount} cups.\n"
                            f"They also have {coinsHeld} coins to their name.\n"
                            f"Defense: {cardboard}\n"
                           f"Sunglasses: {sunglasses}\n"
                           f"'Nocs: {binoculars}\n"
                            f"Your chances of beating them in a fight: {oddsOfWinning}.\n"
                            f"Their attackID (used to attack them specifically) is {attackID}.")

    @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.command(
        name="scoutspecific",
        aliases=["scoutbyname","sbn","specificscout"],
        help="Scout specific target by Discord user name."
    )
    async def scoutByName(self, ctx: commands.Context, user: discord.Member = None):
        member = ctx.author

        userData, collection = await fetchData(self.bot, member.id)
        if user is None:
            await ctx.send(f"Either this person's user name has changed, or you copied it wrong!")
            self.scoutByName.reset_cooldown(ctx)
            return
        else:
            randomUser, collection = await fetchData(self.bot, user.id)

        if randomUser is None:
            await ctx.send(f"Either this person's attack ID has changed, or you copied it wrong!")
            self.scoutByName.reset_cooldown(ctx)
            return

        if user == member or user is None:
            await ctx.send(f"Your scout failed for unusual reasons...")
            self.scoutByName.reset_cooldown(ctx)
            return
        myCupAmount = userData["cups"]
        cupsAmount = randomUser["cups"]
        coinsHeld = randomUser["coins"]
        cardboard = randomUser["cardboard"]
        attackID = randomUser["attackID"]
        sunglasses = randomUser["sunglasses"]
        binoculars = randomUser["binoculars"]
        if myCupAmount > cupsAmount:
            oddsOfWinningNumerator = ((myCupAmount+cupsAmount)/2)-cupsAmount
        else:
            oddsOfWinningNumerator = ((myCupAmount + cupsAmount) / 2) - myCupAmount
        oddsOfWinning = oddsOfWinningNumerator/(myCupAmount+1)
        channel = await member.create_dm()
        await channel.send(f"You found {user.name}'s information on the dark web. They currently hold {cupsAmount} cups.\n"
                            f"They also have {coinsHeld} coins to their name.\n"
                            f"Defense: {cardboard}\n"
                           f"Sunglasses: {sunglasses}\n"
                           f"'Nocs: {binoculars}\n"
                            f"Your chances of beating them in a fight: {oddsOfWinning}.\n"
                            f"Their attackID (used to attack them specifically) is {attackID}.")



    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="steal",
        help="Steal from random people. Why would you do that?"
    )
    async def steal(self, ctx: commands.Context):
        member = ctx.author

        userData, collection = await fetchData(self.bot, member.id)
        async for doc in collection.aggregate([{ "$sample": { "size": 1 } }]):

            randomUser = doc
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            await ctx.send(f"Your theft failed. Good!")
            return
        moneyReceived = random.randint(0, 1000)
        userData["coins"] += moneyReceived
        randomUser["coins"]-= moneyReceived
        await ctx.send(f"You earned {moneyReceived} coins by stealing from {user.name}")
        await collection.replace_one({"_id": member.id}, userData)

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="attack",
        help="Attack random people with the power of your cups.",

    )
    async def attack(self, ctx: commands.Context, *, attackID: str = "-1"):
        member = ctx.author
        fightBonus = 30
        userData, collection = await fetchData(self.bot, member.id)
        if(attackID == "-1"):
            async for doc in collection.aggregate([{"$sample": {"size": 1}}]):
                randomUser = doc
        else:
            randomUser = await findByAttackID(self.bot, attackID)

        if randomUser is None:
            await ctx.send(f"Either this person's attack ID has changed, or you copied it wrong!")
            self.attack.reset_cooldown(ctx)
            return
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            await ctx.send(f"You attacked yourself?. How?!")
            return
        defense = random.randint(0, randomUser["cardboard"])
        yourAttack = random.randint(0, userData["cups"])
        theirAttack = random.randint(0, randomUser["cups"])
        if(yourAttack > theirAttack + defense):
            await ctx.send(f"You won the fight with {yourAttack} attack against {user.name} who lamely produced "
                           f"{theirAttack} attack power and {defense} defense.")
            coinsEarned = (yourAttack - theirAttack) * fightBonus
            userData["coins"] += coinsEarned
            randomUser["coins"] -= coinsEarned
            await ctx.send(f"You earned {coinsEarned} coins from your opponent fair and square.")
        else:
            await ctx.send(f"You lost the fight with {yourAttack} attack against {user.name} who valiantly produced "
                           f"{theirAttack} attack power and {defense} defense.")
            coinsEarned = (theirAttack - yourAttack) * fightBonus
            randomUser["coins"] += coinsEarned
            userData["coins"] -= coinsEarned
            await ctx.send(f"You honorably hand {coinsEarned} coins to your opponent.")

        await collection.replace_one({"_id": member.id}, userData)
        await collection.replace_one({"_id": user.id}, randomUser)
        await updateAttackID(self.bot, user.id)

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="meme",
        help="Generate a meme from one of the meme genres."
    )
    async def meme(self, ctx: commands.Context, genre: str = ""):

        meme = await fetchMeme(self.bot, genre)

        msg = await ctx.send(meme["_id"])

        #await asyncio.sleep(15)
        sticker = msg.stickers
        embeds = msg.embeds
        flags = msg.flags
        interaction = msg.interaction
        webhook_id = msg.webhook_id
        attachments = msg.attachments
        nonce = msg.nonce
        components = msg.components
        #await ctx.send(f"Embeds: {embeds}\n"
                       #f"Webhook_id: {webhook_id}\n"
                       #f"Flags: {flags}\n"
                       #f"Interaction: {interaction}\n"
                       #f"Nonce: {nonce}\n"
                       #f"Components: {components}\n"
                       #f"Stickers: {sticker}\n"
                       #f"Attachments: {attachments}")
        #notAllowedExt = [".io", ".com", ".org", ".gov",".io/"]
        #name, extension = os.path.splitext(meme["_id"])
        #if extension in notAllowedExt:
        #    await ctx.send(f"This doesn't come from the expected sources, deleting from database.")
        #    await msg.delete()
        #    await removeMeme(self.bot, meme["_id"])
        #    return
        #if len(embeds) <= 0:
        #    await ctx.send(f"This doesn't look like a meme, I'm sorry! Removed from database, try again!")
        #    await msg.delete()
        #    await removeMeme(self.bot, meme["_id"])


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="addmeme",
        help="Add a meme by giving it a genre and an image url (copy image address/location and paste)."
    )
    async def addNewMeme(self, ctx: commands.Context, genre: str = "", url: str = None):
        await asyncio.sleep(6)
        msg = ctx.message

        if len(msg.embeds) == 0:
            await ctx.send("This won't be accepted as an image/gif")
            return
        if url is None:
            await ctx.send("You didn't enter an image url")
            return
        if genre == "":
            await ctx.send("You need to choose a genre for this meme to be referenced by.")
            return
        if genre not in self.acceptedGenres:
            await ctx.send(f"You need to choose a genre from this list: {self.acceptedGenres}")
            return
        name, extension = os.path.splitext(url)
        # List valid extensions
        #ext = [".png", ".jpg", ".jpeg", ".cr2", ".nef", ".tif", ".bmp", ".gif"]
        notAllowedExt = [".io", ".com", ".org", ".gov",".io/",""]

        if extension in notAllowedExt:
            await ctx.send(f"You need to use a real image, preferably from an online source.")
            return
        try:
            await addMeme(self.bot,genre,url)
            await ctx.send("Oh boy, a new meme added!")
        except:
            await ctx.send("This meme has probably already been added to the Memedex")

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="memetypes",
        help="Show which genres of memes you can upload to the bot."
    )
    async def memeTypes(self, ctx: commands.Context, genre: str = ""):

        await ctx.send(f"Meme types allowed for adding: {self.acceptedGenres}")

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="kanye",
        aliases=["thegoat"],
        help="Get a random Yeezy quote."
    )
    async def kanye(self, ctx: commands.Context):

        response = requests.get("https://api.kanye.rest/")
        data = response.json()
        quote = data["quote"]
        await ctx.send(f"Kanye says: {quote}")


async def setup(bot: commands.Bot):

    await bot.add_cog(
        funActions(bot)
    )