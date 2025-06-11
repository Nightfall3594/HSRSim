from typing import Optional, Literal, Union

from pydantic import BaseModel

from src.discord.components.discord_member import DiscordMember

class DiscordContext(BaseModel):
    member: Optional[DiscordMember] = None
    interaction_token: Optional[str] = None
    interaction_id: Optional[str] = None
