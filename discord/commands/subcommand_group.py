
from typing import Literal, Optional
from pydantic import  BaseModel
from discord.types import *
from discord.components.misc import DiscordContext
from discord.components.messages import DiscordMessage


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

class SampleSub1(SubCommandGroup):
    type: Literal[2]
    name: Literal["sample"]
