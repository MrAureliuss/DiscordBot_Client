import os

import discord
from discord.ext import commands
from config import settings


def load_extensions(bot):
    """
    Функция для загрузки всех cog'ов из директории cogs.
    """
    for cog in os.listdir(".\\cogs\\"):
        if ".py" in str(cog):
            bot.load_extension("cogs." + str(cog).replace(".py", ""))


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['command_prefix'], intents=intents)

