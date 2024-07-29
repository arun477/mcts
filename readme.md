# Tic-Tac-Toe with Monte Carlo Tree Search AI

This project implements a Tic-Tac-Toe game with an AI opponent using the Monte Carlo Tree Search (MCTS) algorithm. The game features a graphical user interface built with Pygame, allowing human players to compete against the AI.

## Features

- Tic-Tac-Toe game implementation
- Monte Carlo Tree Search AI
- Pygame-based graphical user interface
- Visual representation of AI's move evaluation

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

The game will open in a Pygame window. The human player is 'O', and the AI is 'X'. Click on an empty cell to make your move. The AI will automatically make its move after you.

## Files

- `mcts.py`: Implementation of the Monte Carlo Tree Search algorithm
- `gui.py`: Pygame-based graphical user interface
- `main.py`: Main game loop and integration of MCTS with GUI

## How it Works

1. The game starts with an empty 3x3 grid.
2. Players take turns placing their symbol ('O' for human, 'X' for AI) in empty cells.
3. The AI uses MCTS to evaluate possible moves and choose the best one.
4. After each AI move, a heatmap is displayed showing the AI's evaluation of different positions.
5. The game ends when a player wins or the board is full (draw).

## Monte Carlo Tree Search

The AI uses MCTS to determine its moves:

1. Selection: Choose a promising leaf node in the game tree.
2. Expansion: Add child nodes to the selected node.
3. Simulation: Play out random games from the new nodes.
4. Backpropagation: Update node statistics based on simulation results.

The AI repeats this process for a set number of iterations before choosing the best move.

## Visualization

After each AI move, the program displays a heatmap showing the AI's evaluation of different board positions. Warmer colors (red) indicate moves the AI considers more favorable, while cooler colors (blue) represent less favorable moves.

## Contributing

Contributions to improve the AI, enhance the GUI, or optimize the code are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open-source and available under the MIT License.
