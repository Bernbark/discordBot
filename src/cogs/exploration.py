# A good template for cogs
import asyncio
import random
import time
import discord
from discord.ext import commands
from src.fetchData import fetch_data, update_world_map, fetch_inventory, make_weapon_serializable, fetch_player_map_info
from discord.ui import Button, View, Select
from botUtilities import make_embed
from src.items.randomizeItem import randomize_weapon

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


def boss_battle(health, position, view):
    boss_name = random.choice(enemyNames)
    distanceBuff = abs(position["horizontal"]) + abs(position["vertical"])
    enemyHealth = random.randint(100 + distanceBuff, 1000 + distanceBuff)
    health -= enemyHealth
    description = ""
    if health > 0:

        goldEarned = random.randint(0 + health, 1000 + health)
        description = f"You fought a BOSS {boss_name} who had {enemyHealth} health and won!\nEarned {goldEarned} coins.\n"
        view.goldEarned += goldEarned
    else:
        description = "You lost miserably to the boss, try again in 50 steps!"
        health = 0
    return description, health


def check_for_major_event(view):
    description = ""
    health = view.health
    if view.steps % 50 == 0:
        description, health = boss_battle(view.health, view.position, view)
    return description, health


def normal_battle(health, position, view):
    distanceBuff = abs(position["horizontal"]) + abs(position["vertical"])
    enemyHealth = random.randint(0 + distanceBuff, 100 + distanceBuff)
    health -= enemyHealth
    goldEarned = random.randint(0 + health, 1000 + health)
    view.goldEarned += goldEarned
    return health, enemyHealth, goldEarned


def stranger_encounter(view):
    chanceNumber = random.randint(0, 100)

    if chanceNumber <= 30:
        healthEarned = (chanceNumber + 1) * 10
        view.health += healthEarned
        description = f"\nGained {healthEarned} health.\n"
        return description, view
    elif chanceNumber <= 70:
        view.goldEarned += (chanceNumber + 1) * 100
        description = f"\nGained {(chanceNumber + 1) * 100} gold.\n"
        return description, view
    else:
        # maybe gain an item? i dunno yet sheesh
        description = f"\nHe walked away before you could talk to him.\n"
        return description, view


# come up with random encounters for the player to deal with
def random_encounter(health, position, view):
    chanceNumber = random.randint(0, 100)
    if chanceNumber <= 10:
        # gain gold
        newHealth = health
        goldEarned = random.randint(0 + health, 1000 + health)
        view.goldEarned += goldEarned

        return f"You gained {goldEarned} gold!", newHealth, view
    elif chanceNumber <= 20:
        # fight a player
        newHealth = health
        return "You found a player's base.", newHealth, view
    elif chanceNumber <= 70:
        # fight a normal enemy
        newHealth, enemyHealth, gold = normal_battle(health, position, view)
        if newHealth > 0:
            view.goldEarned += gold
            return f"You fight a {random.choice(enemyNames)} who has {enemyHealth} HP. You survive the battle. Earn {gold} gold", newHealth, view
        else:
            return f"You fight a {random.choice(enemyNames)} who has {enemyHealth} HP. You are overwhelmed.", newHealth, view
    else:
        # mysterious stranger?
        description, view = stranger_encounter(view)
        newHealth = health
        return f"You find the mysterious stranger! {description}", newHealth, view


def player_info(health, position, steps):
    return f"\nPlayer health: {health}\n" \
           f"Position:{position}\n" \
           f"Steps: {steps}"


class ExploreNorth(Button):
    def __init__(self):
        super().__init__(label="^", style=discord.ButtonStyle.blurple, row=1)

    async def callback(self, interaction: discord.Interaction):
        self.view.position["vertical"] += 1
        await travel(self.view, interaction, "North")


class ExploreWest(Button):
    def __init__(self):
        super().__init__(label="<", style=discord.ButtonStyle.blurple, row=2)

    async def callback(self, interaction: discord.Interaction):
        self.view.position["horizontal"] -= 1
        await travel(self.view, interaction, "West")


class ExploreEast(Button):
    def __init__(self):
        super().__init__(label=">", style=discord.ButtonStyle.blurple, row=2)

    async def callback(self, interaction: discord.Interaction):
        self.view.position["horizontal"] += 1
        await travel(self.view, interaction, "East")


