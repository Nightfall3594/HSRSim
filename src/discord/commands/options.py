from pydantic import BaseModel
import typing

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