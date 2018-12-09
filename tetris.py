#!/usr/bin/env python3

import curses
import board
import time
from curses import wrapper
#
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

#
STATUS_WINDOW_HEIGHT = 7
STATUS_WINDOW_WIDTH = 40



#CHECK
def draw_game_window(window, game_board):
    """Draw game window"""

    window.border()

    # draw board
    for a in range(BOARD_HEIGHT):
        for b in range(BOARD_WIDTH):
            if game_board.board[a][b] == 1:
                window.addstr(a + 1, 2 * b + 1, "X")
            else:
                # draw net
                window.addstr(a + 1, 2 * b + 1, " ")

    # draw current block
    for a in range(game_board.current_block.size[0]):
        for b in range(game_board.current_block.size[1]):

            if game_board.current_block.shape[a][b] == 1:
                x = 2 * game_board.current_block_pos[1] + 2 * b + 1
                y = game_board.current_block_pos[0] + a + 1
                window.addstr(y, x, "X")

    if game_board.is_game_over():
        window.addstr(BOARD_HEIGHT//2, BOARD_WIDTH//2+1, "GAME OVER", curses.A_BOLD)
        window.addstr(BOARD_HEIGHT//2+2, 2, "IS THIS YOUR LIMIT?", curses.A_BOLD)
        window.refresh()

#CHECK
def draw_status_window(window, game_board):
    """Draw status window"""

    window.addstr(3, 1, "      🎅   SANTA GIVES YOU {} 🎄    ".format(game_board.score), curses.A_BOLD)

    window.refresh()
    # pass


def main(scr):
    game_board = board.Board(BOARD_HEIGHT, BOARD_WIDTH)
    game_board.start()

    old_score = game_board.score

    curses.curs_set(0)


    game_window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH)
    game_window.timeout(100)

    game_window.keypad(1)

    '''NOTE'''
    status_window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, BOARD_HEIGHT//2-2, BOARD_WIDTH+14)

    draw_game_window(game_window, game_board)
    draw_status_window(status_window, game_board)


    quit_game = False
    while not quit_game:
        key_event = game_window.getch()


        if key_event == curses.KEY_RESIZE:
            draw_game_window(game_window, game_board)

        if key_event == ord("q"):
            quit_game = True

        if not game_board.is_game_over():
            # if time.time() - start >= 1:
            game_board.move_block("down")
                # start = time.time()

            if key_event == curses.KEY_DOWN:
                game_board.move_block("down")
            elif key_event == curses.KEY_LEFT:
                game_board.move_block("left")
            elif key_event == curses.KEY_RIGHT:
                game_board.move_block("right")
        else:
            game_window.timeout(-1)
            if key_event == ord("\n"):
                game_board.start()
                game_window.nodelay(True)

        draw_game_window(game_window, game_board)
        if not old_score is game_board.score:
            draw_status_window(status_window, game_board)
            old_score = game_board.score
    curses.endwin()

if __name__ == "__main__":
    wrapper(main)
