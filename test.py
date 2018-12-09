#!/usr/bin/env python3

import curses
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from curses import wrapper
import signal


class Tetro:
    def __init__(self):
        self.shape = [[1]]
        self.size = [1, 1]

class TetrisBoard:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = self.new_board()

        self.current_block_pos = None
        self.block = None
        self.next_block = None

        self.game_over = False
        self.score = 0

    def start(self):
        self.board = self.new_board()

        self.current_block_pos = None
        self.block = None
        self.next_block = None

        self.game_over = False
        self.score = 0
        self.place_block()

    def new_board(self):
        new_board = []
        for row in range(self.height):
            column = []
            for col in range(self.width):
                column.append(0)
            new_board.append(column)
        return new_board

    def place_block(self):
        self.block = Tetro()
        self.block_shape = self.block.shape
        self.block_size = self.block.size
        block_start_width = round(self.width / 2 - self.block_size[1] / 2)
        block_start_height = 0
        self.current_block_pos = [block_start_height, block_start_width]

        if self.overlap(self.current_block_pos, self.block_shape):
            self.game_over = True

    def move_block(self, direction):
        pos = self.current_block_pos

        if direction == 'DOWN':
            new_position = [pos[0] + 1, pos[1]]
        elif direction == 'LEFT':
            new_position = [pos[0], pos[1] - 1]
        elif direction == 'RIGHT':
            new_position = [pos[0], pos[1] + 1]

        if self.can_move(new_position, self.block_shape):
            self.current_block_pos = new_position
        else:
            if direction == 'DOWN':
                self.land_block(pos, self.block_shape)
                self.del_row()
                self.place_block()

    def land_block(self, start_pos, block_shape):
        block_height = self.block_size[0]
        block_width = self.block_size[1]
        for row in range(block_height):
            for col in range(block_width):
                shape_element = block_shape[row][col]
                if shape_element is 1:
                    self.board[start_pos[0] + row][start_pos[1] + col] = 1

    def del_row(self):
        for row in range(self.height):
            if all(col == 1 for col in self.board[row]):
                for item in range(row, 0, -1):
                    self.board[item] = self.board[item - 1]
                temp = []
                for i in range(self.width):
                    temp.append(0)
                self.board[0] = temp
                self.score += 1

    def overlap(self, start_pos, block_shape):
        block_height = self.block_size[0]
        block_width = self.block_size[1]
        for row in range(block_height):
            for col in range(block_width):
                shape_element = block_shape[row][col]
                shape_element_on_board = self.board[start_pos[0] + row][start_pos[1] + col]
                if shape_element is 1 and \
                   shape_element == shape_element_on_board:
                    return True
        return False

    def can_move(self, pos, shape):
        size = self.block_size
        # if not reach the bottom yet
        if pos[1] + size[1] > self.width \
            or pos[0] + size[0] > self.height \
            or self.overlap(pos, shape):
            with open('texting', 'a+') as file:
                file.write(str(pos[1] + size[1]))
            return False
        return True

    def is_game_over(self):
        return self.game_over

class TetrisWindow:
    def __init__(self):

        tetris_window = curses.initscr()
        HEIGHT, WIDTH = tetris_window.getmaxyx()
        self.win_height = HEIGHT
        self.win_width = WIDTH
        self.board_width = WIDTH // 2
        self.board_height = HEIGHT - 2
        self.score_width = WIDTH // 2
        self.score_height = HEIGHT - 2

    def draw_tetris_window(self, tetris_window, tetris_board):
        tetris_window.border()

        # for i in range(1, self.win_height - 1):
        #     tetris_window.addstr(i, self.win_width // 2 + 1, "||")

        for row in range(self.board_height):
            for col in range(self.board_width):
                if tetris_board.board[row][col] == 1:
                    tetris_window.addstr(row + 1, 2*col + 1, "X")
                else:
                    tetris_window.addstr(row + 1, 2*col + 1, " ")

        for row in range(tetris_board.block.size[0]):
            for col in range(tetris_board.block.size[1]):

                if tetris_board.block.shape[col][row] == 1:
                    x = 2 * tetris_board.current_block_pos[1] + 2 * col + 1
                    y = tetris_board.current_block_pos[0] + row + 1
                    tetris_window.addstr(y, x, "🎁")

        if tetris_board.is_game_over():
            tetris_window.addstr(self.board_height // 2, self.board_width // 2, "GAME OVER", curses.A_BOLD)
            tetris_window.addstr(self.board_height // 2 + 1, self.board_width // 2, "IS THIS YOUR LIMIT?", curses.A_BOLD)
            tetris_window.refresh()

    def updating_score(self, score_window, tetris_board):
        score_window.addstr(self.score_height, self.score_width, "🎅 S C O R E : {} 🎄".format(tetris_board.score))
        score_window.refresh()

    def draw_UI(self, scr):
        signal.signal(signal.SIGWINCH, signal.SIG_IGN)
        tetris_board = TetrisBoard(self.board_height, self.board_width)

        tetris_window = curses.newwin(self.board_height, self.board_width)
        score_window = curses.newwin(self.score_height, self.score_width)

        tetris_board.start()

        old_score = tetris_board.score

        curses.curs_set(0)
        tetris_window.timeout(100)

        tetris_window.keypad(1)

        self.draw_tetris_window(tetris_window, tetris_board)
        self.updating_score(score_window, tetris_board)

        key = 0
        while key != ord('q'):
            key = tetris_window.getch()

            if not tetris_board.is_game_over():
                tetris_board.move_block('DOWN')

                if key == KEY_DOWN:
                    tetris_board.move_block('DOWN')
                elif key == KEY_LEFT:
                    tetris_board.move_block('LEFT')
                elif key == KEY_RIGHT:
                    tetris_board.move_block('RIGHT')
            else:
                tetris_window.timeout(-1)
                if key == ord('s'):
                    tetris_board.start()
                    tetris_board.timeout(100)

            self.draw_tetris_window(tetris_window, tetris_board)
            if not old_score is tetris_board.score:
                self.updating_score(score_window, tetris_board)
                old_score = tetris_board.score

        curses.endwin()

if __name__ == '__main__':
    tetrisWindow = TetrisWindow()
    wrapper(tetrisWindow.draw_UI)
