#!/usr/bin/env python3

import curses
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_RESIZE
from random import randint
from curses import wrapper
import signal


class Tetro(object):

    def __init__(self, height, width, x, y, MAX_X, MAX_Y, window):
        self.last_item = []
        self.score = 0
        self.timeout = 100
        self.start_x = width // 4
        self.start_y = 2
        self.x = x
        self.y = y
        self.max_x = MAX_X
        self.max_y = MAX_Y
        self.char = '🍳'
        self.window = window
        self.direction = KEY_DOWN
        self.direction_map = {
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }

    @property
    def count_score(self):
        return 'Score: {}'.format(self.score)

    def update(self):
        self.direction_map[self.direction]()

    def change_direction(self, direction):
        self.direction = direction

    def render(self):
        self.window.addstr(self.y, self.x, self.char, curses.color_pair(1))

    '''
    em di ngu 1 ti nha
    anh choi game nghe nhac gi di dung lam nua k em theo k kip mat hehe
    '''

    def move_down(self):
        if self.y < self.max_y:
            self.y += 1
        else:
            self.last_item.append((self.x, self.y))
            # self.x = self.start_x
            # self.y = self.start_y

    def move_left(self):
        self.x -= 1
        if self.x < 1:
            self.x = 1

    def move_right(self):
        self.x += 1
        if self.x > self.max_x:
            self.x = self.max_x

class TetrisWindow:
    def __init__(self):
        self.stdscr = curses.initscr()
        # Initialize values
        self.HEIGHT, self.WIDTH = self.stdscr.getmaxyx()
        self.MAX_X = self.WIDTH // 2 - 1
        self.MAX_Y = self.HEIGHT - 2
        self.START_X = self.WIDTH // 4
        self.START_Y = 2

    def draw_UI(self, stdscr):

        key = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # set color for later use
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        # block the window from reading in millisecond
        stdscr.timeout(100)

        #Hide the cursor
        curses.curs_set(0)

        
        while key != ord('q'):
            stdscr.clear()
            tetro = Tetro(self.HEIGHT, self.WIDTH, self.START_X, self.START_Y,
                          self.MAX_X, self.MAX_Y, stdscr)

            tetro.render()
            stdscr.border(0)
            #draw the split and score
            for i in range(1, self.HEIGHT - 1):
                stdscr.addstr(i, self.WIDTH // 2, "||", curses.color_pair(1))

            stdscr.addstr(self.HEIGHT // 2, self.WIDTH // 2 + self.WIDTH // 4, tetro.count_score, curses.color_pair(0))

            # append key and make move
            if key in [KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                tetro.change_direction(key)
            tetro.update()
            # tetro.direction = KEY_DOWN
            self.START_X = tetro.x
            self.START_Y = tetro.y
            #draw the TETRO in its current position
            # tetro.render()
            
            stdscr.refresh()
            key = stdscr.getch()

    def initializeWin(self):
        signal.signal(signal.SIGWINCH, signal.SIG_IGN)
        wrapper(self.draw_UI)


if __name__ == '__main__':
    wd = TetrisWindow()
    wd.initializeWin()
