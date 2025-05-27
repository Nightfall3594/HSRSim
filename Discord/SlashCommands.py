import pydantic
import typing
from Discord.Commands import Options
from Discord.Components import *


class SlashCommand(BaseModel):
    id: str
    name: str
    type: typing.Literal[1]
    options: typing.Optional[list[Options]] = None


class SlashGreet(SlashCommand):
    name: typing.Literal["greet"]

    def execute(self, context: DiscordContext):
        return BotMessage.generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")


class SlashCalculateTurns(SlashCommand):
    name: typing.Literal["calculate"]
    options: list[Options] = pydantic.Field(min_length=2, max_length=2)  # -> receive a json array of exactly 2 in length. This should automatically parse into the appropriate option objects on **kwargs pass, correct?

    @property
    def cycles(self) -> typing.Optional[int]:
        if self.options:
            for i in self.options:
                if i.name == "cycles":
                    return typing.cast(int, i.value)
        else:
            return None


    @property
    def speed(self) -> typing.Optional[float]:
        if self.options:
            for i in self.options:
                if i.name == "speed":
                    return typing.cast(float, i.value)
        else:
            return None


    def execute(self, context: DiscordContext):

        speed = self.speed
        cycles = self.cycles
        turns = ((100 * cycles) + 50) // (10000/speed)

        return BotMessage.generic_message(f"With a speed of {speed}, over the course of {cycles} cycles, a character would take {turns} turns")