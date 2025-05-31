from __future__ import annotations
from pydantic import BaseModel
from typing import Literal, Optional

from discord.components.users import DiscordMember

class DiscordPing(BaseModel):
    type: Literal[1]

class DiscordContext(BaseModel):
    member: Optional[DiscordMember] = None