class ExploreSouth(Button):
    def __init__(self, ):
        super().__init__(label="v", style=discord.ButtonStyle.blurple, row=3)

    async def callback(self, interaction: discord.Interaction):
        self.view.position["vertical"] -= 1
        await travel(self.view, interaction, "South")


class SpacerButton(Button):
    def __init__(self, row):
        super().__init__(emoji="🧇", style=discord.ButtonStyle.blurple, row=row)

    async def callback(self, interaction: discord.Interaction):
        if self.view.health > 0:
            description, self.view.health, newView = random_encounter(self.view.health, self.view.position, self.view)
            await interaction.response.edit_message(content="", view=newView,
                                                    embed=make_embed("Don't click the waffles...",
                                                                     f"{description}{player_info(self.view.health, self.view.position, self.view.steps)}",
                                                                     ""))
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="", view=self.view,
                                                    embed=make_embed("You are dead! Await your results.",
                                                                     f"{player_info(self.view.health, self.view.position, self.view.steps)}",
                                                                  ""))


class ExploreView(View):
    def __init__(self, health, position, bot, ctx, steps, user_data, collection):
        super().__init__(timeout=10)
        self.health = health + 100
        self.position = position
        self.goldEarned = 0
        self.bot = bot
        self.ctx = ctx
        self.user_data = user_data
        self.collection = collection
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
        self.steps = steps
        # let's eventually save where the player is "resting", when player's scout each other,
        # they can see this position
        # and try to reach it for extra rewards

    # 61 203 63 225
    async def on_timeout(self):
        print("Explore: timeout")
        self.user_data["position"] = self.position
        self.user_data["coins"] += self.goldEarned
        await self.collection.replace_one({"_id": self.ctx.author.id}, self.user_data)
        await self.ctx.send(f"{self.ctx.author.name} earned {self.goldEarned} gold on their adventure.")
        await update_world_map(self.bot, self.user_data["_id"], self.position, self.steps)


async def check_for_items(description: str, view: ExploreView, interaction: discord.Interaction):
    if description == "":
        return
    else:
        weapon = randomize_weapon(view.ctx.author.id)
        inventory, collection = await fetch_inventory(view.bot, view.ctx.author.id)
        weapon_dict = make_weapon_serializable(weapon)
        inventory["inventory_weapon"].append(weapon_dict)
        await collection.replace_one({"_id": view.ctx.author.id}, inventory)
        await asyncio.sleep(2)
        await interaction.followup.edit_message(content=f"Earned {weapon}", view=view,
                                                embed=make_embed("Boss defeated!",
                                                                 f"{description}{player_info(view.health, view.position, view.steps)}",
                                                                 ""), message_id=interaction.message.id)


async def travel(view: ExploreView, interaction: discord.Interaction, direction: str):
    if view.health > 0:
        description, view.health, newView = random_encounter(view.health, view.position, view)
        await interaction.response.edit_message(content="", view=newView, embed=make_embed(f"Went {direction}",
                                                                                           f"{description}{player_info(view.health, view.position, view.steps)}",
                                                                                           ""))
        view.steps += 1
        description, view.health = check_for_major_event(view)
        await check_for_items(description, view, interaction)
    else:
        view.clear_items()
        await interaction.response.edit_message(content="", view=view,
                                                embed=make_embed("You are dead! Await your results.",
                                                                 f"{player_info(view.health, view.position, view.steps)}",
                                                                 ""))


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

        userData, collection = await fetch_data(self.bot, ctx.author.id)
        health = userData["cups"]

        position = userData["position"]
        map_info, map_collection = await fetch_player_map_info(self.bot, ctx.author.id)
        steps = map_info["steps"]
        view = ExploreView(health, position, self.bot, ctx, steps, userData, collection)
        embed = make_embed(f"Exploration began at position: {position}", "You get to make the best of "
                                                                         "this exploration as long as you stay alive...Good luck!")
        msg = await ctx.send(embed=embed, view=view)



async def setup(bot: commands.Bot):
    await bot.add_cog(
        exploration(bot)
    )
