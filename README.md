# 🧠 Lemming Game

A lightweight multi-agent coordination environment in a 2D maze. Agents ("lemmings") must navigate through obstacles and reach the goal cell **together** — with rules for movement, collisions, and rewards.

---

## 🚀 Features

- 10×10 handcrafted mazes
- Multi-agent support (configurable number of lemmings)
- Movement constrained by walls, bounds, and collision rules
- Truncation and termination support
- ASCII-based terminal rendering
- Gym-like API (`reset()`, `step()`, `render()`)
- Pluggable maze bank (`MAZE_BANK`)
- Sample random action simulator (`sample_actions()`)

---

## 📦 Installation

Make sure you have Python 3.7+ and `pip`:

```bash
pip install -e .
```
---

## File Structure
```yaml
lemming_game/
│
├── enviornment.py      # Contains Maze, Lemming, and Game classes
├── __init__.py         # Exports Game and MAZE_BANK
├── examples/
│   └── game.py         # Random action simulation runner
├── setup.py            # Project metadata and install config
├── requirements.txt    # Runtime dependencies
└── README.md           # This file
```
---
## Example Run
```bash
python examples/game.py
```
---
## Maze Bank
| Key          | Description                             |
| ------------ | --------------------------------------- |
| `simple`     | Wide open layout with two main paths    |
| `bottleneck` | Narrow central corridor, collision risk |
| `open_trap`  | Open-looking layout with internal traps |

Use it like this:
```bash
from lemming_game import Game, MAZE_BANK
game = Game(maze=MAZE_BANK["bottleneck"])
```
---
## Version History
### v0.1.0 – Initial Release:
- Game logic with two lemmings
- Static 10x10 maze with walls and a goal
- Collision detection & reward structure
- Terminal-based rendering
- Random action runner
- Maze bank with three handcrafted layouts
---
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.