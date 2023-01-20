# A good template for cogs
import asyncio
import random
import time
import discord
from discord.ext import commands
from fetchData import fetchData, removeAccount
from discord.ui import Button, View, Modal

class DynamiteButton(Button):
    def __init__(self, style, label):
        super().__init__(label=label, emoji="🧨",)
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

        color = random.choice(list(self.colors.values()))
        label = random.choice(self.labels)
        dynaButton = DynamiteButton(color,label)
        try:
            self.view.add_item(dynaButton)
        except ValueError:
            self.view.clear_items()
            await interaction.response.edit_message(content="You lose! The board filled with too many sticks of dynamite",
                                                    view=self.view)
            self.view.stop()
        newList = self.view.children
        if len(newList) > 2:
            self.view.clear_items()
            random.shuffle(newList)

            for item in newList:
                self.view.add_item(item)
            await interaction.response.edit_message(content="Fail",
                                                    view=self.view)
        else:
            self.view.clear_items()
            await interaction.response.edit_message(content="You lose!",
                                                    view=self.view)
            self.view.stop()

class DynamiteGame(View):

    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.ctx = ctx
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

    @discord.ui.button(label="Click me!",style=discord.ButtonStyle.blurple, emoji="😎", custom_id="goodButton")
    async def button_callback(self, interaction, button):
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
            await interaction.response.edit_message(content="Good job",
                                                    view=self)
        else:

            self.clear_items()
            await interaction.response.edit_message(content="You win!",
                                                    view=self)
            self.stop()


    async def on_timeout(self):

        self.clear_items()


        await self.ctx.message.delete()
        self.stop()




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

gameLoopTime = 20

arithmetic = ['+',
              '-',
              '*']
def new_equation_easy():
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
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="dynamite", help="Don't Click The Dynamite!")
    async def dynamite(self, ctx: commands.Context):
        """
        Dynamite game using Discord's UI
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
                Type <prefix>math BET_AMOUNT You can play by betting a certain amount or just typing <prefix>m spends 10 gold to play
                """
        winnings = int(bet) * 2
        member = ctx.author
        gameLoopTime = 20
        userData, collection = await fetchData(self.bot, member.id)
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
            embed = await makeEmbed(f"EQUATION: {equation}", f"Here we go!", "")
            msg = await ctx.send(embed=embed)

            counter = 0
            correct = 0
            while counter <= gameLoopTime:
                try:
                    choice = await self.bot.wait_for('message', timeout=3.8,
                                                     check=lambda message: message.author == ctx.author)
                    if str(choice.content) == "quit" or str(choice.content) == "exit" or str(choice.content) == "stop":

                        correct = 0
                        counter = 999

                        embed = await makeEmbed(f"You quit!",
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
                            embed= await makeEmbed(f"EQUATION: {equation}",f"TIME LEFT: {time_left} seconds.","")
                            await msg.edit(embed=embed)
                        else:
                            embed = await makeEmbed(f"EQUATION: {equation}",f"TIME ALMOST UP : {time_left} seconds.","")
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
                        embed = await makeEmbed(f"EQUATION: {equation}", f"Sorry, wrong, 2 second penalty, time left: {time_left} seconds",
                                          "")
                        await msg.edit(embed=embed)

                except asyncio.TimeoutError:
                    counter += 3
                    time_left = gameLoopTime - counter
                    embed = await makeEmbed(f"EQUATION: {equation}",
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
                Type <prefix>math BET_AMOUNT You can play by betting a certain amount or just typing <prefix>m spends 10 gold to play
                """
        winnings = int(bet) * 2
        member = ctx.author
        gameLoopTime = 30
        userData, collection = await fetchData(self.bot, member.id)
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
            embed = await makeEmbed(f"EQUATION: {equation}", f"Here we go!", "")
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

                        embed = await makeEmbed(f"You quit!",
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
                            embed = await makeEmbed(f"EQUATION: {equation}", f"TIME LEFT: {time_left} seconds.", "")
                            await msg.edit(embed=embed)
                        else:
                            embed = await makeEmbed(f"EQUATION: {equation}", f"TIME ALMOST UP : {time_left} seconds.",
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
                        embed = await makeEmbed(f"EQUATION: {equation}",
                                                f"Sorry, wrong, 2 second penalty, time left: {time_left} seconds",
                                                "")
                        await msg.edit(embed=embed)

                except asyncio.TimeoutError:
                    counter += 3
                    time_left = gameLoopTime - counter
                    embed = await makeEmbed(f"EQUATION: {equation}",
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

    """
    Let's make a whack-a-mole style game, avoid the dynamite, and the more dynamite they avoid, the better score
    """





async def setup(bot: commands.Bot):

    await bot.add_cog(
        games(bot)
    )
