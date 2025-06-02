from typing import Literal, Optional, Annotated, Union

from pydantic import BaseModel, Field

from src.discord.components import DiscordContext
from src.discord.interactions import DiscordMessage
from src.discord.commands import Options
from src.discord.commands.subcommands import subcommand_subclasses
from src.discord.commands.subcommand_groups import subcommand_group_subclasses

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


class SlashGreet(SlashCommand):
    name: Literal["greet"]

    def execute(self, context: DiscordContext):
        return DiscordMessage.generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")



slashcommand_subclasses = Annotated[Union[SlashCommand.__subclasses__()], Field(discriminator="name")]