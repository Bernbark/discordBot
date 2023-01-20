# A good template for cogs
import asyncio
import random
import time
import discord
from discord.ext import commands
from fetchData import fetchData, removeAccount, updateWorldMap
from discord.ui import Button, View, Modal

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

enemyNames = [
    "Goblin",
    "Elf",
    "Stormtrooper",
    "Rocky from Rocky and Bullwinkle",
    "Alvin AND the chipmunks",
    "Jack Black as Nacho Libre",
    "Simp",
    "Angry Neighbor",
    "Crazed Yoga Instructor",
    "Bon Jovi",
    "Wild Boar",
    "Red Stapler",
    "Permanent Clothing Stain"
]




def normal_battle(health,position,view):
    distanceBuff = abs(position["horizontal"])+abs(position["vertical"])
    enemyHealth = random.randint(0+distanceBuff,100+distanceBuff)
    health -= enemyHealth
    goldEarned = random.randint(0 + health, 1000 + health)
    view.goldEarned += goldEarned
    return health, enemyHealth, goldEarned


def stranger_encounter(view):
    chanceNumber = random.randint(0, 100)

    if chanceNumber <= 30:
        healthEarned = (chanceNumber+1) * 10
        view.health += healthEarned
        description = f"\nGained {healthEarned} health.\n"
        return description, view
    elif chanceNumber <= 70:
        view.goldEarned += (chanceNumber+1) * 100
        description = f"\nGained {(chanceNumber + 1) * 100} gold.\n"
        return description, view
    else:
        #maybe gain an item? i dunno yet sheesh
        description = f"\nHe walked away before you could talk to him.\n"
        return description, view



# come up with random encounters for the player to deal with
def random_encounter(health,position,view):
    chanceNumber = random.randint(0,100)
    if chanceNumber <= 10:
        #gain gold
        newHealth = health
        goldEarned = random.randint(0+health,1000+health)
        view.goldEarned += goldEarned

        return f"You gained {goldEarned} gold!",newHealth,view
    elif chanceNumber <= 20:
        #fight a player
        newHealth = health
        return "You found a player's base.",newHealth,view
    elif chanceNumber <= 70:
        #fight a normal enemy
        newHealth, enemyHealth, gold = normal_battle(health,position,view)
        if newHealth > 0:
            view.goldEarned += gold
            return f"You fight a {random.choice(enemyNames)} who has {enemyHealth} HP. You survive the battle. Earn {gold} gold",newHealth,view
        else:
            return f"You fight a {random.choice(enemyNames)} who has {enemyHealth} HP. You are overwhelmed.", newHealth,view
    else:
        #mysterious stranger?
        description, view = stranger_encounter(view)
        newHealth = health
        return f"You find the mysterious stranger! {description}",newHealth,view




def player_info(health,position):
    return f"\nPlayer health: {health}\n" \
           f"Position:{position}"


