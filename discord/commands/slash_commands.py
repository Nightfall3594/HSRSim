from typing import Literal, cast
from discord.base_classes import SlashCommand
from discord.components.messages import DiscordMessage
from discord.components.misc import DiscordContext


class Greet(SlashCommand):

    name: Literal["greet"]

    def execute(self, context: DiscordContext) -> DiscordMessage:
        return DiscordMessage.generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")


class Calculate(SlashCommand):

    name: Literal["calculate"]

    def execute(self, context: DiscordContext) -> DiscordMessage:
        return self.sub_command.execute()


