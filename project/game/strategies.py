from abc import ABC, abstractmethod
from typing import List, Tuple
import random


class Strategy(ABC):
    """
    Abstract base class for bot strategies.

    Methods:
        should_continue(round_score: int, num_dice: int, total_score: int) -> bool
            Decides whether to continue rolling or bank the score.

        choose_dice_to_keep(dice: list[int], scoring_dice: list[int]) -> list[int]
            Chooses which scoring dice to keep.
    """

    @abstractmethod
    def should_continue(
        self, round_score: int, num_dice: int, total_score: int
    ) -> bool:
        """
        Decides whether to continue rolling or bank the score.

        Args:
            round_score (int): Current round score.
            num_dice (int): Number of dice available for rolling.
            total_score (int): Total score of the player.

        Returns:
            bool: True to continue rolling, False to bank.
        """
        pass

    @abstractmethod
    def choose_dice_to_keep(
        self, dice: List[int], scoring_dice: List[int]
    ) -> List[int]:
        """
        Chooses which scoring dice to keep.

        Args:
            dice (list[int]): All dice rolled.
            scoring_dice (list[int]): Dice that can score points.

        Returns:
            list[int]: Dice to keep for scoring.
        """
        pass


class ConservativeStrategy(Strategy):
    """
    Conservative strategy that avoids risks.

    This strategy:
    - Banks score after reaching 350 points in a round
    - Always keeps all scoring dice
    - Stops if only 1-2 dice remain
    """

    def should_continue(
        self, round_score: int, num_dice: int, total_score: int
    ) -> bool:
        """
        Decides whether to continue rolling.

        Args:
            round_score (int): Current round score.
            num_dice (int): Number of dice available for rolling.
            total_score (int): Total score of the player.

        Returns:
            bool: True to continue rolling, False to bank.
        """
        if round_score >= 350:
            return False
        if num_dice <= 2:
            return False
        return True

    def choose_dice_to_keep(
        self, dice: List[int], scoring_dice: List[int]
    ) -> List[int]:
        """
        Always keeps all scoring dice.

        Args:
            dice (list[int]): All dice rolled.
            scoring_dice (list[int]): Dice that can score points.

        Returns:
            list[int]: All scoring dice.
        """
        return scoring_dice


class AggressiveStrategy(Strategy):
    """
    Aggressive strategy that takes more risks.

    This strategy:
    - Only banks after reaching 600 points in a round
    - May keep only some scoring dice to maximize remaining dice
    - Continues rolling even with few dice
    """

    def should_continue(
        self, round_score: int, num_dice: int, total_score: int
    ) -> bool:
        """
        Decides whether to continue rolling.

        Args:
            round_score (int): Current round score.
            num_dice (int): Number of dice available for rolling.
            total_score (int): Total score of the player.

        Returns:
            bool: True to continue rolling, False to bank.
        """
        if round_score >= 600:
            return False
        return True

    def choose_dice_to_keep(
        self, dice: List[int], scoring_dice: List[int]
    ) -> List[int]:
        """
        Keeps minimum scoring dice to maximize remaining dice.

        Args:
            dice (list[int]): All dice rolled.
            scoring_dice (list[int]): Dice that can score points.

        Returns:
            list[int]: Selected scoring dice.
        """
        if len(scoring_dice) >= 3:
            return scoring_dice[: min(3, len(scoring_dice))]
        return scoring_dice


class BalancedStrategy(Strategy):
    """
    Balanced strategy with moderate risk.

    This strategy:
    - Banks after reaching 450 points in a round
    - Adapts based on current total score
    - Considers number of remaining dice
    """

    def should_continue(
        self, round_score: int, num_dice: int, total_score: int
    ) -> bool:
        """
        Decides whether to continue rolling.

        Args:
            round_score (int): Current round score.
            num_dice (int): Number of dice available for rolling.
            total_score (int): Total score of the player.

        Returns:
            bool: True to continue rolling, False to bank.
        """
        if round_score >= 450:
            return False

        if num_dice == 1:
            return round_score < 300

        if total_score >= 8000:
            return round_score < 300

        return True

    def choose_dice_to_keep(
        self, dice: List[int], scoring_dice: List[int]
    ) -> List[int]:
        """
        Keeps scoring dice based on situation.

        Args:
            dice (list[int]): All dice rolled.
            scoring_dice (list[int]): Dice that can score points.

        Returns:
            list[int]: Selected scoring dice.
        """
        if len(scoring_dice) <= 2:
            return scoring_dice

        if len(dice) - len(scoring_dice) <= 1:
            return scoring_dice

        keep_count = max(2, len(scoring_dice) // 2)
        return scoring_dice[:keep_count]
