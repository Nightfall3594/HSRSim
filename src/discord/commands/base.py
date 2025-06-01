from __future__ import annotations
from typing import Optional, Union, Literal

from pydantic import BaseModel

from src.discord.commands.options import Options
from

class SlashCommand(BaseModel):
    id: str
    name: str
    type: Literal[1]

    # WIP: This MUST contain either: an options, a subcommand, or group.
    options: Optional[list[]] = None


class SubCommand(BaseModel):
    name: str
    type: Literal[1]

    # WIP: This must contain either options object or nothing.
    options: Optional[list[Options]] = None



class SlashCommandGroup(BaseModel):
    id: str
    name: str
    type: Literal[2]

    # WIP: This must contain either slash command groups OR slash commands.
    options: list[]