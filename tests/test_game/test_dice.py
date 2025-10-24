from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.dice import Dice, roll_multiple_dice


def test_dice_initialization():
    dice = Dice()
    assert dice.value == 0, "Dice should initialize with value 0"


def test_dice_roll():
    dice = Dice()
    value = dice.roll()
    assert 1 <= value <= 6, f"Dice value should be between 1 and 6, got {value}"
    assert dice.get_value() == value, "get_value should return the rolled value"


def test_dice_roll_multiple_times():
    dice = Dice()
    values = [dice.roll() for _ in range(100)]
    assert all(1 <= v <= 6 for v in values), "All dice values should be between 1 and 6"
    assert len(set(values)) > 1, "Multiple rolls should produce different values"


def test_roll_multiple_dice():
    num_dice = 6
    values = roll_multiple_dice(num_dice)
    assert len(values) == num_dice, f"Should roll {num_dice} dice"
    assert all(1 <= v <= 6 for v in values), "All dice values should be between 1 and 6"


def test_dice_repr():
    dice = Dice()
    dice.roll()
    repr_str = repr(dice)
    assert "Dice" in repr_str, "repr should contain 'Dice'"
    assert str(dice.value) in repr_str, "repr should contain the dice value"
