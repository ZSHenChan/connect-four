import numpy as np
import pygame
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW = 6
COLUMN = 7


def create_board():
    board = np.zeros((ROW, COLUMN))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_position(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW-1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN-3):
        for r in range(ROW):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN):
        for r in range(ROW-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN-3):
        for r in range(ROW-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN-3):
        for r in range(3, ROW):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r *
                             SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 0:
                pygame.draw.circle(
                    screen, BLACK, (c*SQUARE_SIZE+RADIUS, r*SQUARE_SIZE+SQUARE_SIZE+RADIUS), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(
                    screen, RED, (c*SQUARE_SIZE+RADIUS, r*SQUARE_SIZE+SQUARE_SIZE+RADIUS), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen, YELLOW, (c*SQUARE_SIZE+RADIUS, r*SQUARE_SIZE+SQUARE_SIZE+RADIUS), RADIUS)
    pygame.display.update()


def draw_circle_on_mouse(event):
    posx = event.pos[0]
    if turn == 0:
        pygame.draw.circle(
            screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
    elif turn == 1:
        pygame.draw.circle(
            screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
running = True
turn = 0

pygame.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2)-5

width = COLUMN*SQUARE_SIZE
height = (ROW+1)*SQUARE_SIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

winning_font = pygame.font.SysFont("monospace", 75)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            draw_circle_on_mouse(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(board)
            if turn == 0:
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(math.floor(posx/SQUARE_SIZE))
                row = int(math.floor(posy/SQUARE_SIZE))
                if is_valid_position(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    print(board)
                    if winning_move(board, 1):
                        winning_label = winning_font.render(
                            "Player 1 Won!!", 1, RED)
                        screen.blit(winning_label, (30, 10))
                        running = False

            else:
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(math.floor(posx/SQUARE_SIZE))
                row = int(math.floor(posy/SQUARE_SIZE))
                if is_valid_position(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    print(board)
                    if winning_move(board, 2):
                        winning_label = winning_font.render(
                            "Player 2 Won!!", 1, YELLOW)
                        screen.blit(winning_label, (30, 10))
                        running = False

            turn = (turn+1) % 2
            draw_board(board)
            draw_circle_on_mouse(event)
