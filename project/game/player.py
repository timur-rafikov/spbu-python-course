from typing import Optional


class Player:
    """
    A class representing a player in the Zonk game.

    Attributes:
        name : str
            The name of the player.
        total_score : int
            The total score accumulated by the player.
        round_score : int
            The score accumulated in the current round.

    Methods:
        __init__(name: str)
            Initializes a Player object.

        add_round_score(score: int)
            Adds points to the current round score.

        bank_round_score()
            Banks the round score to the total score.

        reset_round_score()
            Resets the round score to zero.

        get_total_score() -> int
            Returns the total score.

        get_round_score() -> int
            Returns the current round score.

        __repr__() -> str
            Returns a string representation of the player.
    """

    def __init__(self, name: str):
        """
        Initializes a Player object.

        Args:
            name (str): The name of the player.
        """
        self.name: str = name
        self.total_score: int = 0
        self.round_score: int = 0

    def add_round_score(self, score: int) -> None:
        """
        Adds points to the current round score.

        Args:
            score (int): The score to add.
        """
        self.round_score += score

    def bank_round_score(self) -> None:
        """
        Banks the round score to the total score and resets round score.
        """
        self.total_score += self.round_score
        self.round_score = 0

    def reset_round_score(self) -> None:
        """
        Resets the round score to zero without banking.
        """
        self.round_score = 0

    def get_total_score(self) -> int:
        """
        Returns the total score.

        Returns:
            int: The total score.
        """
        return self.total_score

    def get_round_score(self) -> int:
        """
        Returns the current round score.

        Returns:
            int: The current round score.
        """
        return self.round_score

    def __repr__(self) -> str:
        """
        Returns a string representation of the player.

        Returns:
            str: A string representation of the player.
        """
        return f"Player(name={self.name}, total={self.total_score}, round={self.round_score})"
