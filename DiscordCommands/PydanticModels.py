from pydantic import BaseModel
import pydantic
import typing


class DiscordUser(BaseModel):
    id: str
    username: str
    avatar: typing.Optional[str] = None
    discriminator: str
    public_flags: int

class DiscordMember(BaseModel):
    user: DiscordUser
    roles: list[str]
    premium_since: typing.Optional[str] = None
    permissions: str
    pending: bool
    nick: typing.Optional[str] = None
    mute: bool
    joined_at: str
    deaf: bool

class DiscordMessageContent(BaseModel):
    content: str

class BotMessage(BaseModel):
    type: typing.Literal[1, 4, 5, 6, 7, 8, 9]
    data: typing.Optional[DiscordMessageContent] = None

class DiscordPing(BaseModel):
    type: typing.Literal[1]

class SlashGreet(BaseModel):
    id: str
    name: typing.Literal["greet"]
    type: typing.Literal[1]
    options: typing.Optional[list[dict]] = None

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
    data: typing.Union[SlashGreet] = pydantic.Field(discriminator="type")



    """
    ```
{
    "type": 2,
    "token": "A_UNIQUE_TOKEN",
    "member": {
        "user": {
            "id": "A_USER_ID",
            "username": "A_USERNAME",
            "avatar": "GUILD_AVATAR_HASH",
            "discriminator": "1337",
            "public_flags": 131141
        },
        "roles": ["12345678"],
        "premium_since": null,
        "permissions": "2147483647",
        "pending": false,
        "nick": null,
        "mute": false,
        "joined_at": "2019-04-14T12:14:14.000000+00:00",
        "is_pending": false,
        "deaf": false
    },
    "id": "INTERACTION_ID",
    "application_id": "YOUR_APP_ID",
    "app_permissions": "442368",
    "guild_id": "A_GUILD_ID",
    "guild_locale": "en-US",
    "locale": "en-US",
    "data": {
        "options": [{
            "name": "Igneous",
            "value": "rock_igneous"
        }],
        "name": "rock",
        "id": "APPLICATION_COMMAND_ID"
    },
    "channel_id": "ASSOCIATED_CHANNEL_ID"
}
```
    """