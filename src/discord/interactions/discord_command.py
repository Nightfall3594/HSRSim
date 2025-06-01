from pydantic import BaseModel, Field
import typing


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
    data: typing.Union[SlashCommand.subclasses()] = Field(discriminator="name")  # all top level commands are of type 1
    channel_id: typing.Optional[str] = None
    version: typing.Optional[int] = None