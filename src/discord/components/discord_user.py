from pydantic import BaseModel
import typing

class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: typing.Optional[str] = None
    discriminator: str
    public_flags: typing.Optional[int] = None
    bot: typing.Optional[bool] = False