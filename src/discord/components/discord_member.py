import typing

from pydantic import BaseModel

from src.discord.components.discord_user import DiscordUser

class DiscordMember(BaseModel):
    user: DiscordUser
    roles: list[str]
    premium_since: typing.Optional[str] = None
    permissions: typing.Optional[str] = None
    pending: typing.Optional[bool] = None
    nick: typing.Optional[str] = None
    mute: typing.Optional[bool] = None
    joined_at: str
    deaf: typing.Optional[bool] = None