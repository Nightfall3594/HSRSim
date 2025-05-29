from __future__ import annotations
from typing import Annotated, Union
import pydantic
import typing
from Discord.Commands import Options
from Discord.Components import *


class SlashCommand(BaseModel):
    id: str
    name: str
    type: typing.Literal[1]
    options: typing.Optional[list[Annotated[Union[Options, SlashCommandGroup.subclasses(), SlashCommand.subclasses()], pydantic.Field(discriminator="type")]]] = None  # if there are options, they could either be other slash commands, or groups, or options objects
    choices: typing.Optional[list[Options]] = None

    @classmethod
    def subclasses(cls):
        return typing.Annotated[typing.Union[*cls.__subclasses__()], pydantic.Field(discriminator="name")]


class SlashCommandGroup(BaseModel):
    id: str
    name: str
    type: typing.Literal[2]
    options: list[SlashCommand.subclasses()]  # it could be any slash command!

    @classmethod
    def subclasses(cls):
        if not cls.__subclasses__():
            return
        else:
            return typing.Annotated[typing.Union[*cls.__subclasses__()], pydantic.Field(discriminator="name")]



class Greet(SlashCommand):
    name: typing.Literal["greet"]
    type: typing.Literal[1]

    def execute(self, context: DiscordContext):
        return BotMessage.generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")


class CalculateTurns(SlashCommand):
    name: typing.Literal["turns"]
    type: typing.Literal[1]
    options: list[typing.Union[Options]]

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



class SlashCalculate(SlashCommand):
    name: typing.Literal["calculate"]

    @property
    def subcommand(self) -> typing.Optional[SlashCommand.subclasses()]:
        if self.options:
            return self.options[0]
        else:
            return None

    def execute(self, context: DiscordContext):
        return self.subcommand.execute(context)