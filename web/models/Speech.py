from pydantic import BaseModel


class Speech(BaseModel):
    display_name: int
    speech_text: str
    user_id: int
    