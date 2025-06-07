from itertools import cycle

import pytest

from src.discord.commands.slashcommands import *
from src.discord.components import DiscordContext, DiscordMember, DiscordUser
from src.discord.interactions import DiscordMessage

@pytest.fixture
def ctx():
    mock_user = DiscordUser(id="81818181", username="TestUser", discriminator="Number81")
    mock_member = DiscordMember(user=mock_user,roles=[], joined_at="")
    mock_context = DiscordContext(member=mock_member)
    return mock_context


def test_CalculateTurns(ctx):

    spd = Options(name="speed", type=10, value=134)
    cycles = Options(name="cycles", type=4, value= 1)

    sub_command = CalculateTurns(name="turns", type=1, options=[spd, cycles])
    command = Calculate(id="165", name="calculate", type=1, options=[sub_command])

    output = "With a speed of 134, over the course of 1 cycle(s), a character would take 2.0 turns"

    assert command.execute(ctx) == DiscordMessage.generic_message(output)


def test_CalculateAV(ctx):

    spd = Options(name="speed", type=10, value=160)
    action_advance = Options(name="action_advance", type=10, value=0.2)

    sub_command = CalculateAV(name="av", options=[spd, action_advance], type=1)
    command = Calculate(id="818181", name="calculate", type=1, options=[sub_command])

    expected_output = f"A character with a speed of 160 and a 20.0% action advance has an AV of 50.0"
    assert command.execute(ctx) == DiscordMessage.generic_message(expected_output)