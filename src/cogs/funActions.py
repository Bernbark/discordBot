# A good template for cogs
import asyncio
import random
import requests
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from fetchData import find_by_attack_id, update_attack_id, fetch_meme, add_meme, remove_meme, fetch_data
from botUtilities import make_embed
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

        userData, collection = await fetch_data(self.bot, member.id)
        async for doc in collection.aggregate([{"$sample": {"size": 1}}]):
            randomUser = doc
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            embed=make_embed(f"Your theft failed. Good!")
            await ctx.send(embed=embed)
            return
        theftPower = random.randint(0, userData["sunglasses"])
        theftDefense = randomUser["binoculars"]
        if theftDefense > theftPower:
            moneyLost = random.randint(0, 1000)
            userData["coins"] -= moneyLost
            randomUser["coins"] += moneyLost
            embed = make_embed(f"Your theft attempt failed miserably. Lost {moneyLost} coins in your scramble to get away"
                           f" from {user.name}.")
            await ctx.send(embed=embed)
        elif theftPower > theftDefense:
            cupsGained = random.randint(0, (theftPower-theftDefense))
            userData["cups"] += cupsGained
            randomUser["cups"] -= cupsGained
            if randomUser["cups"]<0:
                randomUser["cups"] = 0
            embed = make_embed(
                f"Your theft was very successful. Stole {cupsGained} cups from {user.name}.")
            await ctx.send(embed=embed)
            await ctx.send()
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
                embed=make_embed(f"Your theft attempt failed miserably. Lost {moneyLost} coins in your scramble to get away from"
                    f" your equal in espionage, {user.name}.")
                await ctx.send(embed=embed)
            else:
                cupsGained = 1
                userData["cups"] += cupsGained
                randomUser["cups"] -= cupsGained
                if randomUser["cups"] < 0:
                    randomUser["cups"] = 0
                embed = make_embed(
                    f"Your theft was minimally successful because your spy power was the same as their spy"
                    f" resistance. Stole 1 cup from your equal in espionage, {user.name}.")
                await ctx.send(embed=embed)

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

        userData, collection = await fetch_data(self.bot, member.id)
        async for doc in collection.aggregate([{"$sample": {"size": 1}}]):
            randomUser = doc
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            embed = make_embed(
                f"Your scout failed. Good!")
            await ctx.send(embed=embed)
            return

        myCupAmount = userData["cups"]

        cupsAmount = randomUser["cups"]
        coinsHeld = randomUser["coins"]
        cardboard = randomUser["cardboard"]
        attackID = randomUser["attackID"]
        sunglasses = randomUser["sunglasses"]
        binoculars = randomUser["binoculars"]
        position = randomUser["position"]
        if myCupAmount > cupsAmount:
            oddsOfWinningNumerator = (myCupAmount/2)/(cupsAmount+1)/2
        else:
            oddsOfWinningNumerator = (cupsAmount/2)/(myCupAmount+1)/2
        oddsOfWinning = oddsOfWinningNumerator/(myCupAmount+1)
        channel = await member.create_dm()
        await channel.send(f"You found {user.name}'s information on the dark web. They currently hold {cupsAmount} cups.\n"
                            f"They also have {coinsHeld} coins to their name.\n"
                            f"Defense: {cardboard}\n"
                           f"Sunglasses: {sunglasses}\n"
                           f"'Nocs: {binoculars}\n"
                           f"World Map Location: {position}\n"
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

        userData, collection = await fetch_data(self.bot, member.id)
        if user is None:
            embed = make_embed(
                f"Either this person's user name has changed, or you copied it wrong!")
            await ctx.send(embed=embed)

            self.scoutByName.reset_cooldown(ctx)
            return
        else:
            randomUser, collection = await fetch_data(self.bot, user.id)

        if randomUser is None:
            embed = make_embed(
                f"Either this person's attack ID has changed, or you copied it wrong!")
            await ctx.send(embed=embed)
            self.scoutByName.reset_cooldown(ctx)
            return

        if user == member or user is None:
            embed = make_embed(
                f"Your scout failed for unusual reasons...")
            await ctx.send(embed=embed)
            self.scoutByName.reset_cooldown(ctx)
            return

        myCupAmount = userData["cups"]
        cupsAmount = randomUser["cups"]
        coinsHeld = randomUser["coins"]
        cardboard = randomUser["cardboard"]
        attackID = randomUser["attackID"]
        sunglasses = randomUser["sunglasses"]
        binoculars = randomUser["binoculars"]
        position = randomUser["position"]

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
                           f"World Map Location: {position}\n"
                            f"Your chances of beating them in a fight: {oddsOfWinning}.\n"
                            f"Their attackID (used to attack them specifically) is {attackID}.")



    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="steal",
        help="Steal from random people. Why would you do that?"
    )
    async def steal(self, ctx: commands.Context):
        member = ctx.author

        userData, collection = await fetch_data(self.bot, member.id)
        async for doc in collection.aggregate([{ "$sample": { "size": 1 } }]):

            randomUser = doc
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            embed = make_embed(f"Your theft failed. Good!")
            await ctx.send(embed=embed)
            return
        moneyReceived = random.randint(0, 1000)
        userData["coins"] += moneyReceived
        randomUser["coins"]-= moneyReceived
        embed = make_embed(f"You earned {moneyReceived} coins by stealing from {user.name}")
        await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, userData)

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(
        name="attack",
        help="Attack random people with the power of your cups."
    )
    async def attack(self, ctx: commands.Context, *, attackID: str = "-1"):
        member = ctx.author
        fightBonus = 30
        userData, collection = await fetch_data(self.bot, member.id)
        if attackID == "-1":
            async for doc in collection.aggregate([{"$sample": {"size": 1}}]):
                randomUser = doc
        else:
            randomUser = await find_by_attack_id(self.bot, attackID)

        if randomUser is None:
            embed = make_embed(f"Either this person's attack ID has changed, or you copied it wrong!")
            await ctx.send(embed=embed)
            self.attack.reset_cooldown(ctx)
            return
        user = self.bot.get_user(randomUser["_id"])
        if user == member or user is None:
            embed = make_embed(f"You attacked yourself?. How?!")
            await ctx.send(embed=embed)
            return
        defense = random.randint(0, randomUser["cardboard"])
        yourAttack = random.randint(0, userData["cups"])
        theirAttack = random.randint(0, randomUser["cups"])
        if(yourAttack > theirAttack + defense):
            coinsEarned = (yourAttack - theirAttack) * fightBonus
            userData["coins"] += coinsEarned
            randomUser["coins"] -= coinsEarned
            embed = make_embed(f"You won the fight with {yourAttack} attack against {user.name} who lamely produced "
                           f"{theirAttack} attack power and {defense} defense.",f"You earned {coinsEarned} coins from your opponent fair and square.")
            await ctx.send(embed=embed)
        else:
            coinsEarned = (theirAttack - yourAttack) * fightBonus
            randomUser["coins"] += coinsEarned
            userData["coins"] -= coinsEarned
            embed = make_embed(f"You lost the fight with {yourAttack} attack against {user.name} who valiantly produced "
                           f"{theirAttack} attack power and {defense} defense.",f"You honorably hand {coinsEarned} coins to your opponent.")
            await ctx.send(embed=embed)
        await collection.replace_one({"_id": member.id}, userData)
        await collection.replace_one({"_id": user.id}, randomUser)
        await update_attack_id(self.bot, user.id)

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="meme",
        help="Generate a meme from one of the meme genres."
    )
    async def meme(self, ctx: commands.Context, genre: str = ""):

        meme = await fetch_meme(self.bot, genre)
        await ctx.send(content=meme["_id"])


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="addmeme",
        help="Add a meme by giving it a genre and an image url (copy image address/location and paste)."
    )
    async def addNewMeme(self, ctx: commands.Context, genre: str = "", url: str = None):
        await asyncio.sleep(6)
        msg = ctx.message

        if len(msg.embeds) == 0:
            embed = make_embed("This won't be accepted as an image/gif")
            await ctx.send(embed=embed)
            return
        if url is None:
            embed = make_embed("You didn't enter an image url")
            await ctx.send(embed=embed)
            return
        if genre == "":
            embed = make_embed("You need to choose a genre for this meme to be referenced by.")
            await ctx.send(embed=embed)
            return
        if genre not in self.acceptedGenres:
            embed = make_embed(f"You need to choose a genre from this list: {self.acceptedGenres}")
            await ctx.send(embed=embed)
            return
        name, extension = os.path.splitext(url)
        # List valid extensions
        #ext = [".png", ".jpg", ".jpeg", ".cr2", ".nef", ".tif", ".bmp", ".gif"]
        notAllowedExt = [".io", ".com", ".org", ".gov",".io/",""]

        if extension in notAllowedExt:
            embed = make_embed(f"You need to use a real image, preferably from an online source.")
            await ctx.send(embed=embed)
            return
        try:
            await add_meme(self.bot,genre,url)
            embed = make_embed("Oh boy, a new meme added!")
            await ctx.send(embed=embed)
        except:
            embed = make_embed("This meme has probably already been added to the Memedex")
            await ctx.send(embed=embed)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="memetypes",
        help="Show which genres of memes you can upload to the bot."
    )
    async def memeTypes(self, ctx: commands.Context, genre: str = ""):

        embed = make_embed("Allowed types for adding:",f"{self.acceptedGenres}")
        await ctx.send(embed=embed)

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
        embed=make_embed(f"Kanye says: {quote}")
        await ctx.send(embed=embed)

    #   %3F - this is the code for question marks
    #   %0D%0A - new line in url
    #   %25 - this is the code for question marks
    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="cat",
        help="Generate a cat pic."
    )
    async def cat(self, ctx: commands.Context):
        says = ctx.message.content
        print(says)
        if says == "!cat":
            request = requests.get("https://cataas.com/cat?json=true")
            data = request.json()
            url = data["url"]
            await ctx.send("https://cataas.com"+url)
        else:
            newStr = says.strip()
            clean_str = newStr.replace('!cat ','')
            #refStr = refStr.replace('%', '%25')

            url_parts = []
            if len(clean_str) > 26:
                words = clean_str.split(' ')
                line_break = 8
                i=1
                if len(words) > 1:
                    for word in words:
                        if "." in word or i==line_break:
                            url_parts.append(word.strip('%0D%0A') + "%0D%0A")
                            i = 0
                        else:
                            url_parts.append(word.strip('%0D%0A') + " ")
                        i += 1
                    print(f"{url_parts}")
                    url = ''.join(url_parts)
                    clean_url = url.replace('?', '%3F')
                    request = requests.get("https://cataas.com/cat/says/"+clean_url+"?json=true")
                    data = request.json()
                    url = data["url"]
                    await ctx.send("https://cataas.com" + url)
                    return
                else:
                    chars = []
                    chars.extend(clean_str)
                    line_break = 20
                    i = 1
                    for char in chars:
                        if "." in char or i == line_break:
                            url_parts.append(char.strip('%0D%0A') + "%0D%0A")
                            i = 0
                        else:
                            url_parts.append(char.strip('%0D%0A') + "")
                        i += 1
                    url = ''.join(url_parts)
                    clean_url = url.replace('?', '%3F')
                    print(f"{url_parts}")
                    request = requests.get("https://cataas.com/cat/says/" + clean_url + "?json=true")
                    data = request.json()
                    url = data["url"]
                    await ctx.send("https://cataas.com" + url)
                    return

            #cleanStr = refStr.replace(' ','%20')
            clean_str = clean_str.replace('?', '%3F')
            url = "https://cataas.com/cat/says/"+clean_str+"?json=true"


            request = requests.get(url)
            data = request.json()
            url = data["url"]
            await ctx.send("https://cataas.com"+url)
#https://cataas.com/cat/says/Why%20is%20this%20happening%20to%20me

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="catfact",
        help="Generate a cat fact."
    )
    async def cat_fact(self, ctx: commands.Context):
        request = requests.get("https://meowfacts.herokuapp.com/")
        data = request.json()
        fact = data["data"][0]
        await ctx.send(f"Cat fact: {fact}")


async def setup(bot: commands.Bot):

    await bot.add_cog(
        funActions(bot)
    )