from pydantic import BaseModel
import typing


class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: typing.Optional[str] = None
    discriminator: str
    public_flags: typing.Optional[int] = None

class DiscordMember(BaseModel):
    user: DiscordUser
    roles: list[str]
    premium_since: typing.Optional[str] = None
    permissions: typing.Optional[str] = None
    pending: typing.Optional[bool] = None
    nick: typing.Optional[str] = None
    mute: typing.Optional[bool] = None
    joined_at: str
    deaf: typing.Optional[bool] = None


class DiscordMessageContent(BaseModel):
    content: str

class BotMessage(BaseModel):
    type: typing.Literal[1, 4, 5, 6, 7, 8, 9]
    data: typing.Optional[DiscordMessageContent] = None

    @classmethod
    def generic_message(cls, text: str):
        return cls(type=4, data=DiscordMessageContent(content=text))

    @classmethod
    def deferred_message(cls, text: str):
        return cls(type=5, data=DiscordMessageContent(content=text))

class DiscordPing(BaseModel):
    type: typing.Literal[1]


class DiscordContext(BaseModel):
    member: typing.Optional[DiscordMember] = None


class Options(BaseModel):
    name: str
    type: typing.Literal[3,4,5,6,7,8,9,10]  # this is the dtype of the input. Refer to docs below.
    value: typing.Union[int, float, bool, str, None]

    """
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

