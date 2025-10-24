import random
from typing import List


class Dice:
    """
    A class representing a single dice.

    Attributes:
        value : int
            The current value of the dice (1-6).

    Methods:
        __init__()
            Initializes a Dice object.

        roll() -> int
            Rolls the dice and returns a random value between 1 and 6.

        get_value() -> int
            Returns the current value of the dice.

        __repr__() -> str
            Returns a string representation of the dice.
    """

    def __init__(self):
        """
        Initializes a Dice object with no initial value.
        """
        self.value: int = 0

    def roll(self) -> int:
        """
        Rolls the dice and returns a random value between 1 and 6.

        Returns:
            int: The rolled value.
        """
        self.value = random.randint(1, 6)
        return self.value

    def get_value(self) -> int:
        """
        Returns the current value of the dice.

        Returns:
            int: The current value of the dice.
        """
        return self.value

    def __repr__(self) -> str:
        """
        Returns a string representation of the dice.

        Returns:
            str: A string representation of the dice.
        """
        return f"Dice({self.value})"


def roll_multiple_dice(num_dice: int) -> List[int]:
    """
    Rolls multiple dice and returns their values.

    Args:
        num_dice (int): The number of dice to roll.

    Returns:
        list[int]: A list of rolled values.
    """
    dice_list = [Dice() for _ in range(num_dice)]
    return [dice.roll() for dice in dice_list]
