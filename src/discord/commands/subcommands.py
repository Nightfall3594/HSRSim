from typing import Literal, Optional, Union, Annotated, cast

from pydantic import BaseModel, Field

from src.discord.commands import Options
from src.discord.components import DiscordContext
from src.discord.interactions.discord_message import DiscordMessage

class SubCommand(BaseModel):
    name: str
    type: Literal[1]

    # WIP: This must contain either options object or nothing.
    options: Optional[list[Options]] = None


class CalculateTurns(SubCommand):
    name: Literal["turns"]

    @property
    def speed(self):
        if self.options:
            for i in self.options:
                if i.name == "speed":
                    return cast(float, i.value)


    @property
    def cycles(self):
        if self.options:
            for i in self.options:
                if i.name == "cycles":
                    return cast(int, i.value)


    def execute(self, context: DiscordContext):

        speed = self.speed
        cycles = self.cycles

        turns = ((100*cycles + 50)/ (10000/speed))
        return DiscordMessage.generic_message(f"With a speed of {speed}, over the course of {cycles} cycle(s), a character would take {turns} turns")



class CalculateAV(SubCommand):

    name: Literal["av"]






subcommand_subclasses = Annotated[Union[*SubCommand.__subclasses__()], Field(discriminator="name")]