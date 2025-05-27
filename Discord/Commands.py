from pydantic import BaseModel
import typing
import pydantic
from Components import *
from SlashCommands import *


class Options(BaseModel):
    name: str
    type: int  # this is the dtype of the input. Refer to docs below.
    value: typing.Union[int, float, bool, str, None]

    """
    Represents the type of the slash command option.
    These values correspond to Discord's Application Command Option Type field.

    Attributes:
        type (int): The integer representation of the option type.
                    Refer to the official Discord API documentation for the most
                    up-to-date list.

    Discord Application Command Option Types:
    - 1: SUB_COMMAND (Represents a subcommand)
    - 2: SUB_COMMAND_GROUP (Represents a group of subcommands)
    - 3: STRING (A plain string value)
    - 4: INTEGER (An integer value. Discord may enforce a range -2^53 and 2^53)
    - 5: BOOLEAN (A boolean value: true or false)
    - 6: USER (A user snowflake ID)
    - 7: CHANNEL (A channel snowflake ID; accepts all channel types)
    - 8: ROLE (A role snowflake ID)
    - 9: MENTIONABLE (A user or role snowflake ID)
    - 10: NUMBER (A floating-point number value. Discord 
    """


class SlashCommand(BaseModel):
    id: str
    name: typing.Literal["BaseSlashCommand"]
    type: typing.Literal[1]
    options: typing.Optional[list[Options]] = None


class DiscordCommand(BaseModel):
    type: typing.Literal[2, 3, 4, 5]
    token: str
    id: str
    application_id: str
    app_permissions: str
    guild_id: typing.Optional[str] = None
    guild_locale: typing.Optional[str] = None
    locale: typing.Optional[str] = None
    member: typing.Optional[DiscordMember] = None
    user: typing.Optional[DiscordUser] = None
    data: typing.Union[*SlashCommand.__subclasses__()] = pydantic.Field(discriminator="name")