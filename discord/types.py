from __future__ import annotations
from typing import Annotated, Union
from pydantic import Field


from discord.commands.slash_commands import SlashCommand
from discord.commands.subcommands import SubCommand
from discord.commands.subcommand_group import SubCommandGroup
from discord.components.misc import Options


SlashCommandType = Annotated[Union[*SlashCommand.__subclasses__()], Field(discriminator="name")]

SubCommandType = Annotated[Union[*SubCommand.__subclasses__()], Field(discriminator="name")]

SubCommandGroupType = Annotated[Union[*SubCommandGroup.__subclasses__()], Field(discriminator="name")]

CompositeOptionType = Annotated[Union[Options, SubCommandType, SubCommandGroupType], Field(discriminator="type")]

SubCommandGroupOption = Annotated[Union[SubCommandType, SubCommandGroupType], Field(discriminator="type")] #  if SubCommand.__subclasses__() and SubCommandGroup.__subclasses__() else None
