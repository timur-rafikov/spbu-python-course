from typing import List, Tuple, Dict
from collections import Counter


class ScoreCalculator:
    """
    A class for calculating scores in the Zonk dice game.

    Methods:
        calculate_score(dice: list[int]) -> int
            Calculates the total score for a given dice roll.

        get_scoring_dice(dice: list[int]) -> list[int]
            Returns the dice that contribute to the score.

        is_zonk(dice: list[int]) -> bool
            Checks if the dice roll is a zonk (no scoring combinations).

        find_best_scoring_combination(dice: list[int]) -> tuple[int, list[int]]
            Finds the best scoring combination and returns score and used dice.
    """

    @staticmethod
    def calculate_score(dice: List[int]) -> int:
        """
        Calculates the total score for a given dice roll.

        Args:
            dice (list[int]): List of dice values.

        Returns:
            int: The total score.
        """
        if not dice:
            return 0

        dice_sorted = sorted(dice)

        if ScoreCalculator._is_straight(dice_sorted):
            return 1500

        score, _ = ScoreCalculator.find_best_scoring_combination(dice)
        return score

    @staticmethod
    def _is_straight(dice: List[int]) -> bool:
        """
        Checks if the dice form a straight (1-2-3-4-5-6).

        Args:
            dice (list[int]): Sorted list of dice values.

        Returns:
            bool: True if the dice form a straight, False otherwise.
        """
        return len(dice) == 6 and dice == [1, 2, 3, 4, 5, 6]

    @staticmethod
    def _is_three_pairs(dice: List[int]) -> bool:
        """
        Checks if the dice form three pairs.

        Args:
            dice (list[int]): List of dice values.

        Returns:
            bool: True if the dice form three pairs, False otherwise.
        """
        if len(dice) != 6:
            return False

        counts = Counter(dice)
        pairs = [count for count in counts.values() if count == 2]
        return len(pairs) == 3

    @staticmethod
    def find_best_scoring_combination(dice: List[int]) -> Tuple[int, List[int]]:
        """
        Finds the best scoring combination for the given dice.

        Args:
            dice (list[int]): List of dice values.

        Returns:
            tuple[int, list[int]]: Total score and list of dice used for scoring.
        """
        if not dice:
            return 0, []

        dice_sorted = sorted(dice)

        if ScoreCalculator._is_straight(dice_sorted):
            return 1500, dice_sorted

        if ScoreCalculator._is_three_pairs(dice_sorted):
            return 750, dice_sorted

        counts = Counter(dice)
        score = 0
        used_dice = []

        for value, count in counts.items():
            if count >= 3:
                if value == 1:
                    base_score = 1000
                else:
                    base_score = value * 100

                score += base_score
                used_dice.extend([value] * 3)

                remaining = count - 3
                if value == 1:
                    score += remaining * 100
                    used_dice.extend([1] * remaining)
                elif value == 5:
                    score += remaining * 50
                    used_dice.extend([5] * remaining)
            else:
                if value == 1:
                    score += count * 100
                    used_dice.extend([1] * count)
                elif value == 5:
                    score += count * 50
                    used_dice.extend([5] * count)

        return score, sorted(used_dice)

    @staticmethod
    def get_scoring_dice(dice: List[int]) -> List[int]:
        """
        Returns the dice that contribute to the score.

        Args:
            dice (list[int]): List of dice values.

        Returns:
            list[int]: List of dice that score points.
        """
        _, scoring_dice = ScoreCalculator.find_best_scoring_combination(dice)
        return scoring_dice

    @staticmethod
    def is_zonk(dice: List[int]) -> bool:
        """
        Checks if the dice roll is a zonk (no scoring combinations).

        Args:
            dice (list[int]): List of dice values.

        Returns:
            bool: True if the roll is a zonk, False otherwise.
        """
        score, _ = ScoreCalculator.find_best_scoring_combination(dice)
        return score == 0

    @staticmethod
    def get_possible_scoring_options(dice: List[int]) -> List[Tuple[int, List[int]]]:
        """
        Returns all possible scoring options for the given dice.

        Args:
            dice (list[int]): List of dice values.

        Returns:
            list[tuple[int, list[int]]]: List of (score, dice_used) tuples.
        """
        if not dice:
            return [(0, [])]

        options = []

        dice_sorted = sorted(dice)
        if ScoreCalculator._is_straight(dice_sorted):
            options.append((1500, dice_sorted))
            return options

        if ScoreCalculator._is_three_pairs(dice_sorted):
            options.append((750, dice_sorted))

        best_score, best_dice = ScoreCalculator.find_best_scoring_combination(dice)
        if best_score > 0:
            options.append((best_score, best_dice))

        return options if options else [(0, [])]
