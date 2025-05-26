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

class DiscordPing(BaseModel):
    type: typing.Literal[1]


# ----------------------------------------------------------------------

class Options(BaseModel):
    name: str
    type: int
    value: typing.Union[int, float, bool, str, None]


class SlashCommand(BaseModel):
    id: str
    name: str
    type: typing.Literal[1]
    options: typing.Optional[list[Options]] = None


class SlashGreet(SlashCommand):
    name: typing.Literal["greet"]



class SlashCalculateTurns(BaseModel):

    name: typing.Literal["calculate"]
    options: list[Options] = pydantic.Field(min_length=2, max_length=2) # -> receive a json array of exactly 2 in length. This should automatically parse into the appropriate option objects on **kwargs pass, correct?

    @property
    def cycles(self) -> typing.Optional[int]:
        if self.options:
            for i in self.options:
                if i.name == "cycles":
                    return typing.cast(int, i.value)
        else:
            return None


    @property
    def speed(self) -> typing.Optional[float]:
        if self.options:
            for i in self.options:
                if i.name == "speed":
                    return typing.cast(float, i.value)
        else:
            return None



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
    data: typing.Union[SlashGreet, SlashCalculateTurns] = pydantic.Field(discriminator="name")