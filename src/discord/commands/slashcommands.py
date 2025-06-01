import typing
from src.discord.commands.base import SlashCommand
from src.discord.components import DiscordContext
from src.discord.interactions import DiscordMessage

class SlashGreet(SlashCommand):
    name: typing.Literal["greet"]

    def execute(self, context: DiscordContext):
        return DiscordMessage   .generic_message(f"Hello, {context.member.user.username}. Would you like some cake?")



slashcommand_subclasses = SlashCommand.__subclasses__()