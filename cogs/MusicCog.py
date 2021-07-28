import asyncio
import random
import discord
import utils.MusicTrack as Track
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.errors import ClientException
from utils.YTDLSource import YTDLSource


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    @commands.command()
    async def play(self, ctx, *, url):
        """Функция проигрывания музыки в музыкальном канале."""
        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                embed = discord.Embed()

                music_track = Track.MusicTrack(player, ctx)
                if not ctx.voice_client.is_playing():
                    embed = discord.Embed(title=":musical_note:  Ваши уши греет песня :musical_note: ",
                                          description=str(player.title),
                                          color=0xFF00FF)
                    embed.add_field(name="Заказал пластинку", value=str(ctx.message.author))
                    ctx.voice_client.play(player, after=lambda check_queue: self.get_next_song(ctx.guild.id))
                else:
                    self.add_music_to_queue(ctx.guild.id, music_track)
                    embed = discord.Embed(title="На данный момент бот уже проигрывает музыку.\n"
                                                "Выбранная аудиодорожка поставлена в очередь Вашего канала.",
                                          description=str(player.title),
                                          color=0xFF00FF)

                await ctx.send(embed=embed)
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

    @commands.command()
    async def queue(self, ctx):
        """Показ очереди песен в канале."""
        if (self.queue.get(ctx.guild.id) is not None) and len(self.queue.get(ctx.guild.id)) > 0:
            songs_queue = self.queue.get(ctx.guild.id)  # Берем очередь песен для нужного канала.
            description = ""

            for song in songs_queue:
                description += f"{song.get_music_player().title}. Трек заказал: {song.get_ctx().message.author}\n\n"

            embed = discord.Embed(title="Список очереди песен Вашего канала.",
                                  description=description,
                                  color=0xFF00FF)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Очередь песен Вашего канала пуста.")

    @commands.command()
    async def shuffle(self, ctx):
        """Перемешивание песен в очереди."""
        if (self.queue.get(ctx.guild.id) is not None) and len(self.queue.get(ctx.guild.id)) > 0:
            random.shuffle(self.queue.get(ctx.guild.id))

            await ctx.send("Очередь песен перемешана.")
        else:
            await ctx.send("Очередь песен Вашего канала пуста.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Если человек забыл ввести URL или название аудиодорожки - уведомляем об этом."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Ошибка! Вы забыли ввести URL или название аудиодорожки.")

    def add_music_to_queue(self, guild_id, music_track):
        """Добавление песни в очередь.
        Если уже какие-то треки заказывались в канале(есть ключ в self.queue), то добавляем к существующим значениям новый трек,
        иначе создаем новый key."""
        if guild_id in self.queue:  # Добавление к существующему ключу новое значение трека.
            self.queue[guild_id] += [music_track]
        else:  # Создание нового ключа с значением.
            self.queue[guild_id] = [music_track]

    def get_next_song(self, guild_id):
        """Воспроизведение песен из очереди.
        Если в канале (guild.id) есть треки которые еще не играли - воспроизводим их."""
        song_values = self.queue.get(guild_id)  # Берем очередь песен для нужного канала.
        if len(song_values) > 0:    # Если в очереди есть песни.
            music_track = song_values[0]    # Берем первую из очереди песню в канале.
            del song_values[0]  # Удаляем из очереди трек который будет воспроизводить.

            player = music_track.get_music_player()
            ctx = music_track.get_ctx()

            ctx.voice_client.play(player, after=lambda check_queue: self.get_next_song(ctx.guild.id))

            embed = discord.Embed(title=":musical_note:  Встречайте песню из очереди :musical_note: ",
                                  description=str(player.title),
                                  color=0xFF00FF)
            embed.add_field(name="Заказал пластинку", value=str(ctx.message.author))

            send = ctx.send(embed=embed)    # Корутина для отправки без await.
            future = asyncio.run_coroutine_threadsafe(send, self.bot.loop)  # Выполняем операцию потокобезопасно.
            try:
                future.result()
            except:
                print("Queue exception.")


def setup(bot):
    bot.add_cog(MusicCog(bot))
    print("Musical cog is active.")
