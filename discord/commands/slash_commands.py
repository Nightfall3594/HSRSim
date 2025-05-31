from typing import Literal, cast, Union, Optional
from pydantic import Field, BaseModel
from discord.components.messages import DiscordMessage
from discord.components.misc import DiscordContext
from discord.commands.subcommands import *

from discord.types import *


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


class Greet(SlashCommand):

    name: Literal["greet"]

    def execute(self, context: DiscordContext) -> DiscordMessage:
        return DiscordMessage.generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")


class Calculate(SlashCommand):
    """
    Calculate something.
    Currently maps to either AV or Turns.
    """
    name: Literal["calculate"]
    options: list[Union[CalculateTurns, CalculateAV]] = Field(discriminator="name")

    def execute(self, context: DiscordContext) -> DiscordMessage:
        return self.sub_command.execute()


