# Quoridor AI

Quoridor AI is a Python implementation of the popular strategy board game **Quoridor**. The project includes game logic, a player-controlled interface, and a framework for creating AI agents to play the game. This is a great starting point for learning about pathfinding, game mechanics, and AI strategies.

## Features
- **Core Game Mechanics**: Fully implemented game logic, including wall placements and movement rules.
- **Path Validation**: Ensures players always have a valid path to their goal.
- **Player vs Player**: Play against another human.
- **Extendable AI**: Framework for developing and testing AI agents.
- **Unit Tests**: Comprehensive test suite using `pytest`.

---

## Installation

### Prerequisites
- Python 3.8 or higher

### Clone the Repository
```bash
git clone https://github.com/StMilica/Quoridor_AI.git
cd Quoridor_AI
```

### Create a Virtual Environment
Set up a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Usage

### Run the Game
You can run the game directly from the command line:

```bash
python main.py
```

### Run Unit Tests
To verify the functionality of the game, run the test suite:

```bash
pytest
```

---

## Project Structure
```plaintext
quoridor_ai/
├── quoridor/             # Main package
│   ├── src/              # Source code
│   │   ├── __init__.py   
│   │   ├── board.py      # Board logic
│   │   ├── player.py     # Player class
│   │   └── game.py       # Game controller
├── tests/                # Unit tests
│   ├── test_board.py     # Board tests
│   ├── test_player.py    # Player tests
│   └── test_game.py      # Game tests
├── .gitignore            # Ignore unnecessary files
├── requirements.txt      # Dependencies
├── pytest.ini            # pytest configuration
├── README.md             # Documentation
└── LICENSE               # License information
```

---

## How to Contribute
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Inspired by the classic **Quoridor** board game.
- Thanks to all contributors and the open-source community!
