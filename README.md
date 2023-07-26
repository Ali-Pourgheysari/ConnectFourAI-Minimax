# Connect Four AI Player using Minimax Algorithm
 This is a Python script that implements an AI player for the game Connect Four using the Minimax algorithm with alpha-beta pruning. The AI player makes optimal moves by searching through the game tree up to a certain depth and choosing the move that maximizes its chances of winning.

 ## Dependencies
 The script uses the following libraries:

* `pettingzoo`: A Python library for multi-agent
* `reinforcement` learning environments, which includes the Connect Four environment.
* `numpy`: A library for numerical computing in Python.
* `time`: A module for time-related functions.
* `copy`: A module for creating deep copies of objects.

Make sure you have these libraries installed before running the code.

## How to Use
1. First, make sure you have the necessary libraries installed.
2. Import the required libraries and set the maximum depth for the Minimax search (maxdepth).
3. Create the Connect Four environment and reset it.
4. Implement utility functions:
    * `count_sublists(lst)`: Counts the number of sublists of 1s in a given list.
    * `get_material_score(observation, player, terminate=False)`: Calculates the material score for a given player's observation.
    * `heuristic(observation, player)`: Implements the heuristic function to evaluate the board state for a player.
    * `possible_moves(observation)`: Generates all possible legal moves for a given observation.
    * `make_move(observation, move, player)`: Makes a move on the board and returns the updated observation.
    * `undo_move(observation, move, player)`: Undoes a move on the board and returns the previous observation.
5. Implement the Minimax algorithm:
    * `minimax(observation, depth, termination, truncation, maximize_player, alpha, beta)`: Implements the Minimax algorithm with alpha-beta pruning.
6. Play the game:
    * The AI player ('player_0') and the human player ('player_1') take turns making moves until the game terminates.
    * The AI player uses the Minimax algorithm to choose its moves, and the human player can input their move from 0 to 6 (column number).

## How the AI Player Works
The AI player uses the Minimax algorithm with alpha-beta pruning to find the best move that maximizes its chances of winning. It considers a certain depth of the game tree and evaluates each possible move using a heuristic function based on the material score of the board state.

The material score is calculated by counting the number of 2s, 3s, and 4s (continuous pieces of the AI player) in each row, column, diagonal, and anti-diagonal. The AI player aims to maximize its material score while minimizing the opponent's material score.

The AI player uses the minimax function to explore the game tree and choose the best move. It considers both maximizing and minimizing scenarios (for itself and the opponent) at each level of the tree and applies alpha-beta pruning to speed up the search.

## Playing the Game
The game is played on a 7x6 grid, and the columns are numbered from 0 to 6. The AI player ('player_0') and the human player ('player_1') take turns making moves. The AI player uses the Minimax algorithm to choose its moves, and the human player can input their move from 0 to 6.

The game continues until one player wins or the board is full (draw). If the AI player wins, the program prints "Player 0 wins!" and if the human player wins, it prints "Player 1 wins!" The program also handles the case when a player resigns from the game.

 Read the complete documentation [HERE](Documentation.pdf).
Also you can read [THIS](Code_review.pdf) code review for more details about the code.

Enjoy playing Connect Four against the AI player! 🤖