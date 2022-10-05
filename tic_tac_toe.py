import pygame
from pygame.locals import *
import math
import sys

"""
VAI project
Petr Šemora, 4pAIŘ/1
Tic Tac Toe with alpha-beta pruning in pygame
"""
# init pygame
pygame.init()

# variables 
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height+100))
line_width = 5
margin = 10
window_width = screen_width - margin * 2
window_height = screen_height - margin * 2
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

xMark = 'X'
oMark = 'O'

pygame.display.set_caption('Tic Tac Toe')
font = pygame.font.SysFont('ubuntumono', 120, False, False)
xText = font.render(xMark, True, blue)
oText = font.render(oMark, True, green)
winFont = pygame.font.SysFont('ubuntumono', 80, False, False)
endFont = pygame.font.Font('freesansbold.ttf', 32)
x_win = winFont.render('Player X win', True, red)
o_win = winFont.render('Player O win', True, red)
drawText = winFont.render('      Draw', True, red)
play_again = endFont.render('Play again', True, red, yellow)
cancel = endFont.render('End Game', True, red, yellow)
text_x = endFont.render("Player: X ", True, white) 
text_o = endFont.render("AI: O ", True, white)

X_MOVES = []
O_MOVES = []

Player_X = 1
Player_O = -1
EMPTY = 0

grid = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

def winning_states(grid, player):
    # possible moves to win the game
    ws = [[grid[0][0], grid[0][1], grid[0][2]],
          [grid[1][0], grid[1][1], grid[1][2]],
          [grid[2][0], grid[2][1], grid[2][2]],
          [grid[0][0], grid[1][0], grid[2][0]],
          [grid[0][1], grid[1][1], grid[2][1]],
          [grid[0][2], grid[1][2], grid[2][2]],
          [grid[0][0], grid[1][1], grid[2][2]],
          [grid[0][2], grid[1][1], grid[2][0]]]

    if [player, player, player] in ws:
        return True
    else:
        return False

def win_game(grid):
    # return winner of the game
    return winning_states(grid, Player_X) or winning_states(grid, Player_O)

def is_draw(grid):
    # return TRUE if the game is draw 
    if len(empty_cells(grid)) == 0 and (not winning_states(grid, Player_X) or not winning_states(grid, Player_O)):
        return True
    else:
        return False

def is_game_over(grid):
    # return TRUE if user / AI win the game or game is draw  
    if winning_states(grid, Player_X) or winning_states(grid, Player_O) or is_draw(grid):
        return True
    else:
        return False

def empty_cells(grid):
    # return empty cells of grid 
    empty_cell = []
    for x, row in enumerate(grid):
        for y, col in enumerate(row):
            if grid[x][y] == EMPTY:
                empty_cell.append([x, y])
    return empty_cell

def set_move(grid, x, y, player):
    # set player or AI to empty cell 
    grid[x][y] = player

def evaluation(grid):
    # return evaluation for AI move 
    if winning_states(grid, Player_X):
        return 1
    elif winning_states(grid, Player_O):
        return -1
    else:
        return 0

def ABpruning(grid, depth, alpha, beta, player):
    # alpha-beta pruning - return row and col of AI move 
    row = 0
    col = 0
    if depth == 0 or win_game(grid):
        return [row, col, evaluation(grid)]
    else:
        for cell in empty_cells(grid):
            set_move(grid, cell[0], cell[1], player)
            score = ABpruning(grid, depth - 1, alpha, beta, -player)
            if player == Player_X and score[2] > alpha:
                alpha = score[2]
                row = cell[0]
                col = cell[1]
            elif player == Player_O and score[2] < beta:
                beta = score[2]
                row = cell[0]
                col = cell[1]

            set_move(grid, cell[0], cell[1], EMPTY) 

            if alpha >= beta:
                break

        if player == Player_X:
            return [row, col, alpha]
        else:
            return [row, col, beta]


