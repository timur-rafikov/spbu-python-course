from typing import List, Optional, Tuple
from project.game.player import Player
from project.game.strategies import Strategy
from project.game.dice import roll_multiple_dice
from project.game.score_calculator import ScoreCalculator


class Game:
    """
    Main game class for Zonk dice game.

    Attributes:
        players : list[Player]
            List of players in the game.
        strategies : list[Strategy]
            List of strategies for each player.
        target_score : int
            The score needed to win.
        current_player_index : int
            Index of the current player.
        round_number : int
            Current round number.
        game_over : bool
            Whether the game has ended.
        winner : Player | None
            The winner of the game.

    Methods:
        __init__(players: list[Player], strategies: list[Strategy], target_score: int)
            Initializes a Game object.

        play_round() -> dict
            Plays one round for the current player.

        play_turn() -> dict
            Plays a complete turn for the current player.

        play_game(max_rounds: int | None) -> Player
            Plays the entire game until someone wins.

        get_game_state() -> dict
            Returns the current state of the game.

        display_game_state() -> str
            Returns a formatted string of the game state.

        is_game_over() -> bool
            Checks if the game is over.

        get_winner() -> Player | None
            Returns the winner if game is over.
    """

    def __init__(
        self,
        players: List[Player],
        strategies: List[Strategy],
        target_score: int = 10000,
    ):
        """
        Initializes a Game object.

        Args:
            players (list[Player]): List of players.
            strategies (list[Strategy]): List of strategies for each player.
            target_score (int): The score needed to win (default 10000).

        Raises:
            ValueError: If number of players and strategies don't match.
        """
        if len(players) != len(strategies):
            raise ValueError("Number of players must match number of strategies")

        self.players: List[Player] = players
        self.strategies: List[Strategy] = strategies
        self.target_score: int = target_score
        self.current_player_index: int = 0
        self.round_number: int = 1
        self.game_over: bool = False
        self.winner: Optional[Player] = None

    def play_turn(self) -> dict:
        """
        Plays a complete turn for the current player.

        Returns:
            dict: Turn information including rolls, scores, and actions.
        """
        player = self.players[self.current_player_index]
        strategy = self.strategies[self.current_player_index]
        player.reset_round_score()

        num_dice = 6
        turn_info = {
            "player": player.name,
            "rolls": [],
            "zonk": False,
            "final_score": 0,
            "banked": False,
        }

        while True:
            dice = roll_multiple_dice(num_dice)
            roll_info = {"dice": dice, "num_dice": num_dice}

            if ScoreCalculator.is_zonk(dice):
                roll_info["zonk"] = True
                turn_info["rolls"].append(roll_info)
                turn_info["zonk"] = True
                player.reset_round_score()
                break

            score, scoring_dice = ScoreCalculator.find_best_scoring_combination(dice)
            roll_info["score"] = score
            roll_info["scoring_dice"] = scoring_dice

            kept_dice = strategy.choose_dice_to_keep(dice, scoring_dice)
            player.add_round_score(score)
            roll_info["kept_dice"] = kept_dice

            turn_info["rolls"].append(roll_info)

            num_dice_used = len(kept_dice)
            num_dice -= num_dice_used

            if num_dice == 0:
                num_dice = 6

            if not strategy.should_continue(
                player.get_round_score(), num_dice, player.get_total_score()
            ):
                player.bank_round_score()
                turn_info["banked"] = True
                turn_info["final_score"] = player.get_round_score()
                break

        if turn_info["banked"]:
            turn_info["final_score"] = self.players[
                self.current_player_index
            ].get_total_score()

        if (
            self.players[self.current_player_index].get_total_score()
            >= self.target_score
        ):
            self.game_over = True
            self.winner = self.players[self.current_player_index]

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.round_number += 1

        return turn_info

    def play_game(self, max_rounds: Optional[int] = None) -> Optional[Player]:
        """
        Plays the entire game until someone wins or max rounds reached.

        Args:
            max_rounds (int | None): Maximum number of rounds to play.

        Returns:
            Player | None: The winner, or None if max rounds reached.
        """
        while not self.game_over:
            self.play_turn()

            if max_rounds and self.round_number > max_rounds:
                max_score = max(p.get_total_score() for p in self.players)
                winners = [p for p in self.players if p.get_total_score() == max_score]
                self.winner = winners[0]
                self.game_over = True
                break

        return self.winner

    def get_game_state(self) -> dict:
        """
        Returns the current state of the game.

        Returns:
            dict: Game state information.
        """
        return {
            "round": self.round_number,
            "current_player": self.players[self.current_player_index].name,
            "players": [
                {
                    "name": p.name,
                    "total_score": p.get_total_score(),
                    "round_score": p.get_round_score(),
                }
                for p in self.players
            ],
            "target_score": self.target_score,
            "game_over": self.game_over,
            "winner": self.winner.name if self.winner else None,
        }

    def display_game_state(self) -> str:
        """
        Returns a formatted string of the game state.

        Returns:
            str: Formatted game state.
        """
        state = self.get_game_state()
        output = f"\n{'='*60}\n"
        output += (
            f"Round {state['round']} | Current Player: {state['current_player']}\n"
        )
        output += f"{'='*60}\n"

        for player_info in state["players"]:
            output += f"{player_info['name']:20} | Total: {player_info['total_score']:5} | Round: {player_info['round_score']:4}\n"

        output += f"{'='*60}\n"
        output += f"Target Score: {state['target_score']}\n"

        if state["game_over"]:
            output += f"\n*** WINNER: {state['winner']} ***\n"

        return output

    def is_game_over(self) -> bool:
        """
        Checks if the game is over.

        Returns:
            bool: True if game is over, False otherwise.
        """
        return self.game_over

    def get_winner(self) -> Optional[Player]:
        """
        Returns the winner if game is over.

        Returns:
            Player | None: The winner, or None if game is not over.
        """
        return self.winner
