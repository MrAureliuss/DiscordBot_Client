import os
from discord.ext import commands
from config import settings


def load_extensions(bot):
    """
    Функция для загрузки всех cog'ов из директории cogs.
    """
    for cog in os.listdir(".\\cogs\\"):
        if ".py" in str(cog):
            bot.load_extension("cogs." + str(cog).replace(".py", ""))


if __name__ == '__main__':
    bot = commands.Bot(command_prefix=settings['command_prefix'])
    load_extensions(bot)

    bot.run(settings['token'])
