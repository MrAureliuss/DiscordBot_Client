from pydantic import BaseModel


class Speech(BaseModel):
    display_name: int
    speech_text: str
    channel_owner_id: int
    