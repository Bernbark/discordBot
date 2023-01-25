# bot.py
import asyncio
import os
import random
import aiohttp
import discord
import motor.motor_asyncio

from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MongoURI = os.getenv('URI')


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id=1062320142719127653,
            case_insensitive=True
        )
        self.initial_extensions = [
            "cogs.test",
            "cogs.economy",
            "cogs.funActions",
            "cogs.games",
            "cogs.whatToWatch",
            "cogs.artsy",
            "cogs.exploration",
            "cogs.shop",
            "cogs.inventory"
        ]

    # Loading cogs
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync()

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

bot = MyBot()

# General user case error handling for events with cooldowns
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('This command is on a %.2fs cooldown' % error.retry_after)
    raise error  # re-raise the error so all the errors will still show up in console

@bot.command(
        name="yo"
    )
async def yo(ctx, arg):
    await ctx.send(arg)




bot.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(MongoURI)
bot.run(TOKEN)

