import json

import pytest

from src.discord.commands.slashcommands import *
from src.discord.component_commands.string_select_command import CharacterSelectCommand
from src.discord.components import DiscordContext, DiscordMember, DiscordUser
from src.discord.components.message_components import StringSelectOption
from src.discord.interactions import InteractionResponse
from src.discord.interactions.interaction_types import DiscordInteraction, ComponentInteraction


@pytest.fixture
def ctx():
    mock_user = DiscordUser(id="81818181", username="TestUser", discriminator="Number81")
    mock_member = DiscordMember(user=mock_user,roles=[], joined_at="")
    mock_context = DiscordContext(member=mock_member)
    return mock_context


@pytest.mark.asyncio
async def test_greet(ctx):

    command = Greet(id="818181", name="greet", type=1, options=[])
    expected_message = f"Hello, {ctx.member.user.username}. Would you like some cake?"

    assert await command.execute(ctx) == InteractionResponse.generic_message(expected_message)


@pytest.mark.asyncio
async def test_CalculateTurns(ctx):

    spd = Options(name="speed", type=10, value=134)
    cycles = Options(name="cycles", type=4, value= 1)

    sub_command = CalculateTurns(name="turns", type=1, options=[spd, cycles])
    command = Calculate(id="165", name="calculate", type=1, options=[sub_command])

    output = "With a speed of 134, over the course of 1 cycle(s), a character would take 2.0 turns"

    assert await command.execute(ctx) == InteractionResponse.generic_message(output)


@pytest.mark.asyncio
async def test_CalculateAV(ctx):

    spd = Options(name="speed", type=10, value=160)
    action_advance = Options(name="action_advance", type=10, value=0.2)

    sub_command = CalculateAV(name="av", options=[spd, action_advance], type=1)
    command = Calculate(id="818181", name="calculate", type=1, options=[sub_command])

    expected_output = f"A character with a speed of 160 and a 20.0% action advance has an AV of 50.0"
    assert await command.execute(ctx) == InteractionResponse.generic_message(expected_output)

@pytest.mark.asyncio
async def test_ShowBuildString(ctx):

    uid = Options(name="uid", type=3, value="805629555")
    subcommand = ShowBuild(name="build", type=1, options=[uid])
    command = SlashShow(id = "81818181" ,name="show", type=1, options=[subcommand])

    chars = [StringSelectOption(label="Ruan Mei", value="805629555;Ruan Mei")]
    expected_output = BuildMessage.string_select(chars, custom_id="character_select")

    assert await command.execute(ctx) == expected_output


# @pytest.mark.asyncio
# async def test_StringSelectChar(ctx):
#
#     uid = Options(name="uid", type=3, value="805629555")
#     subcommand: ShowBuild = ShowBuild(name="build", type=1, options=[uid])
#     command: SlashShow = SlashShow(id = "81818181" ,name="show", type=1, options=[subcommand])
#
#     string_select: BuildMessage = command.execute(ctx)


@pytest.mark.asyncio
async def test_stringHanlder(ctx):

    mock_input = CharacterSelectCommand(component_type=3, custom_id="character_select", values=["805629555;Ruan Mei"])

    async with enka.HSRClient() as client:
        showcase = await client.fetch_showcase("805629555")
    rm = showcase.characters[0]


    assert await mock_input.execute(ctx) == BuildMessage.build_showcase(rm)


@pytest.mark.asyncio
async def test_stringHanlder2(ctx):

    mock_input = CharacterSelectCommand(component_type=3, custom_id="character_select", values=["831414160;The Herta"])

    async with enka.HSRClient() as client:
        showcase = await client.fetch_showcase("831414160")

    for char in showcase.characters:
        if char.name == "The Herta":
            tHerta = char


    assert await mock_input.execute(ctx) == BuildMessage.build_showcase(tHerta)


@pytest.mark.asyncio
async def test_FullMockInputForStringSelectHandler(ctx):

    sent_message = """{
    "type": 3,
    "token": "MOCK_INTERACTION_TOKEN_12345ABC",
    "id": "123456789012345678",
    "application_id": "845027738276462632",
    "app_permissions": "4398046511103",
    "guild_id": "772904309264089089",
    "guild_locale": "en-US",
    "locale": "en-US",
    "member": {
        "avatar": null,
        "deaf": false,
        "is_pending": false,
        "joined_at": "2023-01-15T10:30:00.000000+00:00",
        "mute": false,
        "nick": "TestUser",
        "pending": false,
        "permissions": "2147483647",
        "premium_since": null,
        "roles": ["785609923542777878"],
        "user": {
            "avatar": "abcdef1234567890abcdef1234567890",
            "discriminator": "0001",
            "id": "53908232506183680",
            "public_flags": 64,
            "username": "ExampleUser"
        }
    },
    "user": {
        "avatar": "abcdef1234567890abcdef1234567890",
        "discriminator": "0001",
        "id": "53908232506183680",
        "public_flags": 64,
        "username": "ExampleUser"
    },
    "data": {
        "component_type": 3,
        "custom_id": "character_select",
        "values": [
            "831414160;The Herta"
        ]
    },
    "channel_id": "772908445358620702",
    "version": 1
}"""

    interaction = ComponentInteraction(**json.loads(sent_message))

    mock_input = CharacterSelectCommand(component_type=3, custom_id="character_select", values=["831414160;The Herta"])

    async with enka.HSRClient() as client:
        showcase = await client.fetch_showcase("831414160")

    for char in showcase.characters:
        if char.name == "The Herta":
            tHerta = char

    assert await interaction.data.execute(ctx) == BuildMessage.build_showcase(tHerta)






