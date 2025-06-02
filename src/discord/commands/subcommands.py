from typing import Literal, Optional, Union, Annotated

from pydantic import BaseModel, Field

from src.discord.commands import Options

class SubCommand(BaseModel):
    name: str
    type: Literal[1]

    # WIP: This must contain either options object or nothing.
    options: Optional[list[Options]] = None


class TestSub(SubCommand):
    name: Literal["sampleSubCommand"]


subcommand_subclasses = Annotated[Union[SubCommand.__subclasses__()], Field(discriminator="name")]