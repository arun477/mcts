# Tic-Tac-Toe with Monte Carlo Tree Search

This project implements a Tic-Tac-Toe game with an Monte Carlo Tree Search opponent using the Monte Carlo Tree Search (MCTS) algorithm. The game features a graphical user interface built with Pygame, allowing human players to compete against the Monte Carlo Tree Search.


## Game Board
<img src="https://github.com/user-attachments/assets/eab0d191-60db-4b21-9701-77f6ec68474a" alt="Game Board" width="300">

## Terminal Output
<img src="https://github.com/user-attachments/assets/bc6eb7c8-5956-4a42-b5f7-ae6e850f843f" alt="Terminal Output" width="600">

## Board Scores
<img src="https://github.com/user-attachments/assets/07fa9522-ccc7-48c4-be5b-b0e683d99695" alt="Board Scores" width="600">


## Features

- Tic-Tac-Toe game implementation
- Monte Carlo Tree Search
- Pygame-based graphical user interface
- Visual representation of Monte Carlo Tree Search's move evaluation

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- Pygame
- PySpiel

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

```
pip install numpy matplotlib pygame open_spiel
```

## Usage

To start the game, run the main script:

```
python main.py
```

The game will open in a Pygame window. The human player is 'O', and the Monte Carlo Tree Search is 'X'. Click on an empty cell to make your move. The Monte Carlo Tree Search will automatically make its move after you.

## Files

- `mcts.py`: Implementation of the Monte Carlo Tree Search algorithm
- `gui.py`: Pygame-based graphical user interface
- `main.py`: Main game loop and integration of MCTS with GUI

## How it Works

1. The game starts with an empty 3x3 grid.
2. Players take turns placing their symbol ('O' for human, 'X' for Monte Carlo Tree Search) in empty cells.
3. The Monte Carlo Tree Search uses MCTS to evaluate possible moves and choose the best one.
4. After each Monte Carlo Tree Search move, a heatmap is displayed showing the Monte Carlo Tree Search's evaluation of different positions.
5. The game ends when a player wins or the board is full (draw).

## Monte Carlo Tree Search

The Monte Carlo Tree Search uses MCTS to determine its moves:

1. Selection: Choose a promising leaf node in the game tree.
2. Expansion: Add child nodes to the selected node.
3. Simulation: Play out random games from the new nodes.
4. Backpropagation: Update node statistics based on simulation results.

The Monte Carlo Tree Search repeats this process for a set number of iterations before choosing the best move.

## Visualization

After each Monte Carlo Tree Search move, the program displays a heatmap showing the Monte Carlo Tree Search's evaluation of different board positions. Warmer colors (red) indicate moves the Monte Carlo Tree Search considers more favorable, while cooler colors (blue) represent less favorable moves.

## Contributing

For educational purposes and tinkering.

## License

This project is open-source and available under the MIT License.
