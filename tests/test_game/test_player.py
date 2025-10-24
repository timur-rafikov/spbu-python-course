from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.player import Player


@pytest.fixture
def player():
    return Player("TestBot")


def test_player_initialization():
    player = Player("TestPlayer")
    assert player.name == "TestPlayer", "Player name should be set correctly"
    assert player.total_score == 0, "Total score should start at 0"
    assert player.round_score == 0, "Round score should start at 0"


def test_add_round_score(player: Player):
    player.add_round_score(100)
    assert player.get_round_score() == 100, "Round score should be 100"
    assert player.get_total_score() == 0, "Total score should still be 0"


def test_bank_round_score(player: Player):
    player.add_round_score(150)
    player.bank_round_score()
    assert player.get_total_score() == 150, "Total score should be 150"
    assert player.get_round_score() == 0, "Round score should reset to 0"


def test_reset_round_score(player: Player):
    player.add_round_score(200)
    player.reset_round_score()
    assert player.get_round_score() == 0, "Round score should be reset to 0"
    assert player.get_total_score() == 0, "Total score should remain 0"


def test_multiple_rounds(player: Player):
    player.add_round_score(100)
    player.bank_round_score()

    player.add_round_score(200)
    player.bank_round_score()

    assert player.get_total_score() == 300, "Total score should be 300"


def test_player_repr(player: Player):
    repr_str = repr(player)
    assert "Player" in repr_str, "repr should contain 'Player'"
    assert player.name in repr_str, "repr should contain player name"
