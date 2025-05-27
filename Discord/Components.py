from pydantic import BaseModel
import pydantic
import typing


class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: typing.Optional[str] = None
    discriminator: str
    public_flags: typing.Optional[int] = None

class DiscordMember(BaseModel):
    user: DiscordUser
    roles: list[str]
    premium_since: typing.Optional[str] = None
    permissions: str
    pending: typing.Optional[bool] = None
    nick: typing.Optional[str] = None
    mute: typing.Optional[bool] = None
    joined_at: str
    deaf: typing.Optional[bool] = None


class DiscordMessageContent(BaseModel):
    content: str

class BotMessage(BaseModel):
    type: typing.Literal[1, 4, 5, 6, 7, 8, 9]
    data: typing.Optional[DiscordMessageContent] = None

    # def __init__(self, message: str):
    #     return {"type": 4, "data": {"content" : message}}


class DiscordPing(BaseModel):
    type: typing.Literal[1]


"""
class DiscordCommand(BaseModel):
    type: typing.Literal[2, 3, 4, 5]
    token: str
    id: str
    application_id: str
    app_permissions: str
    guild_id: typing.Optional[str] = None
    guild_locale: typing.Optional[str] = None
    locale: typing.Optional[str] = None
    member: typing.Optional[DiscordMember] = None
    user: typing.Optional[DiscordUser] = None
    data: typing.Union[*SlashCommand.__subclasses__()] = pydantic.Field(discriminator="name")
"""

class DiscordContext(BaseModel):
    user: typing.Optional[DiscordUser] = None
    member: typing.Optional[DiscordMember] = None




