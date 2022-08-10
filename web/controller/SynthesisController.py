import os
import asyncio
import discord

from os.path import exists
from sqlalchemy import select
from discord.errors import Forbidden, HTTPException
from fastapi import HTTPException as fastapi_Error

from db.models.Channels import channel
from web.models import Speech
from web.utils.TextToSpeech import gen_speech
from utils.QueueHolder import queue_holder


class SpeechController:
    def __init__(self, session, bot):
        self.session = session
        self.bot = bot
        self.queue = queue_holder().queue

    async def synthesis(self, speech: Speech):
        stmt = select(channel).where(
            channel.c.display_name == str(speech.display_name),
            channel.c.owner_id == str(speech.channel_owner_id)
        )

        row_count = self.session.execute(stmt).rowcount

        if row_count == 1:
            work_channel = self.session.execute(stmt).fetchone()
            if work_channel[1]:  # Если канал активен.
                try:
                    guild = await self.bot.fetch_guild(work_channel[2])  # Находим канал по его ID.
                    sound_file_path = f'{os.getcwd()}/web/utils/synthesized/{gen_speech(speech.speech_text)}'  # Генерируем файл с аудио по заданному тексту.

                    if guild.voice_client.is_playing():  # Если что-то уже играет ставим на паузу.
                        guild.voice_client.pause()

                    guild.voice_client.play(discord.FFmpegPCMAudio(
                        executable=f"{os.getcwd()}/utils/ffmpeg/ffmpeg.exe",
                        source=sound_file_path),
                        after=lambda e: self.get_next_song(int(speech.display_name), guild, sound_file_path)
                    )  # Генерируем и проигрываем наш сгенерированный войс-файл.

                except (Forbidden, HTTPException):
                    raise fastapi_Error(status_code=403, detail="Ошибка! Данный канал вам не принадлежит!")
                except AttributeError:
                    raise AttributeError
            else:
                raise fastapi_Error(status_code=400, detail="Ошибка! Бот не привязан к серверу через сайт!")
        elif row_count == 0:
            raise fastapi_Error(status_code=400, detail="Ошибка! Канал или пользователь не найден!")
        else:
            raise fastapi_Error(status_code=400, detail="Ошибка! Операция не может быть завершена!")

    def get_next_song(self, guild_id, guild, remove_file_path):
        self.remove_file(remove_file_path)  # Удаляем сгенерированный файл из директории.
        song_values = self.queue.get(guild_id)  # Берем очередь песен для нужного канала.
        if song_values is not None and len(song_values) > 0:    # Если в очереди есть песни.
            music_track = song_values[0]    # Берем первую из очереди песню в канале.
            del song_values[0]  # Удаляем из очереди трек который будем воспроизводить.

            player = music_track.get_music_player()
            ctx = music_track.get_ctx()

            guild.voice_client.play(player, after=lambda check_queue: self.get_next_song(int(guild_id), guild))

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

    def remove_file(self, remove_file_path):
        if exists(remove_file_path):
            os.remove(remove_file_path)
