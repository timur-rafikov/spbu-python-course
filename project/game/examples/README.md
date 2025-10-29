# Zonk Game Examples

This folder contains example implementations of the Zonk dice game.

## Files

### 1. `zonk_game_example.py` (Interactive)
An interactive version where you press Enter after each turn to see the next move.

**How to run:**

From project root:
```bash
python project/game/examples/zonk_game_example.py
```

Or as a module:
```bash
python -m project.game.examples.zonk_game_example
```

**Features:**
- Three bots compete to reach 5000 points
- Interactive mode - press Enter to see each turn
- Full game state displayed after each round
- Shows all dice rolls and decisions

### 2. `zonk_demo_non_interactive.py` (Demo)
A non-interactive demo that runs automatically without user input.

**How to run:**

From project root:
```bash
python project/game/examples/zonk_demo_non_interactive.py
```

Or as a module:
```bash
python -m project.game.examples.zonk_demo_non_interactive
```

**Features:**
- Faster demonstration (target: 2000 points)
- No user input required
- Good for quick testing and demonstration
- Shows complete game flow

## Game Rules

**Zonk** is a dice game where players try to reach the target score by rolling 6 dice.

### Scoring:
- Single 1 = 100 points
- Single 5 = 50 points
- Three of a kind:
  - Three 1s = 1000 points
  - Three 2s = 200 points
  - Three 3s = 300 points
  - Three 4s = 400 points
  - Three 5s = 500 points
  - Three 6s = 600 points
- Straight (1-2-3-4-5-6) = 1500 points
- Three pairs = 750 points

### Gameplay:
- Players take turns rolling dice
- After each roll, keep at least one scoring die
- Can continue rolling remaining dice or bank the score
- If no scoring dice appear, it's a "Zonk" - lose all round points
- If all 6 dice score, get to roll all 6 again

## Bot Strategies

### ConservativeBot
- Banks after reaching 350 points
- Stops rolling with 2 or fewer dice
- Always keeps all scoring dice
- Plays it safe

### AggressiveBot
- Banks only after 600 points
- Continues rolling even with few dice
- Keeps minimum scoring dice to maximize rerolls
- Takes more risks

### BalancedBot
- Banks after 450 points
- Adapts to game situation
- Balances risk and reward
- More conservative when close to winning
