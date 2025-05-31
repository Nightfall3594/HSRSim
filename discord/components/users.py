from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Literal


class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: Optional[str] = None
    discriminator: str
    public_flags: Optional[int] = None

class DiscordMember(BaseModel):
    user: DiscordUser
    roles: list[str]
    premium_since: Optional[str] = None
    permissions: Optional[str] = None
    pending: Optional[bool] = None
    nick: Optional[str] = None
    mute: Optional[bool] = None
    joined_at: str
    deaf: Optional[bool] = None
