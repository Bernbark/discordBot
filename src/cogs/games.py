# A good template for cogs
import asyncio
import random
import time
import discord
from discord.ext import commands
from fetchData import fetch_data
from discord.ui import Button, View
from botUtilities import make_embed


class DynamiteButton(Button):
    """
    The subclass responsible for templating dynamite buttons and their behavior
    """
    def __init__(self, style, label):
        super().__init__(label=label, emoji="🧨")
        self.colors = { "red": discord.ButtonStyle.red,
                        "blurple": discord.ButtonStyle.blurple,
                        "green": discord.ButtonStyle.green,
                        "grey": discord.ButtonStyle.grey}
        self.labels = [
            "Don't click me!",
            "Click m3!",
            "Don't hurt me!",
            "Wait!",
            "Stop!",
            "Go Ahead, Click My Day",
            "Don't click me!",
            "DANGER",
            "Safe",
            "Click me?"
        ]
        self.style = style

    async def callback(self, interaction: discord.Interaction):
        """
        A necessary method for buttons in Discord.py UI, this is what the button should do when clicked, in this case
        we want to create more dynamite when dynamite is clicked, or decide if the game is over due to clicking it.
        """
        color = random.choice(list(self.colors.values()))
        label = random.choice(self.labels)
        dynaButton = DynamiteButton(color,label)
        try:
            self.view.add_item(dynaButton)
        except ValueError:
            self.view.clear_items()

            await interaction.response.edit_message(embed=make_embed("You lose! The board filled with too many sticks of dynamite"),
                                                    view=self.view)
            self.view.stop()
        newList = self.view.children
        if len(newList) > 2:
            self.view.clear_items()
            random.shuffle(newList)

            for item in newList:
                self.view.add_item(item)
            await interaction.response.edit_message(embed=make_embed("Fail"),
                                                    view=self.view)
        else:
            self.view.clear_items()
            await interaction.response.edit_message(embed=make_embed("You lose!"),
                                                    view=self.view)
            self.view.stop()


class DynamiteGame(View):
    """
    One of the coolest parts about using the View as a class is that we can add behavior to it. Such as tracking game
    stats like the count variable that will tell us how many times the user clicked a "correct" button in the main
    function calling the game, dynamite().
    """
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.ctx = ctx
        # This can definitely be done better
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red,"Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red,"Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red,"Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red,"Don't click me!")
        self.add_item(self.dynaButton1)
        self.add_item(self.dynaButton2)
        self.add_item(self.dynaButton3)
        self.add_item(self.dynaButton4)
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.add_item(self.dynaButton1)
        self.add_item(self.dynaButton2)
        self.add_item(self.dynaButton3)
        self.add_item(self.dynaButton4)
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.add_item(self.dynaButton1)
        self.add_item(self.dynaButton2)
        self.add_item(self.dynaButton3)
        self.add_item(self.dynaButton4)
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.add_item(self.dynaButton1)
        self.add_item(self.dynaButton2)
        self.add_item(self.dynaButton3)
        self.add_item(self.dynaButton4)
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")

        self.add_item(self.dynaButton1)
        self.add_item(self.dynaButton2)
        self.add_item(self.dynaButton3)
        self.add_item(self.dynaButton4)
        self.dynaButton1 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton2 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton3 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")
        self.dynaButton4 = DynamiteButton(discord.ButtonStyle.red, "Don't click me!")

        self.add_item(self.dynaButton1)
        self.add_item(self.dynaButton2)
        self.add_item(self.dynaButton3)
        self.add_item(self.dynaButton4)
        self.colors = {"red": discord.ButtonStyle.red,
                       "blurple": discord.ButtonStyle.blurple,
                       "green": discord.ButtonStyle.green,
                       "grey": discord.ButtonStyle.grey}
        self.labels = [
            "Don't click me!",
            "Click m3!",
            "Don't hurt me!",
            "Wait!",
            "Stop!",
            "Go Ahead, Click My Day",
            "Don't click me!",
            "DANGER",
            "Safe",
            "Click me?"
        ]
        self.emojis = [
            "🎐",
            "🏒",
            "🏑",
            "😎"
        ]
        self.count = 0

    """
    def addExplosion(self):
        explosionButton = create_explosion(self.ctx, self)
        return explosionButton

    @discord.ui.button(label="Don't click me!", style=discord.ButtonStyle.grey, emoji="✨", custom_id="explosion")
    async def explosion_button_callback(self,interaction, button):

        explosionButton = self.addExplosion()
        explosionButton.callback = self.explosion_button_callback
        self.add_item(explosionButton)
    """
    # I wanted to subclass this button as well, but decided the functionality allowed by keeping it here is what I
    # actually want
    @discord.ui.button(label="Click me!",style=discord.ButtonStyle.blurple, emoji="😎", custom_id="goodButton")
    async def button_callback(self, interaction, button):
        """
        This method is for the correct button, it shuffles the entire list of buttons, removes one button from the list,
        and then changes the color, label of every button, and the emoji of this button to confuse the player.
        :param interaction: discord Interaction
        :param button: Discord UI
        :return: Nothing
        """
        #if len(self.children) > 2:
            #explosionButton = [x for x in self.children if "explosion" in x.custom_id][0]
            #if explosionButton:
                #self.remove_item(explosionButton)
        self.count+=1
        newList = self.children
        if len(newList) > 2:
            self.clear_items()
            random.shuffle(newList)
            while newList[0].custom_id == "goodButton":
                random.shuffle(newList)
            newList.remove(newList[0])
            color = random.choice(list(self.colors.values()))
            label = random.choice(self.labels)
            emoji = random.choice(self.emojis)
            button.style = color
            button.label = label
            button.emoji = emoji
            for item in newList:
                item.style = random.choice(list(self.colors.values()))
                item.label = random.choice(self.labels)
                self.add_item(item)
            await interaction.response.edit_message(embed=make_embed("Good job"),
                                                    view=self)
        else:

            self.clear_items()
            await interaction.response.edit_message(embed=make_embed("You win!"),
                                                    view=self)
            self.stop()


    async def on_timeout(self):
        """
        This is what happens when the game is no longer interactable, we want to clear the UI
        :return:
        """
        self.clear_items()
        await self.ctx.message.delete()
        self.stop()


