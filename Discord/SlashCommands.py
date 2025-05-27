import pydantic
import typing
from Discord.Commands import Options, SlashCommand
from Components import BotMessage, DiscordContext


class SlashGreet(SlashCommand):
    name: typing.Literal["greet"]

    def execute(self, context: DiscordContext):
        output = {"type": 4, "data": {"content" : f"Hello, {context.user.username}. Would you like some cake?"}}
        return BotMessage(**output)


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

        output = {"type": 4, "data": {"content": f"With a speed of {speed}, over the course of {cycles} cycles, a character would take {turns} turns"}}
        return BotMessage(**output)