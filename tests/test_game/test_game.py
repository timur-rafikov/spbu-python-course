from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.game import Game
from project.game.player import Player
from project.game.strategies import (
    ConservativeStrategy,
    AggressiveStrategy,
    BalancedStrategy,
)


@pytest.fixture
def game_setup():
    players = [Player("Bot1"), Player("Bot2"), Player("Bot3")]
    strategies = [
        ConservativeStrategy(),
        AggressiveStrategy(),
        BalancedStrategy(),
    ]
    return players, strategies


def test_game_initialization(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=5000)

    assert len(game.players) == 3, "Should have 3 players"
    assert game.target_score == 5000, "Target score should be 5000"
    assert game.round_number == 1, "Should start at round 1"
    assert not game.game_over, "Game should not be over at start"


def test_game_initialization_mismatched_strategies():
    players = [Player("Bot1"), Player("Bot2")]
    strategies = [ConservativeStrategy()]

    with pytest.raises(ValueError):
        Game(players, strategies)


def test_game_state_changes_after_turn(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=5000)

    initial_state = game.get_game_state()
    game.play_turn()
    new_state = game.get_game_state()

    assert (
        initial_state["current_player"] != new_state["current_player"]
    ), "Current player should change after turn"


def test_play_turn_returns_info(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=5000)

    turn_info = game.play_turn()

    assert "player" in turn_info, "Turn info should contain player"
    assert "rolls" in turn_info, "Turn info should contain rolls"
    assert "zonk" in turn_info, "Turn info should contain zonk status"
    assert "final_score" in turn_info, "Turn info should contain final score"


def test_game_tracks_rounds(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=10000)

    initial_round = game.round_number

    for _ in range(3):
        game.play_turn()

    assert game.round_number > initial_round, "Round number should increase"


def test_game_ends_when_target_reached(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=100)

    winner = game.play_game(max_rounds=100)

    assert game.is_game_over(), "Game should be over"
    assert winner is not None, "Should have a winner"
    assert winner.get_total_score() >= 100, "Winner should have reached target score"


def test_game_state_display(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=5000)

    state_str = game.display_game_state()

    assert "Round" in state_str, "Display should show round number"
    assert "Bot1" in state_str, "Display should show player names"
    assert "Total" in state_str, "Display should show total scores"


def test_game_with_max_rounds(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=100000)

    winner = game.play_game(max_rounds=5)

    assert game.is_game_over(), "Game should end after max rounds"
    assert winner is not None, "Should have a winner based on highest score"


def test_player_scores_increase(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=10000)

    initial_scores = [p.get_total_score() for p in game.players]

    for _ in range(20):
        game.play_turn()
        if game.is_game_over():
            break

    final_scores = [p.get_total_score() for p in game.players]

    assert any(
        final > initial for final, initial in zip(final_scores, initial_scores)
    ), "At least one player should have increased score"


def test_get_winner_before_game_over(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=10000)

    assert game.get_winner() is None, "Should not have winner before game ends"


def test_game_state_structure(game_setup):
    players, strategies = game_setup
    game = Game(players, strategies, target_score=5000)

    state = game.get_game_state()

    assert "round" in state, "State should have round"
    assert "current_player" in state, "State should have current player"
    assert "players" in state, "State should have players list"
    assert "target_score" in state, "State should have target score"
    assert "game_over" in state, "State should have game_over flag"
    assert "winner" in state, "State should have winner field"
