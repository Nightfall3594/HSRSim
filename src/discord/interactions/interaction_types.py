from typing import Optional, Union, Annotated, Literal, Any

from pydantic import BaseModel, Field

from src.discord.components import DiscordMember, DiscordUser
from src.discord.commands.slashcommands import slashcommand_subclasses
from src.discord.component_commands.string_select_command import string_select_subclasses


class BaseInteraction(BaseModel):
    type: int
    token: str
    id: str
    application_id: str
    app_permissions: str
    guild_id: Optional[str] = None
    guild_locale: Optional[str] = None
    locale: Optional[str] = None
    member: Optional[DiscordMember] = None
    user: Optional[DiscordUser] = None
    data: Union[Any]
    channel_id: Optional[str] = None
    version: Optional[int] = None


class SlashInteraction(BaseInteraction):
    type: Literal[2]
    data: slashcommand_subclasses


class ComponentInteraction(BaseInteraction):
    type: Literal[3]
    # it could be any component interaction. Discriminate via component_type
    data: Annotated[Union[string_select_subclasses], Field(discriminator="component_type")]



DiscordInteraction = Annotated[Union[SlashInteraction, ComponentInteraction], Field(discriminator="type")]