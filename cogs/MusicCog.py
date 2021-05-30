from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.errors import ClientException

from utils.YTDLSource import YTDLSource


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, url):
        """Функция проигрывания музыки в музыкальном канале."""
        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                await ctx.send(f'Now playing: {player.title}')
            except AttributeError:
                await ctx.send("Ошибка! Бот не находится ни в одном голосовом канале.")
            except ClientException:
                await ctx.send("Ошибка! Бот уже воспроизводит музыку.")

    @commands.command()
    async def stop(self, ctx):
        """Функция отключения текущей аудиодорожки."""
        ctx.voice_client.stop()

    @commands.command()
    async def volume(self, ctx, volume):
        """Изменение громкости бота в музыкальном канале."""
        try:
            if ctx.voice_client is None:
                return await ctx.send("Ошибка! Бот не находится ни в одном голосовом канале.")

            ctx.voice_client.source.volume = int(volume) / 100
            await ctx.send(f"Значение громкости изменено на {volume}%")
        except (CommandInvokeError, AttributeError):
            await ctx.send("Ошибка! На данный момент бот не воспроизводит музыку.")
        except ValueError:
            await ctx.send("Ошибка! Громкость звука должна являться целочисленным числом.")

    @commands.command()
    async def pause(self, ctx):
        """Приостановка текущей аудиодорожки."""
        try:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
            else:
                await ctx.send("Ошибка! На данный момент бот не воспроизводит музыку.")
        except AttributeError:
            await ctx.send("Ошибка! Бот не находится ни в одном голосовом канале.")

    @commands.command()
    async def resume(self, ctx):
        """Продолжение приостановленной аудиодорожки."""
        try:
            if ctx.voice_client.is_playing():
                await ctx.send("Ошибка! Бот уже воспроизводит музыку.")
                return

            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
            else:
                await ctx.send("Ошибка! Бот не приостановлен.")
        except AttributeError:
            await ctx.send("Ошибка! Бот не находится ни в одном голосовом канале.")


def setup(bot):
    bot.add_cog(MusicCog(bot))
    print("Musical cog is active.")