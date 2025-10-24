from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.score_calculator import ScoreCalculator


def test_single_one():
    dice = [1]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 100, f"Single 1 should score 100, got {score}"


def test_single_five():
    dice = [5]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 50, f"Single 5 should score 50, got {score}"


def test_three_ones():
    dice = [1, 1, 1]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 1000, f"Three 1s should score 1000, got {score}"


def test_three_twos():
    dice = [2, 2, 2]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 200, f"Three 2s should score 200, got {score}"


def test_three_threes():
    dice = [3, 3, 3]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 300, f"Three 3s should score 300, got {score}"


def test_three_fours():
    dice = [4, 4, 4]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 400, f"Three 4s should score 400, got {score}"


def test_three_fives():
    dice = [5, 5, 5]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 500, f"Three 5s should score 500, got {score}"


def test_three_sixes():
    dice = [6, 6, 6]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 600, f"Three 6s should score 600, got {score}"


def test_straight():
    dice = [1, 2, 3, 4, 5, 6]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 1500, f"Straight should score 1500, got {score}"


def test_three_pairs():
    dice = [1, 1, 2, 2, 3, 3]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 750, f"Three pairs should score 750, got {score}"


def test_zonk():
    dice = [2, 3, 4, 6]
    assert ScoreCalculator.is_zonk(dice), "Should be a zonk"
    score = ScoreCalculator.calculate_score(dice)
    assert score == 0, f"Zonk should score 0, got {score}"


def test_mixed_scoring_dice():
    dice = [1, 5, 2, 3]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 150, f"1 and 5 should score 150, got {score}"


def test_four_ones():
    dice = [1, 1, 1, 1]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 1100, f"Four 1s should score 1100 (1000 + 100), got {score}"


def test_get_scoring_dice():
    dice = [1, 5, 2, 3, 6]
    scoring = ScoreCalculator.get_scoring_dice(dice)
    assert 1 in scoring, "Scoring dice should include 1"
    assert 5 in scoring, "Scoring dice should include 5"
    assert 2 not in scoring, "Scoring dice should not include 2"


def test_is_not_zonk():
    dice = [1, 2, 3, 4]
    assert not ScoreCalculator.is_zonk(dice), "Should not be a zonk with a 1"


def test_empty_dice():
    dice = []
    score = ScoreCalculator.calculate_score(dice)
    assert score == 0, "Empty dice should score 0"


def test_three_ones_with_five():
    dice = [1, 1, 1, 5, 2, 3]
    score = ScoreCalculator.calculate_score(dice)
    assert score == 1050, f"Three 1s and a 5 should score 1050, got {score}"
