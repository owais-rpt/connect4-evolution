import numpy as np
import pygame
import sys
import math

# Colors define karte hain
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

# Board banane ka function
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Piece drop karne ka function
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check karte hain ke location valid hai ya nahi
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Next open row dhundhne ka function
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Board ko print karne ka function
def print_board(board):
    print(np.flip(board, 0))

# Winning condition check karte hain
def winning_move(board, piece):
    # Horizontal check
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive slope diagonal check
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative slope diagonal check
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Board ko draw karte hain
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))  # Rectangles draw karna
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)  # Circles draw karna

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):  # Agar board ke kisi spot par piece hai toh uska color draw karna
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Game ka start setup
board = create_board()
print_board(board)
game_over = False
turn = 0  # Player 1 ka turn first

pygame.init()

# Square aur screen ke size set karte hain
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)  # Game window banate hain
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)  # Font for displaying winning message

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Mouse ke movement par rectangle draw karna
            posx = event.pos[0]
            if turn == 0:  # Player 1 ke liye
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:  # Player 2 ke liye
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Mouse click ke baad black rectangle draw karte hain
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))  # Column ke according position calculate karte hain

            if turn == 0:  # Player 1 ka turn
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):  # Player 1 ne jeet liya
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            else:  # Player 2 ka turn
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):  # Player 2 ne jeet liya
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)  # Board print karte hain
            draw_board(board)  # Board draw karte hain

            turn += 1
            turn = turn % 2  # Alternate turns for player 1 and player 2

            if game_over:
                pygame.time.wait(3000)  # Game khatam hone ke baad wait time
