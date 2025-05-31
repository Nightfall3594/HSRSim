from __future__ import annotations

import typing
from typing import Union, Optional, Literal
from discord.types import *
from pydantic import BaseModel, Field
from discord.components.misc import DiscordContext
from discord.components.messages import DiscordMessage


class SlashCommand(BaseModel):
    """
    Top-level command.
    This can map to either a subgroup, a sub-command, or directly contain an options object
    """
    id: int
    name: str
    type: Literal[1]
    options: Optional[list[CompositeOptionType]]

    @property
    def sub_command(self) -> SubCommandType:
        # bear in mind that in a real payload, there is only one command choice.
        # this should only be accessed if you're certain the option type is strictly a subcommand.
        return self.options[0] if self.options and isinstance(self.options[0], SubCommandType) else None

    def execute(self, context: DiscordContext) -> DiscordMessage:
        raise NotImplementedError


class SubCommand(BaseModel):
    """
    Subcommand.
    It must only directly map to options objects.
    """
    name: str
    type: Literal[1]
    options: Optional[list[Options]]
    choices: Optional[list[Options]]

    def execute(self, context: DiscordContext) -> DiscordMessage:
        raise NotImplementedError


class SubCommandGroup(BaseModel):
    """
    This is for the "command folders".
    This must directly map to strictly only other folders, or subcommands.
    """
    name: str
    type: Literal[2]
    options: Optional[list[SubCommandGroupOption]]

    @property
    def sub_command(self):  # bear in mind that in a real payload, there is only one command choice.
        return self.options[0] if self.options else None

    # since this is a folder, it should execute the specific command under it (delegation pattern)
    def execute(self, context: DiscordContext) -> DiscordMessage:
        raise NotImplementedError


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