class ExploreNorth(Button):
    def __init__(self):
        super().__init__(label="^", style=discord.ButtonStyle.blurple,row=1)

    async def callback(self, interaction: discord.Interaction):
        self.view.position["vertical"] += 1
        if self.view.health > 0:
            description, self.view.health, newView = random_encounter(self.view.health, self.view.position, self.view)
            await interaction.response.edit_message(content="", view=newView, embed=await makeEmbed("Went North",
                                                                                                      f"{description}{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="", view=self.view, embed=await makeEmbed("You are dead! Await your results.",
                                                                                                      f"{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))


class ExploreWest(Button):
    def __init__(self):
        super().__init__(label="<", style=discord.ButtonStyle.blurple,row=2)
    async def callback(self, interaction: discord.Interaction):
        self.view.position["horizontal"] -= 1
        if self.view.health > 0:
            description, self.view.health, newView = random_encounter(self.view.health, self.view.position, self.view)
            await interaction.response.edit_message(content="", view=newView, embed=await makeEmbed("Went West",
                                                                                                      f"{description}{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="", view=self.view, embed=await makeEmbed("You are dead! Await your results.",
                                                                                                      f"{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))


class ExploreEast(Button):
    def __init__(self):
        super().__init__(label=">", style=discord.ButtonStyle.blurple,row=2)
    async def callback(self, interaction: discord.Interaction):
        self.view.position["horizontal"] += 1
        if self.view.health > 0:
            description, self.view.health, newView = random_encounter(self.view.health, self.view.position, self.view)
            await interaction.response.edit_message(content="", view=newView, embed=await makeEmbed("Went East",
                                                                                                      f"{description}{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="", view=self.view, embed=await makeEmbed("You are dead! Await your results.",
                                                                                                      f"{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))


class ExploreSouth(Button):
    def __init__(self,):
        super().__init__(label="v", style=discord.ButtonStyle.blurple,row=3)
    async def callback(self, interaction: discord.Interaction):
        self.view.position["vertical"] -= 1
        if self.view.health > 0:
            description, self.view.health, newView = random_encounter(self.view.health,self.view.position,self.view)
            await interaction.response.edit_message(content="",view=newView,embed=await makeEmbed("Went South",f"{description}{player_info(self.view.health,self.view.position)}",""))
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="", view=self.view, embed=await makeEmbed("You are dead! Await your results.",
                                                                                                      f"{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))


class SpacerButton(Button):
    def __init__(self,row):
        super().__init__(emoji="🧇", style=discord.ButtonStyle.blurple,row=row)

    async def callback(self, interaction: discord.Interaction):
        if self.view.health > 0:
            description, self.view.health, newView = random_encounter(self.view.health, self.view.position, self.view)
            await interaction.response.edit_message(content="", view=newView, embed=await makeEmbed("Don't click the waffles...",
                                                                                                      f"{description}{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="", view=self.view, embed=await makeEmbed("You are dead! Await your results.",
                                                                                                      f"{player_info(self.view.health, self.view.position)}",
                                                                                                      ""))



class ExploreView(View):
    def __init__(self, health,position):
        super().__init__()
        self.health = health
        self.position = position
        self.goldEarned = 0
        button = SpacerButton(1)
        self.add_item(button)
        button = ExploreNorth()
        self.add_item(button)
        button = SpacerButton(1)
        self.add_item(button)
        button = SpacerButton(3)
        self.add_item(button)
        button = ExploreSouth()
        self.add_item(button)
        button = SpacerButton(3)
        self.add_item(button)
        button = ExploreWest()
        self.add_item(button)
        button = SpacerButton(2)
        self.add_item(button)
        button = ExploreEast()
        self.add_item(button)
        # let's eventually save where the player is "resting", when player's scout each other, they can see this position
        # and try to reach it for extra rewards



class exploration(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 3000, commands.BucketType.user)
    @commands.command(name="explore", help="Explore the world.")
    async def explore(self, ctx: commands.Context):
        """
        Explore the world using Discord's UI
        """
        # button1 = Button(label="Click me!",style=discord.ButtonStyle.blurple, emoji="😎")
        # button2 = Button(label="Don't click me!", style=discord.ButtonStyle.red, emoji="🧨")
        # button3 = Button()

        userData, collection = await fetchData(self.bot, ctx.author.id)
        health = userData["cups"]

        position = userData["position"]
        view = ExploreView(health,position)
        msg = await ctx.send("You get 2 minutes to make the best of this exploration...Good luck!", view=view, delete_after=120)
        await asyncio.sleep(121)
        userData["position"] = view.position
        userData["coins"] += view.goldEarned
        await collection.replace_one({"_id": ctx.author.id}, userData)
        await ctx.send(f"{ctx.author.name} earned {view.goldEarned} gold on their adventure.")
        await updateWorldMap(self.bot,userData["_id"],view.position,)

async def setup(bot: commands.Bot):

    await bot.add_cog(
        exploration(bot)
    )
