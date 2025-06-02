from pydantic import BaseModel, Field
import typing

from src.discord.components import DiscordMember, DiscordUser
from src.discord.commands.slashcommands import slashcommand_subclasses


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
    data: slashcommand_subclasses = Field(discriminator="name")  # always must be slash command
    channel_id: typing.Optional[str] = None
    version: typing.Optional[int] = None