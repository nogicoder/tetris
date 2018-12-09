import math
import random
import os

block_shapes = [[[1, 0], [1, 1]]]

class Board:
    #CHECK
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = None
    #CHECK
    def start(self):
        """Start game"""

        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = 0

        self._place_new_block()

    #CHECK
    def is_game_over(self):
        """Is game over"""

        return self.game_over

    #CHECK
    def move_block(self, direction):
        """Try to move block"""

        pos = self.current_block_pos
        if direction == "left":
            new_pos = [pos[0], pos[1] - 1]
        elif direction == "right":
            new_pos = [pos[0], pos[1] + 1]
        elif direction == "down":
            new_pos = [pos[0] + 1, pos[1]]


        if self._can_move(new_pos, self.current_block.shape):
            self.current_block_pos = new_pos
        else:
            if direction == "down":
                self._land_block(pos, self.current_block.shape)
                self._burn()
                self._place_new_block()

    #CHECK
    def _get_new_board(self):
        """Create new empty board"""
        board = []
        for row in range(self.height):
            column = []
            for col in range(self.width):
                column.append(0)
            board.append(column)
        return board

    #CHECK
    def _place_new_block(self):
        """Place new block and generate the next one"""

        self.current_block = Block()
        size = self.current_block.size
        col_pos = round((self.width/2 - size[0] / 2))
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos, self.current_block.shape):
            self.game_over = True
        # else:
        #     self.score += 0

    #CHECK
    def _land_block(self, pos, shape):
        """Put block to the board and generate a new one"""

        size = self.current_block.size
        for row in range(size[0]):
            for col in range(size[1]):
                shape_element = shape[row][col]
                if shape_element == 1:
                    self.board[pos[0] + row][pos[1] + col] = 1

    #CHECK
    def _burn(self):
        """Remove matched lines"""

        for row in range(self.height):
            if all(col == 1 for col in self.board[row]):
                for item in range(row, 0, -1):
                    self.board[item] = self.board[item - 1]
                temp = []
                for i in range(self.width):
                    temp.append(0)
                self.board[0] = temp
                self.score += 1

    #CHECK
    def _check_overlapping(self, pos, shape):
        """If current block overlaps any other on the board"""

        size = self.current_block.size
        for row in range(size[0]):
            for col in range(size[1]):
                shape_element = shape[row][col]
                shape_element_on_board = self.board[pos[0] + row][pos[1] + col]
                if shape_element is 1 and \
                   shape_element == shape_element_on_board:
                    return True
        return False

    #CHECK
    def _can_move(self, pos, shape):
        """Check if move is possible"""
        size = self.current_block.size
        if pos[1] + size[1] > self.width \
                or pos[0] + size[0] > self.height \
                or self._check_overlapping(pos, shape):
            return False
        return True

#CHECK
class Block:
    """Block representation"""

    def __init__(self):
        self.shape = block_shapes[0]
        self.size = [2, 2]
