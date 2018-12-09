#!/usr/bin/env python3
import curses
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_RESIZE
from random import randint
from curses import wrapper
import signal


# WIDTH = 35
# HEIGHT = 20


class Tetro(object):
    REV_DIR_MAP = {
    KEY_UP: KEY_DOWN
    }

    def __init__(self, x, y, MAX_X, MAX_Y, window):
        self.score = 0
        self.timeout = 100
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
        self.y += 1
        if self.y > self.max_y:
            self.y = self.max_y


    def move_left(self):
        self.x -= 1
        if self.x < 1:
            self.x = self.max_x

    def move_right(self):
        self.x += 1
        if self.x > self.max_x:
            self.x = 1

class TetrisWindow:
    def __init__(self):
        self.initializeWin()

    def handle_size(self):
        height, width = self.stdscr.getmaxyx()
        if height < 20 or width < 20:
            self.stdscr.clear()
            self.stdscr.addstr(height//2, width//2, 'TOO SMALL', curses.color_pair(1))
            self.stdscr.refresh()

    def draw_UI(self, stdscr):
        # signal.signal(signal.SIGWINCH, signal.SIG_IGN)

        key = 0
        self.stdscr = stdscr

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        self.HEIGHT, self.WIDTH = stdscr.getmaxyx()
        MAX_X = self.WIDTH // 2 - 1
        MAX_Y = self.HEIGHT - 2
        TETRO_X = self.WIDTH // 4
        TETRO_Y = 1

        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        stdscr.timeout(100)
        # turn off echoing to screen when pressing a button
        curses.noecho()
        # react instantly to key without enter
        curses.cbreak()
        # enable keypad mode to handle keys ourselves
        stdscr.keypad(True)
        curses.curs_set(0)

        tetro = Tetro(TETRO_X, TETRO_Y, MAX_X, MAX_Y, stdscr)
        self.cont = 1
        while self.cont:
            while 1:
                if key == KEY_RESIZE:
                    self.handle_size()
                else:

                    if key is ord('q'):
                        break
                    stdscr.clear()
                    stdscr.border(0)
                    #draw the border and score
                    for i in range(1, self.HEIGHT - 1):
                        stdscr.addstr(i, self.WIDTH // 2, "||", curses.color_pair(1))

                    stdscr.addstr(self.HEIGHT // 2, self.WIDTH // 2 + self.WIDTH // 4, tetro.count_score, curses.color_pair(0))

                    # append key and make move
                    if key in [KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                        tetro.change_direction(key)
                    tetro.update()

                    #draw the TETRO in its current position
                    tetro.render()
                    stdscr.refresh()
                    key = stdscr.getch()

            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr(self.HEIGHT//2 + 1, self.WIDTH // 2, "   GAME OVER", curses.color_pair(1))
            stdscr.addstr(self.HEIGHT//2 + 2, self.WIDTH // 2, "Press Q to exit", curses.color_pair(1))
            stdscr.addstr(self.HEIGHT//2 + 3, self.WIDTH // 2, "Press P to play again", curses.color_pair(1))
            while 1:
                key = stdscr.getch()
                if key != ord('q'):
                    self.cont = 0
                    break
                elif key == ord('p'):
                    break
            stdscr.refresh()

    def initializeWin(self):
        wrapper(self.draw_UI)


if __name__ == '__main__':
    TetrisWindow()
