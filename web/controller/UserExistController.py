import discord

from sqlalchemy import select
from discord.errors import Forbidden, HTTPException
from fastapi import HTTPException as fastapi_Error

from db.models.Channels import channel
from web.models import UserToCheckExistData


class UserExistController:
    def __init__(self, session, bot):
        self.session = session
        self.bot = bot

    async def check_user_exist(self, user_to_check_exist: UserToCheckExistData):
        stmt = select(channel).where(
            channel.c.display_name == str(user_to_check_exist.display_name),
            channel.c.owner_id == str(user_to_check_exist.channel_owner_id)
        )

        row_count = self.session.execute(stmt).rowcount

        if row_count == 1:
            work_channel = self.session.execute(stmt).fetchone()
            if work_channel[1]:  # Если канал активен.
                try:
                    guild = self.bot.get_guild(int(work_channel[2]))  # Находим канал по его ID.
                    split_name = user_to_check_exist.user_to_exist.split("#")

                    if len(split_name) < 2:  # Если пользователь забыл отправить имя или дискриминатор - выбрасываем ошибку.
                        raise AttributeError

                    user = discord.utils.get(guild.members, name=f"{split_name[0]}", discriminator=f"{split_name[-1]}")
                    if user is None:  # Если пользователь не найден - выкидываем ошибку.
                        raise AttributeError

                    return user.id

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
