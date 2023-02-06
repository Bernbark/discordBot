import discord
from discord import app_commands
from discord.ext import commands
from src.fetchData import fetch_data, remove_account
from src.botUtilities import make_embed


class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="picture", help="Change your profile picture. Must be a link to an image, "
                                           "use http in front.\n"
                                           "You need to right click the image/gif and copy the image "
                                           "address/location, then"
                                           "paste that after !picture")
    async def change_picture(self, ctx: commands.Context, url: str = ""):

        user_data, collection = await fetch_data(self.bot, ctx.author.id)
        user_data["picUrl"] = url

        await ctx.send(embed=make_embed("Your picture has been changed."))
        await collection.replace_one({"_id": ctx.author.id}, user_data)

    @commands.command(name="resetplease", help="Reset your own profile to default. THERE IS NO WARNING, IT WILL JUST"
                                               " HAPPEN FOR NOW, BEWARE")
    async def reset_account(self, ctx: commands.Context):
        await remove_account(self.bot, ctx.author.id)
        user_data, collection = await fetch_data(self.bot, ctx.author.id)
        my_pic = user_data["picUrl"]
        coins = user_data["coins"]

        own_profile_embed = make_embed(
            str(ctx.message.author.name) + "'s profile'",
            f"**Username:** {ctx.message.author}\n**User ID:** {ctx.message.author.id}"
            f"\nCurrent coins: {coins}", my_pic)

        await ctx.send("Your profile has been reset to default. That means no more coins, cups, or cardboard...for now")
        await ctx.send(embed=own_profile_embed)

    @commands.command(name="profile", help="View someone's profile")
    async def profile(self, ctx: commands.Context, user: discord.User = None):

        user_data, collection = await fetch_data(self.bot, ctx.author.id)
        if user is not None:
            other, collection = await fetch_data(self.bot, user.id)
            other_user = self.bot.get_user(other["_id"])
            other_coins = other["coins"]
            other_image = other["picUrl"]
            other_profile_embed = make_embed(
                str(other_user.name) + "'s profile",
                f"**Username:** {other_user.name}\n**User ID:** {other_user.id}"
                f"\nCurrent coins: {other_coins}", other_image
            )
            await ctx.send(embed=other_profile_embed)
            return

        coins = user_data["coins"]

        channel = await ctx.author.create_dm()
        total_cups = user_data["cups"]
        total_cardboard = user_data["cardboard"]
        total_sunglasses = user_data["sunglasses"]
        total_binoculars = user_data["binoculars"]
        my_pic = user_data["picUrl"]
        own_profile_embed = make_embed(
            str(ctx.author.name) + "'s profile",
            f"**Username:** {ctx.author.name}\n**User ID:** {ctx.author.id}"
            f"\nCurrent coins: {coins}", my_pic
        )

        if user is None:
            await ctx.send(embed=own_profile_embed)
            await channel.send(f"**Username:** {ctx.message.author}\n**User ID:** {ctx.message.author.id}"
                               f"\nCurrent coins: {coins}\n"
                               f"Current Cups: {total_cups}\n"
                               f"Current Cardboard: {total_cardboard}\n"
                               f"Current Sunglasses: {total_sunglasses}\n"
                               f"Current 'nocs: {total_binoculars}")

    @commands.command(name="api", help="Does nothing for now")
    async def my_api(self, ctx: commands.Context, user: discord.User = None):
        # request = requests.get()
        pass

    @app_commands.checks.cooldown(1, 120)
    @app_commands.command(
        name="introduce",
        description="Introduce yourself!"
    )
    async def introduce(self,
                        interaction: discord.Interaction,
                        name: str,
                        age: int) -> None:
        await interaction.response.send_message(
            embed=make_embed(f"My name is {name} and my age is {age}")
        )

    @introduce.error
    async def on_introduce_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Test(bot)
    )
