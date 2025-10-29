import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

os.chdir(project_root)

from project.game.game import Game
from project.game.player import Player
from project.game.strategies import (
    ConservativeStrategy,
    AggressiveStrategy,
    BalancedStrategy,
)


def display_turn_info(turn_info):
    """Display detailed information about a turn."""
    print(f"\n{'='*60}")
    print(f"Player: {turn_info['player']}")
    print(f"{'='*60}")

    for i, roll_info in enumerate(turn_info["rolls"], 1):
        print(f"\n  Roll {i}:")
        print(f"    Dice: {roll_info['dice']}")

        if roll_info.get("zonk"):
            print("    [X] ZONK! No scoring combinations!")
        else:
            print(f"    Score: {roll_info['score']}")
            print(f"    Scoring dice: {roll_info['scoring_dice']}")
            print(f"    Kept dice: {roll_info['kept_dice']}")

    if turn_info["zonk"]:
        print(f"\n  [!] ZONK! Lost all round points!")
    elif turn_info["banked"]:
        print(f"\n  [OK] Banked score! Total: {turn_info['final_score']}")

    print(f"{'='*60}")


def main():
    """Run a demo game of Zonk with three bots (non-interactive)."""
    print("\n" + "=" * 60)
    print("ZONK GAME - Demo (Non-Interactive)")
    print("=" * 60)
    print("\nThree bots will compete to reach 2000 points:")
    print("  - ConservativeBot: Banks after 350 points, avoids risks")
    print("  - AggressiveBot: Takes more risks, banks after 600 points")
    print("  - BalancedBot: Moderate risk-taking, banks after 450 points")
    print("=" * 60)

    players = [
        Player("ConservativeBot"),
        Player("AggressiveBot"),
        Player("BalancedBot"),
    ]

    strategies = [
        ConservativeStrategy(),
        AggressiveStrategy(),
        BalancedStrategy(),
    ]

    game = Game(players, strategies, target_score=2000)

    turn_count = 0
    max_turns = 30

    while not game.is_game_over() and turn_count < max_turns:
        print(game.display_game_state())

        turn_info = game.play_turn()
        display_turn_info(turn_info)

        turn_count += 1

    print("\n" + "=" * 60)
    print("GAME OVER!")
    print("=" * 60)
    print(game.display_game_state())

    winner = game.get_winner()
    if winner:
        print(
            f"\n*** WINNER: {winner.name} with {winner.get_total_score()} points! ***"
        )

    print("\nFinal Standings:")
    sorted_players = sorted(
        game.players, key=lambda p: p.get_total_score(), reverse=True
    )
    for i, player in enumerate(sorted_players, 1):
        print(f"  {i}. {player.name}: {player.get_total_score()} points")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
