
from typing import cast, Literal, Optional
from discord.components.misc import DiscordContext
from discord.components.messages import DiscordMessage

from pydantic import  BaseModel
from discord.types import *
from discord.components.misc import *


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


class CalculateTurns(SubCommand):

    name: Literal["turns"]

    @property
    def speed(self):
        if self.options:
            for i in self.options:
                if i.name == "speed":
                    return cast(float, i.value)
        else:
            return None

    @property
    def cycles(self):
        if self.options:
            for i in self.options:
                if i.name == "options":
                    return cast(int, i.value)
        else:
            return None

    def execute(self, context: DiscordContext):
        speed = self.speed
        cycles = self.cycles
        turns = ((100 * cycles) + 50) // (10000 / speed)

        return DiscordMessage.generic_message(
            f"With a speed of {speed}, over the course of {cycles} cycles, a character would take {turns} turns")


class CalculateAV(SubCommand):

    name: Literal["av"]

    @property
    def speed(self):
        if self.options:
            for i in self.options:
                if i.name == "speed":
                    return cast(float, i.value)
        else:
            return None

    @property
    def action_advance(self):
        if self.options:
            for i in self.options:
                if i.name == "action_advance":
                    return cast(float, i.value)
        else:
            return None

    def execute(self, context: DiscordContext) -> DiscordMessage:

        speed = self.speed
        action_advance = self.action_advance
        action_gauge = max(10000 * (1 - action_advance), 0)
        action_value = action_gauge/speed

        return DiscordMessage.generic_message(f"An entity with {speed} speed and {action_advance} action advance has an AV of {action_value}")
