import discord
from discord.ext import commands


class ControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Функция для призыва бота в звуковой канал.
        :AttributeError возникает при вызове бота будучи не в голосовом канале.
        """
        try:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        except AttributeError:
            await ctx.send("Ошибка! Вы должны нахдоится в голосовом канале.")

    @commands.command()
    async def leave(self, ctx):
        """Функция для исключения бота из звукового канала.
        :AttributeError возникает при попытке исключения бота, который заведомо не находится в голосовом канале.
        """
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            await ctx.send("Ошибка! Бот не находится ни в одном голосовом канале.")


def setup(bot):
    bot.add_cog(ControlCog(bot))
    print("Control cog is active.")
