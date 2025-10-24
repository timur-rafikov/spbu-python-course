from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.strategies import (
    ConservativeStrategy,
    AggressiveStrategy,
    BalancedStrategy,
)


def test_conservative_strategy_continues():
    strategy = ConservativeStrategy()
    assert strategy.should_continue(
        200, 4, 1000
    ), "Should continue with 200 points and 4 dice"


def test_conservative_strategy_banks():
    strategy = ConservativeStrategy()
    assert not strategy.should_continue(400, 4, 1000), "Should bank with 400 points"


def test_conservative_strategy_stops_with_few_dice():
    strategy = ConservativeStrategy()
    assert not strategy.should_continue(100, 2, 1000), "Should stop with only 2 dice"


def test_conservative_keeps_all_scoring_dice():
    strategy = ConservativeStrategy()
    dice = [1, 5, 2, 3]
    scoring_dice = [1, 5]
    kept = strategy.choose_dice_to_keep(dice, scoring_dice)
    assert kept == scoring_dice, "Should keep all scoring dice"


def test_aggressive_strategy_continues():
    strategy = AggressiveStrategy()
    assert strategy.should_continue(400, 2, 1000), "Should continue with 400 points"


def test_aggressive_strategy_banks():
    strategy = AggressiveStrategy()
    assert not strategy.should_continue(650, 3, 1000), "Should bank with 650 points"


def test_aggressive_strategy_continues_with_few_dice():
    strategy = AggressiveStrategy()
    assert strategy.should_continue(200, 1, 1000), "Should continue even with 1 dice"


def test_balanced_strategy_moderate_behavior():
    strategy = BalancedStrategy()
    assert strategy.should_continue(300, 3, 1000), "Should continue with 300 points"
    assert not strategy.should_continue(500, 3, 1000), "Should bank with 500 points"


def test_balanced_strategy_adapts_to_score():
    strategy = BalancedStrategy()
    assert not strategy.should_continue(
        350, 2, 8500
    ), "Should be more conservative when close to winning"


def test_balanced_strategy_one_dice():
    strategy = BalancedStrategy()
    assert strategy.should_continue(
        200, 1, 1000
    ), "Should continue with 1 dice if round score is low"
    assert not strategy.should_continue(
        350, 1, 1000
    ), "Should stop with 1 dice if round score is high"


def test_strategies_are_different():
    conservative = ConservativeStrategy()
    aggressive = AggressiveStrategy()
    balanced = BalancedStrategy()

    round_score = 400
    num_dice = 3
    total_score = 1000

    cons_result = conservative.should_continue(round_score, num_dice, total_score)
    agg_result = aggressive.should_continue(round_score, num_dice, total_score)
    bal_result = balanced.should_continue(round_score, num_dice, total_score)

    assert not all([cons_result, agg_result, bal_result]) or not any(
        [cons_result, agg_result, bal_result]
    ), "Strategies should behave differently"
