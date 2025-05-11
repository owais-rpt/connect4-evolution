import numpy as np
import random
import pygame
import sys
import math

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# RGB Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAYER1 = 0  # Human 1 (Red)
PLAYER2 = 1  # Human 2 (Yellow)
AI = 2       # AI (Green)

PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
AI_PIECE = 3

WINDOW_LENGTH = 4
DEPTH = 4  # Minimax depth

pygame.init()
myfont = pygame.font.SysFont("monospace", 75)
screen = pygame.display.set_mode(size)

# Board banane ka function
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Piece drop karne ka function
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check karna agar column valid hai ya nahi
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Next open row find karna
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Board print karna
def print_board(board):
    print(np.flip(board, 0))

# Winning move check karna
def winning_move(board, piece):
    # Horizontal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True

    # Diagonal / check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    # Diagonal \ check
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    return False

# Board draw karna
def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            piece = board[r][c]
            if piece == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif piece == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif piece == 3:
                pygame.draw.circle(screen, GREEN, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

# Window score evaluate karna (Minimax ke liye)
def evaluate_window(window, piece):
    score = 0
    opp_pieces = [PLAYER1_PIECE, PLAYER2_PIECE]
    if piece in opp_pieces:
        opp_pieces.remove(piece)

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    for opp in opp_pieces:
        if window.count(opp) == 3 and window.count(0) == 1:
            score -= 4

    return score

# Score position ke liye calculate karna
def score_position(board, piece):
    score = 0

    # Center column ka score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    score += center_array.count(piece) * 3

    # Horizontal check
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical check
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Diagonal check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Valid columns find karna
def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

# Check karna agar game over ho gaya hai
def is_terminal_node(board):
    return winning_move(board, PLAYER1_PIECE) or winning_move(board, PLAYER2_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1e6)
            elif winning_move(board, PLAYER1_PIECE) or winning_move(board, PLAYER2_PIECE):
                return (None, -1e6)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, random.choice([PLAYER1_PIECE, PLAYER2_PIECE]))
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Game start hone ka logic
board = create_board()
print_board(board)
game_over = False
draw_board(board)

turns = [PLAYER1, AI, PLAYER2]
random.shuffle(turns)
turn_index = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turns[turn_index] == PLAYER1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            elif turns[turn_index] == PLAYER2:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turns[turn_index] in [PLAYER1, PLAYER2]:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    piece = PLAYER1_PIECE if turns[turn_index] == PLAYER1 else PLAYER2_PIECE
                    drop_piece(board, row, col, piece)

                    if winning_move(board, piece):
                        label = myfont.render(f"Player {piece} wins!", 1, RED if piece == PLAYER1_PIECE else YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn_index = (turn_index + 1) % 3
                    draw_board(board)

    if turns[turn_index] == AI and not game_over:
        col, minimax_score = minimax(board, DEPTH, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("AI wins!", 1, GREEN)
                screen.blit(label, (40, 10))
                game_over = True

            turn_index = (turn_index + 1) % 3
            draw_board(board)

    if game_over:
        pygame.time.wait(3000)