def main_game(row, col, grid):
    # main game - append user click and best AI move 
    x_move = (row, col)
    X_MOVES.append(x_move)
    set_move(grid, row, col, Player_X)
    if not winning_states(grid, Player_X) and not is_draw(grid):
        o_move = ABpruning(grid, len(empty_cells(grid)), -math.inf, math.inf, Player_O)
        set_move(grid, o_move[0], o_move[1], Player_O)
        O_MOVES.append((o_move[0], o_move[1]))
    print_mark(screen, xText, oText)

def draw_line(screen):
    screen.fill(white)
    # draw horizontal line
    pygame.draw.line(screen, black, (margin, window_height / 3 + margin), (screen_width - margin, window_height / 3 + margin), line_width)
    pygame.draw.line(screen, black, (margin, window_height / 3 * 2 + margin), (screen_width - margin, window_height / 3 * 2 + margin), line_width)

    # draw vertical lines
    pygame.draw.line(screen, black, (window_width / 3 + margin, margin), (window_width / 3 + margin, screen_height - margin), line_width)
    pygame.draw.line(screen, black, (window_width / 3 * 2 + margin, margin), (window_width / 3 * 2 + margin, screen_height - margin), line_width)
    pygame.display.update()


def show_info():
    # show rectangle with simple info
    screen.fill (black, (0, 400, 500, 100))
    screen.blit(text_x, (40,440))
    screen.blit(text_o, (240,440))

def get_position():
    # row calculation of user click 
    x, y = pygame.mouse.get_pos() 

    if y < window_height / 3:
        row = 0
    elif y > window_height / 3 and y < window_height / 3 * 2:
        row = 1
    elif y > window_height / 3 * 2:
        row = 2
    else: 
        row = None
    
    # column calculation of user click 
    if x < window_width / 3:
        col = 0
    elif x > window_width / 3 and x < window_width / 3 * 2:
        col = 1
    elif x > window_width / 3 * 2:
        col = 2
    else:
        col = None
    user_click(row,col)


def print_position(row, col):
    # return position of mark to print 
    return margin + window_width / 3 * col + 35, margin + window_height / 3 * row + 25

def print_mark(screen, xText, oText):
    # print mark on board 
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == Player_X:
                screen.blit(xText, (print_position(row, col)))
            elif grid[row][col] == Player_O:
                screen.blit(oText, (print_position(row, col)))
    pygame.display.update() 
    check_win()

def check_win():
    # check user / AI win or draw 
    if winning_states(grid, Player_O):
        screen.blit(o_win, (screen_width * 0.1, screen_height * 0.4))
    elif winning_states(grid, Player_X):
        screen.blit(x_win, (screen_width * 0.1, screen_height * 0.4))   
    elif is_draw(grid):
        screen.blit(drawText, (screen_width * 0.1, screen_height * 0.4))
  
def user_click(row,col):
    # check user click, user can click only in empty cell 
    if (row,col) in X_MOVES  or (row,col) in O_MOVES:
        return
    elif winning_states(grid, Player_X) or winning_states(grid, Player_O) or is_draw(grid):
        return
    else:
        main_game(row, col, grid)

def reset_game():
    # reset variables and play again
    X_MOVES .clear()
    O_MOVES.clear()  
    grid[:] = [[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]
    pygame.display.update()
    game_loop() 
    

def game_loop(): 
    fps = 10
    clock = pygame.time.Clock()
    draw_line(screen)
    show_info()
    
    while(True): 
        # main loop
        for event in pygame.event.get(): 
            if event.type is QUIT: 
                pygame.quit()
                sys.exit() 
            elif event.type is MOUSEBUTTONDOWN:
                # user click
                get_position()
            if is_game_over(grid):
                btn_play_again = screen.blit(play_again, (20, 250))
                btn_cancel = screen.blit(cancel,(220, 250))
                if event.type == pygame.MOUSEBUTTONDOWN and btn_play_again.collidepoint(event.pos):
                    # click on button "play again" and reset game
                    reset_game()
                if event.type == pygame.MOUSEBUTTONDOWN and btn_cancel.collidepoint(event.pos):
                    # click on button "cancel" and end game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(fps)   

if __name__ == "__main__":
    game_loop()