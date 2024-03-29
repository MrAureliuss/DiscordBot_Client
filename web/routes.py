from fastapi import APIRouter
from bot_init import bot
from web.models.Speech import Speech
from web.models.UserToCheckExistData import UserToCheckExistData
from web.controller.SynthesisController import SpeechController
from web.controller.SenderContoller import SenderController
from web.controller.UserExistController import UserExistController
from db.SessionHolder import SessionHolder
from db.CreateDBEngine import engine, create_all
from fastapi import HTTPException as fastapi_Error

router = APIRouter()
create_all(engine)
session_holder = SessionHolder(engine=engine)
speech_controller = SpeechController(session=session_holder.session, bot=bot)
sender_controller = SenderController(session=session_holder.session, bot=bot)
user_exist_controller = UserExistController(session=session_holder.session, bot=bot)


@router.post("/speech_synthesis")
async def speech_synthesis(speech: Speech):
    try:
        await speech_controller.synthesis(speech)
        return {"success_message": "Текст успешно синтезирован!"}
    except fastapi_Error as ex:
        raise fastapi_Error(status_code=ex.status_code, detail=ex.detail)
    except AttributeError:
        raise fastapi_Error(status_code=400, detail="Ошибка! Бот не находится в голосовом канале!")


@router.post("/send_speech")
async def send_speech(speech: Speech):
    try:
        await sender_controller.message_send(speech)
        return {"success_message": "Текст успешно отправлен!"}
    except fastapi_Error as ex:
        raise fastapi_Error(status_code=ex.status_code, detail=ex.detail)
    except AttributeError:
        raise fastapi_Error(status_code=400, detail="Ошибка! Текстовый канал не найден!")


@router.post("/get_user_id")
async def get_user_id(user_check_exist: UserToCheckExistData):
    try:
        user_id = await user_exist_controller.check_user_exist(user_check_exist)
        return {"required_user_id": user_id}
    except fastapi_Error as ex:
        raise fastapi_Error(status_code=ex.status_code, detail=ex.detail)
    except AttributeError:
        raise fastapi_Error(status_code=400, detail="Ошибка! Пользователь не найден!")
