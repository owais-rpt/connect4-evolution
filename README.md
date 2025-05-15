Demo Video:
https://drive.google.com/file/d/1t4b_LHIBsvNm7IQQMyDaqQ_5pKCBF6u-/view?usp=drive_link

Project Report: Connect Four Game (Human vs Human, Human vs AI)

1. Introduction

The "Connect Four" game is a two-player strategy board game, where players take turns dropping discs into a grid, attempting to align four of their discs either horizontally, vertically, or diagonally. This project involves building a variation of the game in Python, using the Pygame library, and incorporating both a Human vs Human and Human vs AI mode.

The AI component of this game uses the Minimax algorithm with Alpha-Beta pruning to make strategic moves and challenge the player. The game logic is structured to accommodate multiple turns and victory conditions.

2. Objective

The objective of this project was to:

1. Develop a working version of the Connect Four game with the ability to switch between Human vs Human and Human vs AI modes.
2. Implement the Minimax algorithm to control the AI's decision-making in a way that mimics strategic gameplay.
3. Use Pygame for the graphical interface, allowing an interactive and visually appealing user experience.

3. System Design

3.1 Board Representation

- The game board is represented as a 2D array (numpy.zeros()) of size 6x7, representing the grid of the game.
- Each cell in the array holds a value:
  - 0 represents an empty space.
  - 1 represents Player 1’s piece (Red).
  - 2 represents Player 2’s piece (Yellow).
  - 3 represents the AI's piece (Green).

3.2 Modes of Play

- Human vs Human: Both players take turns selecting columns to drop their pieces. The game ends when a player wins or the grid is full.
  
- Human vs AI: The player competes against the AI. The AI makes decisions based on the Minimax algorithm, maximizing its chances of winning while minimizing the player's opportunities.

4. Core Logic

4.1 Board Creation and Manipulation

- create_board(): Initializes a 6x7 grid with all cells set to 0.
- drop_piece(): Places a piece on the board at the given row and column.
- is_valid_location(): Checks if a column is available for dropping a piece.
- get_next_open_row(): Returns the next available row in a column for dropping a piece.

4.2 Win Condition

The game checks for a winning move using the winning_move() function, which checks for four connected pieces in horizontal, vertical, and diagonal directions.

4.3 AI Decision Making

The AI uses the Minimax algorithm with Alpha-Beta pruning to evaluate the best possible move. The AI’s moves are calculated by:
  
1. Evaluating the current board position.
2. Simulating all possible future moves and recursively evaluating the board state.
3. Using Alpha-Beta pruning to cut off branches of the tree that won’t be explored, improving efficiency.

5. Graphical User Interface (GUI)

The Pygame library was used to create the graphical interface, making the game interactive. The interface includes:
  
- A grid where players can drop their pieces.
- Player piece colors: Red for Player 1, Yellow for Player 2, and Green for the AI.
- Displaying game-over messages when a player wins or the board is full.

6. Algorithm: Minimax with Alpha-Beta Pruning

The AI's strategy is based on the Minimax algorithm, which simulates all possible future moves in a game and selects the one that leads to the best outcome for the AI. Alpha-Beta pruning optimizes this process by eliminating branches of the decision tree that do not need to be explored.

Minimax Algorithm:
- The algorithm considers two players: one trying to maximize the score (AI) and one trying to minimize it (the player).
- The AI chooses the move that maximizes its score, while the player tries to minimize the AI's score.

Alpha-Beta Pruning:
- A technique used to cut off unnecessary branches in the Minimax tree.
- It helps speed up the search by eliminating moves that are already known to be worse than other options.

7. Challenges

- AI Difficulty: Initially, the AI was too predictable, but the use of Minimax with Alpha-Beta pruning made it significantly more challenging.
- UI Interactivity: Ensuring that the graphical interface was responsive and reflected the current game state took some time to fine-tune, particularly during transitions between player turns.

8. Conclusion

The project was successful in creating an interactive, functional version of Connect Four with both Human vs Human and Human vs AI modes. The use of the Minimax algorithm for the AI provided a competitive experience for the player, and the Pygame library allowed for smooth and visually appealing gameplay.

9. Future Enhancements

- Difficulty Levels: The AI could be enhanced with different difficulty levels, where the depth of the Minimax algorithm varies based on the selected difficulty.
- Multiplayer Online Mode: Implementing an online mode to allow players to compete against others over the internet.
