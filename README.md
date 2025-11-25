# GigaGigus - Gigaverse Combat Calculator

A PyQt5-based calculator tool for determining optimal combat moves in [Gigaverse](https://glhfers.gitbook.io/gigaverse/combat/dungetron-overview/dungetron-5000-normal)'s Dungetron 5000 combat system.

## About Gigaverse

Gigaverse is a rogue-lite style combat dungeon game where players battle through increasingly difficult enemies across multiple floors. The combat system features a rock-paper-scissors style mechanic with three skills:

- **Sword** counters **Spell**
- **Spell** counters **Shield**
- **Shield** counters **Sword**

When you win a matchup, you deal damage to the enemy and can repair your shield. Players must strategically choose their moves to maximize damage while minimizing losses.

## What This Tool Does

GigaGigus calculates the **Expected Value (EV)** of each possible combat action, helping you make optimal decisions during Dungetron battles. The calculator considers:

- **Attack (ATK)**: Damage dealt to opponent
- **Defense (DEF)**: Shield recovery amount
- **Stamina**: Available uses for each skill (0-3)
- **HP & Shield**: Current and maximum values for both characters
- **Matchup Results**: Rock-paper-scissors outcomes affecting which actions apply

### EV Calculation

The tool calculates EV using the formula:

```
EV = (Enemy HP Lost + Enemy Shield Lost) - (My HP Lost + My Shield Lost)
```

This accounts for both offensive and defensive outcomes, giving you a net value for each possible action.

## Features

- ✅ **Real-time EV Calculation**: Instantly compute the best move based on current stats
- ✅ **Detailed Breakdown**: View all possible enemy responses with probabilities
- ✅ **Matchup Analysis**: See WIN/LOSE/DRAW outcomes for each scenario
- ✅ **Shield Cap Enforcement**: Respects maximum shield limits during recovery
- ✅ **Stamina Tracking**: Only shows moves with available stamina
- ✅ **Comprehensive Display**: Shows HP/Shield changes for all outcomes

## Installation

### Requirements

- Python 3.6+
- PyQt5

### Setup

```bash
# Install dependencies
pip install PyQt5

# Run the application
python gui.py
```

## How to Use

1. **Enter Your Stats**:
   - Set HP (current/max)
   - Set Shield (current/max)
   - Configure each skill's ATK, DEF, and Stamina

2. **Enter Enemy Stats**:
   - Same configuration as your stats
   - Input enemy's current HP/Shield and skill attributes

3. **Calculate**:
   - Click "Calculate Best Move"
   - View the optimal skill and its expected value
   - Review detailed breakdown of all possible outcomes

## Combat Mechanics

### Matchup Rules

- **WIN**: Only your attack damages enemy + only your shield recovers
- **LOSE**: Only enemy attack damages you + only enemy shield recovers
- **DRAW**: Both attacks and shields apply simultaneously

### Damage Application

1. Damage is applied to shield first
2. Excess damage carries over to HP
3. Shield recovery is capped at maximum shield value

### Stamina System

Each skill has stamina ranging from 0-3:
- **3**: Fully available
- **2**: Two uses remaining
- **1**: One use remaining
- **0**: Cannot use this skill

## Example Calculation

**Scenario**: Both players at 10 HP, 10 Shield (max), choosing SWORD

```
Case 1: Enemy uses SWORD = DRAW
  My Lost: HP=0, Shield=4 (Total: 4)
  Enemy Lost: HP=0, Shield=4 (Total: 4)
  Net Value: 0
  Contribution: 0 × 33.33% = 0.00

Case 2: Enemy uses SHIELD ✗ LOSE
  My Lost: HP=90, Shield=10 (Total: 100)
  Enemy Lost: HP=0, Shield=0 (Total: 0)
  Net Value: -100
  Contribution: -100 × 33.33% = -33.33

Case 3: Enemy uses SPELL ✓ WIN
  My Lost: HP=0, Shield=0 (Total: 0)
  Enemy Lost: HP=0, Shield=4 (Total: 4)
  Net Value: +4
  Contribution: +4 × 33.33% = +1.33

Total EV: -32.00
```

## Files

- `gui.py`: PyQt5 user interface
- `main_logic.py`: Core calculation logic and combat mechanics
- `README.md`: This file

## Contributing

Feel free to submit issues or pull requests to improve the calculator!

## Links

- [Gigaverse Official Site](https://gigaverse.io)
- [Gigaverse Documentation](https://glhfers.gitbook.io/gigaverse)
- [Dungetron 5000 Guide](https://glhfers.gitbook.io/gigaverse/combat/dungetron-overview/dungetron-5000-normal)

## License

This is an unofficial fan-made tool for Gigaverse players. Not affiliated with the official Gigaverse team.

---

**Good luck in the Dungetron!** 🗡️🛡️✨
