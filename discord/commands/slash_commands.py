from typing import Literal, cast, Union
from pydantic import Field
from discord.base_classes import SlashCommand
from discord.components.messages import DiscordMessage
from discord.components.misc import DiscordContext
from discord.commands.subcommands import *



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


