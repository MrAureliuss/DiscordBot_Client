from pydantic import BaseModel


class UserToCheckExistData(BaseModel):
    display_name: str
    user_to_exist: str
    channel_owner_id: str
