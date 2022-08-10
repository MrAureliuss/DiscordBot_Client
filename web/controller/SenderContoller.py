import discord

from sqlalchemy import select
from discord.errors import Forbidden, HTTPException
from fastapi import HTTPException as fastapi_Error

from db.models.Channels import channel
from web.models import Speech


class SenderController:
    def __init__(self, session, bot):
        self.session = session
        self.bot = bot

    async def message_send(self, speech: Speech):
        stmt = select(channel).where(
            channel.c.display_name == str(speech.display_name),
            channel.c.owner_id == str(speech.channel_owner_id)
        )

        row_count = self.session.execute(stmt).rowcount

        if row_count == 1:
            work_channel = self.session.execute(stmt).fetchone()
            if work_channel[1]:  # Если канал активен.
                try:
                    guild = self.bot.get_guild(int(work_channel[2]))  # Находим канал по его ID.
                    embed = discord.Embed(title=":loudspeaker:  Объявление от администратора :loudspeaker: ",
                                          description=str(speech.speech_text),
                                          color=0xff0000)

                    await guild.text_channels[0].send(embed=embed)

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