gameLoopTime = 20

arithmetic = ['+',
              '-',
              '*']


def new_equation_easy():
    """
    Creates an equation and an answer and returns it as a dict with keys "equation" and "answer". Only uses single
    digits
    """
    first = random.randint(1,10)
    second = random.randint(1,10)
    sign = random.choice(arithmetic)
    if sign is '+':
        return {'equation':str(first)+sign+str(second),'answer':first+second}
    elif sign is '-':
        return {'equation':str(first)+sign+str(second),'answer':first-second}
    else: # '*' multiply
        return {'equation':str(first)+sign+str(second),'answer':first*second}

def new_equation_hard():
    """
    Creates an equation and an answer and returns it as a dict with keys "equation" and "answer". Uses triple digits
    """
    first = random.randint(1,100)
    second = random.randint(1,100)
    sign = random.choice(arithmetic)
    if sign is '+':
        return {'equation':str(first)+sign+str(second),'answer':first+second}
    elif sign is '-':
        return {'equation':str(first)+sign+str(second),'answer':first-second}
    else: # '*' multiply
        return {'equation':str(first)+sign+str(second),'answer':first*second}

class games(commands.Cog):
    """
    The class which organizes all games into one place
    """
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="dynamite", help="Don't Click The Dynamite!")
    async def dynamite(self, ctx: commands.Context):
        """
        Dynamite game using Discord's UI, click buttons until there are none left or 30 seconds runs out.
        """
        # button1 = Button(label="Click me!",style=discord.ButtonStyle.blurple, emoji="😎")
        # button2 = Button(label="Don't click me!", style=discord.ButtonStyle.red, emoji="🧨")
        # button3 = Button()
        view = DynamiteGame(ctx)
        msg = await ctx.send("Hi!", view=view, delete_after=30)
        await asyncio.sleep(30)
        count = view.count
        userName = ctx.author.name
        if count == 0:
            await ctx.send(f"{userName}'s Correct hits: {count}...\n"
                           f"Did you even try?")
        elif count <= 10:
            await ctx.send(f"{userName}'s Correct hits: {count}...\n"
                           f"You should pick up the pace!")
        elif count <= 20:
            await ctx.send(f"{userName}'s Correct hits: {count}...\n"
                           f"You're starting to get it!")
        else:
            await ctx.send(f"{userName}'s Correct hits: {count}...\n"
                           f"Wow that's a lot!")
        """async def button_callback(interaction):
            explosionButton = [x for x in view.children if "explosion" in x.custom_id][0]
            if explosionButton:
                view.remove_item(explosionButton)
            await interaction.response.edit_message(content="Good job",
                                                    view=view)
        async def fail_callback(interaction: discord.Interaction):
            randomNum = random.randint(0,99999999)
            randomNum2 = random.randint(0, -99999999)
            button3 = Button(label="Don't click me!", style=discord.ButtonStyle.gray, emoji="✨",custom_id=f"explosion{ctx.author.id}-{randomNum}+{randomNum2}")
            view.add_item(button3)

            await msg.edit(content="Why would you click the dynamite?",view=view)
            await interaction.response.edit_message(content="Why would you click the dynamite (interaction edit)?",view=view)


        button1.callback = button_callback
        button2.callback = fail_callback

        view.add_item(button1)
        view.add_item(button2)"""

    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(name="math", help="Play the Math Wizard Game.")
    async def mathwiz(self, ctx: commands.Context, *,bet: int = 1):
        """
        Math wizard game is an attempt at a live game, creating equations for the player to solve as quickly as they can
        They're given 20 seconds to answer as many as possible.
        """
        winnings = int(bet) * 2
        member = ctx.author
        gameLoopTime = 20
        userData, collection = await fetch_data(self.bot, member.id)
        if userData["coins"] < 10 or int(bet) > userData["coins"]:
            await ctx.send("You don't have the coin to play this game, go earn more!.")
            return
        else:
            bid = int(bet)
            startTime = time.time()
            if bid > 1000:
                data = new_equation_hard()
            else:
                data = new_equation_easy()
            equation = data['equation']
            answer = data['answer']
            embed = await make_embed(f"EQUATION: {equation}", f"Here we go!", "")
            msg = await ctx.send(embed=embed)

            counter = 0
            correct = 0
            while counter <= gameLoopTime:
                try:
                    # the check here is saying when we receive the next message, only do this if it's from the original
                    # author
                    choice = await self.bot.wait_for('message', timeout=3.8,
                                                     check=lambda message: message.author == ctx.author)
                    if str(choice.content) == "quit" or str(choice.content) == "exit" or str(choice.content) == "stop":

                        correct = 0
                        counter = 999

                        embed = await make_embed(f"You quit!",
                                                f"Quitter! :)",
                                                "")
                        await msg.edit(embed=embed)
                        self.mathwiz.reset_cooldown(ctx)
                        break
                    elif str(choice.content) == str(answer):
                        correct += 1
                        if bid > 1000:
                            data = new_equation_hard()
                        else:
                            data = new_equation_easy()
                        equation = data['equation']
                        answer = data['answer']
                        timeNow = time.time()
                        counter = int(timeNow - startTime)

                        time_left = gameLoopTime - counter
                        if time_left > 0:
                            embed= await make_embed(f"EQUATION: {equation}",f"TIME LEFT: {time_left} seconds.","")
                            await msg.edit(embed=embed)
                        else:
                            embed = await make_embed(f"EQUATION: {equation}",f"TIME ALMOST UP : {time_left} seconds.","")
                            await msg.edit(embed=embed)



                    else:
                        if bid > 1000:
                            data = new_equation_hard()
                        else:
                            data = new_equation_easy()
                        equation = data['equation']
                        answer = data['answer']
                        counter += 2
                        time_left = gameLoopTime - counter
                        embed = await make_embed(f"EQUATION: {equation}", f"Sorry, wrong, 2 second penalty, time left: {time_left} seconds",
                                          "")
                        await msg.edit(embed=embed)

                except asyncio.TimeoutError:
                    counter += 3
                    time_left = gameLoopTime - counter
                    embed = await make_embed(f"EQUATION: {equation}",
                                      f"3 second penalty for no answer in time. Time left {time_left} seconds.",
                                      "")
                    await msg.edit(embed=embed)

            if correct > 0:
                multi = correct * winnings
                await ctx.send(
                    f"Time up! You got {correct} correct. You earned {winnings} points. Multiply by the number correct to get {multi} coins.")
                userData["coins"] += multi - bet

            elif correct == 0:
                userData["coins"] -= bet
                await ctx.send(f"You probably didn't answer in time, you lose all bet money in the process")
            else:
                await ctx.send(f"Sorry, you lose {bet} gold. You couldn't get any answers right. Try again!")
                userData["coins"] -= bet
            await collection.replace_one({"_id": member.id}, userData)

    @commands.command(name="stealmath", help="Play the Math Wizard Game with your friends >:) ")
    async def stealmath(self, ctx: commands.Context, *, bet: int = 1):
        """
        Math wizard game except there is no checking for the correct author, meaning others can intervene (WIP)
        """
        winnings = int(bet) * 2
        member = ctx.author
        gameLoopTime = 30
        userData, collection = await fetch_data(self.bot, member.id)
        if userData["coins"] < 10 or int(bet) > userData["coins"]:
            await ctx.send("You don't have the coin to play this game, go earn more!.")
            return
        else:
            bid = int(bet)
            startTime = time.time()
            if bid > 1000:
                data = new_equation_hard()
            else:
                data = new_equation_easy()
            equation = data['equation']
            answer = data['answer']
            embed = await make_embed(f"EQUATION: {equation}", f"Here we go!", "")
            msg = await ctx.send(embed=embed)

            counter = 0
            correct = 0
            while counter <= gameLoopTime:
                try:
                    choice = await self.bot.wait_for('message', timeout=3.8
                                                     )
                    if str(choice.content) == "quit" or str(choice.content) == "exit" or str(choice.content) == "stop":

                        correct = 0
                        counter = 999

                        embed = await make_embed(f"You quit!",
                                                f"Quitter! :)",
                                                "")
                        await msg.edit(embed=embed)
                        break
                    elif str(choice.content) == str(answer):
                        correct += 1
                        if bid > 1000:
                            data = new_equation_hard()
                        else:
                            data = new_equation_easy()
                        equation = data['equation']
                        answer = data['answer']
                        timeNow = time.time()
                        counter = int(timeNow - startTime)

                        time_left = gameLoopTime - counter
                        if time_left > 0:
                            embed = await make_embed(f"EQUATION: {equation}", f"TIME LEFT: {time_left} seconds.", "")
                            await msg.edit(embed=embed)
                        else:
                            embed = await make_embed(f"EQUATION: {equation}", f"TIME ALMOST UP : {time_left} seconds.",
                                                    "")
                            await msg.edit(embed=embed)



                    else:
                        if bid > 1000:
                            data = new_equation_hard()
                        else:
                            data = new_equation_easy()
                        equation = data['equation']
                        answer = data['answer']
                        counter += 2
                        time_left = gameLoopTime - counter
                        embed = await make_embed(f"EQUATION: {equation}",
                                                f"Sorry, wrong, 2 second penalty, time left: {time_left} seconds",
                                                "")
                        await msg.edit(embed=embed)

                except asyncio.TimeoutError:
                    counter += 3
                    time_left = gameLoopTime - counter
                    embed = await make_embed(f"EQUATION: {equation}",
                                            f"3 second penalty for no answer in time. Time left {time_left} seconds.",
                                            "")
                    await msg.edit(embed=embed)

            if correct > 0:
                multi = correct * winnings
                await ctx.send(
                    f"Time up! You got {correct} correct. You earned {winnings} points. Multiply by the number correct to get {multi} coins.")
                userData["coins"] += multi - bet

            elif correct == 0:
                userData["coins"] -= bet
                await ctx.send(f"You probably didn't answer in time, you lose all bet money in the process")
            else:
                await ctx.send(f"Sorry, you lose {bet} gold. You couldn't get any answers right. Try again!")
                userData["coins"] -= bet
            await collection.replace_one({"_id": member.id}, userData)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        games(bot)
    )
