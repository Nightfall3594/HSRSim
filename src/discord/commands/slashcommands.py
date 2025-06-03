from typing import *

from pydantic import BaseModel, Field

from src.discord.components import DiscordContext
from src.discord.interactions.discord_message import DiscordMessage
from src.discord.commands import Options
from src.discord.commands.subcommands import *
from src.discord.commands.subcommand_groups import *

T = TypeVar('T')

class SlashCommand(BaseModel):
    id: str
    name: str
    type: Literal[1]

    # WIP: This MUST contain either: an options, a subcommand, or group.
    options: Optional[list[
        Annotated[
            Union[
                Options,
                subcommand_subclasses,
                subcommand_group_subclasses
            ],
            Field(discriminator="type")
        ]
    ]] = None


    # This is a getter for if a command contains a subcommand.
    # Bear in mind, although it's an array, there's almost always only 1 subcommand choice or several options
    @property
    def subcommand(self):
        return self.options[0] if self.options else None


    # This is a getter for options, makes it easier to get options by
    # simply wrapping the getter with this method.
    def _get(self, attribute: str, dtype: Type[T]) -> Optional[T]:
        if self.options:
            for i in self.options:
                if i.name == attribute:
                    return cast(dtype, attribute)
        return None


class Greet(SlashCommand):
    name: Literal["greet"]

    def execute(self, context: DiscordContext):
        return DiscordMessage.generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")


class Calculate(SlashCommand):
    name: Literal["calculate"]
    options: list[Union[CalculateTurns, CalculateAV]]

    def execute(self, context: DiscordContext):
        return self.subcommand.execute(context)


slashcommand_subclasses = Annotated[Union[*SlashCommand.__subclasses__()], Field(discriminator="name")]