import typing
from typing import *

from pydantic import BaseModel, Field
from enka import HSRClient
from enka.errors import *
import os

from pyexpat.errors import messages

from src.discord.commands import Options
from src.discord.components import DiscordContext
from src.discord.components.message_components import StringSelectOption
from src.discord.interactions.component_message import BuildMessage
from src.discord.interactions.interaction_responses import CallBackResponse, FollowUpResponse
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

        turns = ((100*cycles + 50) // (10000/speed))
        return CallBackResponse.generic_message(f"With a speed of {speed}, over the course of {cycles} cycle(s), a character would take {turns} turns",
                                                context.interaction_id,
                                                context.interaction_token)


class CalculateAV(SubCommand):

    name: Literal["av"]

    @property
    def speed(self):
        return self._get("speed", float)

    @property
    def action_advance(self):
        return self._get("action_advance", float)

    def execute(self, context: DiscordContext):

        action_gauge = (10000 * (1-self.action_advance))
        action_value = (action_gauge/self.speed)

        return CallBackResponse.generic_message(f"A character with a speed of {self.speed} and a {self.action_advance * 100}% action advance has an AV of {action_value}",
                                                context.interaction_id,
                                                context.interaction_token)


class ShowBuild(SubCommand):
    name: Literal["builds"]

    async def execute(self, ctx: DiscordContext):

        CallBackResponse.deferred_message(ctx.interaction_id, ctx.interaction_token)

        async with HSRClient() as client:
            try:
                response = await client.fetch_showcase(self.options[0].value)
            except RateLimitedError:
                error_message = DiscordMessage.generic("Looks like you're hitting rate limits. How about you try again a few minutes from now?")
            except GameMaintenanceError:
                error_message = DiscordMessage.generic("Looks like the game is still on maintenance. Try again later on")
            except WrongUIDFormatError:
                error_message = DiscordMessage.generic("Invalid UID format, please use a valid one")
            except PlayerDoesNotExistError:
                error_message = DiscordMessage.generic("This player does not exist")
            except EnkaAPIError:
                error_message = DiscordMessage.generic("There is an error with enka.network")
            except EnkaPyError:
                error_message = DiscordMessage.generic("There is an error with the server.")

        if error_message:
            FollowUpResponse.send_followup(error_message, ctx.interaction_token)

        if not response.characters:
            return CallBackResponse.generic_message("No characters found. Are you sure they are public?",
                                                    ctx.interaction_id,
                                                    ctx.interaction_token)

        char_list = []
        for character in response.characters:
            char_list.append(
                StringSelectOption(label=character.name, value=f"{self.options[0].value};{character.name}"))

        print("DEBUG-------------------------------------", flush=True)
        print("Endpoint: ", flush=True)
        print(f"https://discord.com/api/v10/webhooks/{os.environ.get('APPLICATION_ID')}/{ctx.interaction_token}", flush=True)
        print("\n\n\n", flush=True)
        print("Testcase payload", flush=True)
        print(BuildMessage.string_select(options=char_list, custom_id="character_select").model_dump(), flush=True)

        FollowUpResponse.send_followup(BuildMessage.string_select(options=char_list, custom_id="character_select"),
                                       ctx.interaction_token)

        return None







subcommand_subclasses = Annotated[Union[*SubCommand.__subclasses__()], Field(discriminator="name")]