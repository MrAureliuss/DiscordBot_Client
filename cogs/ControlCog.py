from discord.ext import commands
from discord.ext.commands import CheckFailure

from db.BlacklistUserChecker import user_not_in_blacklist


class ControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(user_not_in_blacklist)
    async def join(self, ctx):
        """Функция для призыва бота в звуковой канал.
        :AttributeError возникает при вызове бота будучи не в голосовом канале.
        """
        try:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        except AttributeError:
            await ctx.send("Ошибка! Вы должны находиться в голосовом канале.")

    @commands.command()
    @commands.check(user_not_in_blacklist)
    async def leave(self, ctx):
        """Функция для исключения бота из звукового канала.
        :AttributeError возникает при попытке исключения бота, который заведомо не находится в голосовом канале.
        """
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            await ctx.send("Ошибка! Бот не находится ни в одном голосовом канале.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Если человек пользователь находится в черном списке канале - то уведомляем его об этом."""
        if isinstance(error, CheckFailure):
            await ctx.send("Ошибка! Вы не можете вызвать команду, так как находитесь в черном списке канала!")


def setup(bot):
    bot.add_cog(ControlCog(bot))
    print("Control cog is active.")
