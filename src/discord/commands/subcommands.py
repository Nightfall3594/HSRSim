import typing
from typing import *

import typing_extensions
from pydantic import BaseModel, Field

from src.discord.commands import Options
from src.discord.components import DiscordContext
from src.discord.interactions.discord_message import DiscordMessage

T = typing.TypeVar('T')

class SubCommand(BaseModel):
    name: str
    type: Literal[1]

    options: Optional[list[Options]] = None

    def _get(self, attribute: str, dtype: Type[T]) -> Optional[T]:
        if self.options:
            for i in self.options:
                if i.name == attribute:
                    return cast(dtype, i.value)

        return None


class CalculateTurns(SubCommand):
    name: Literal["turns"]

    @property
    def speed(self):
        return self._get("speed", float)


    @property
    def cycles(self):
        return self._get("cycles", int)


    def execute(self, context: DiscordContext):

        speed = self.speed
        cycles = self.cycles

        turns = ((100*cycles + 50)/ (10000/speed))
        return DiscordMessage.generic_message(f"With a speed of {speed}, over the course of {cycles} cycle(s), a character would take {turns} turns")



class CalculateAV(SubCommand):

    name: Literal["av"]






subcommand_subclasses = Annotated[Union[*SubCommand.__subclasses__()], Field(discriminator="name")]