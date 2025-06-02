from __future__ import annotations
from typing import Literal, Annotated, Union

from pydantic import BaseModel, Field

from src.discord.commands.subcommands import subcommand_subclasses


class SubCommandGroup(BaseModel):
    id: str
    name: str
    type: Literal[2]

    # WIP: This must contain either sub command groups OR sub commands.
    # UNTESTED BEHAVIOR. Check later if it is deferred properly
    options: list[Union[subcommand_subclasses, subcommand_group_subclasses]]


class SampleSubGroup(SubCommandGroup):
    name: Literal["SampleSubCommand"]


subcommand_group_subclasses = Annotated[Union[SubCommandGroup.__subclasses__()], Field(discriminator="name")]


