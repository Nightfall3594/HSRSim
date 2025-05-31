from pydantic import BaseModel
from typing import Literal, Optional
from discord.components.users import DiscordUser, DiscordMember
from discord.types import SlashCommandType

class DiscordCommand(BaseModel):
    type: Literal[2, 3, 4, 5]
    token: str
    id: str
    application_id: str
    app_permissions: str
    guild_id: Optional[str] = None
    guild_locale: Optional[str] = None
    locale: Optional[str] = None
    member: Optional[DiscordMember] = None
    user: Optional[DiscordUser] = None
    data: SlashCommandType
    channel_id: Optional[str] = None
    version: Optional[int] = None