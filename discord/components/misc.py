from __future__ import annotations
from pydantic import BaseModel
from typing import Literal, Optional, Union

from discord.components.users import DiscordMember

class DiscordPing(BaseModel):
    type: Literal[1]

class DiscordContext(BaseModel):
    member: Optional[DiscordMember] = None

class Options(BaseModel):
    """
    Options object.
    Contains the direct arguments for the commands themselves.
    Refer to official discord docs for typings based on number codes.
    Bear in mind this object is very polymorphic, and values and typings are on a case-by-case basis.
    """
    name: str
    type: Literal[3,4,5,10]
    value: Union[int, str, bool, float]