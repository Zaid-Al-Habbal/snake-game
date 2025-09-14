# 🐍 Snake Game

A simple classic **Snake Game** built with Python and Pygame. The snake grows as it eats food, and the game ends if it collides with the wall or itself.

---

## 🚀 Features

* Snake moves smoothly across the grid
* Food spawns randomly
* Score counter
* Game Over screen with restart option

---

## 📦 Requirements

* Python 3.13+
* [uv](https://docs.astral.sh/uv/) for package management

---

## 🔧 Setup & Run

Clone the repository:

```bash
git clone https://github.com/your-username/snake-game.git
cd snake-game
```

Install dependencies:

```bash
uv sync
```

Run the game:

```bash
uv run python snake_game/main.py
```

---

## 🎮 Controls

* Arrow Keys → Move
* R → Restart after Game Over
* Esc → Quit

---

## 🛠 Build Executable

Package the game into a standalone executable:

```bash
uv run pyinstaller --onefile --windowed --name snake-game src/snake_game/main.py
```

Executable will be in the `dist/` folder.

---

## 🧪 Tests

Run logic tests:

```bash
uv run pytest
```
