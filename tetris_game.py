import random
import time
import os
import sys
from typing import List, Tuple

# Tetris pieces (I, J, L, O, S, T, Z)
SHAPES = [
    [[1, 1, 1, 1]],
    [[2, 0, 0], [2, 2, 2]],
    [[0, 0, 3], [3, 3, 3]],
    [[4, 4], [4, 4]],
    [[0, 5, 5], [5, 5, 0]],
    [[0, 6, 0], [6, 6, 6]],
    [[7, 7, 0], [0, 7, 7]]
]

COLORS = {
    0: '  ',    # Empty space needs two spaces
    1: '🟦 ',   # I piece
    2: '🟨 ',   # J piece
    3: '🟧 ',   # L piece
    4: '🟥 ',   # O piece
    5: '🟩 ',   # S piece
    6: '🟪 ',   # T piece
    7: '⬜️ ',   # Z piece
    8: '⬛️ '    # Landed pieces
}

class TetrisGame:
    def __init__(self, height: int = 20, width: int = 10):
        self.height = height
        self.width = width
        self.board = [[0] * width for _ in range(height)]
        self.current_piece = None
        self.current_pos = None
        self.game_over = False
        self.score = 0
        self.spawn_piece()

    def spawn_piece(self) -> None:
        self.current_piece = random.choice(SHAPES)
        piece_width = len(self.current_piece[0])
        self.current_pos = [0, self.width // 2 - piece_width // 2]
        
        if self.check_collision():
            self.game_over = True

    def check_collision(self) -> bool:
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_pos[0] + y
                    board_x = self.current_pos[1] + x
                    if (board_y >= self.height or 
                        board_x < 0 or 
                        board_x >= self.width or 
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False

    def rotate_piece(self) -> None:
        old_piece = self.current_piece
        self.current_piece = list(zip(*self.current_piece[::-1]))
        if self.check_collision():
            self.current_piece = old_piece

    def move_piece(self, dx: int, dy: int) -> bool:
        self.current_pos[0] += dy
        self.current_pos[1] += dx
        
        if self.check_collision():
            self.current_pos[0] -= dy
            self.current_pos[1] -= dx
            return False
        return True

    def land_piece(self) -> None:
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_pos[0] + y
                    if board_y >= 0:
                        self.board[board_y][self.current_pos[1] + x] = 8

    def clear_lines(self) -> None:
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(cell != 0 for cell in self.board[y]):
                lines_cleared += 1
                self.board.pop(y)
                self.board.insert(0, [0] * self.width)
            else:
                y -= 1
        self.score += lines_cleared * 100

    def get_display_board(self) -> List[List[str]]:
        display = [row[:] for row in self.board]
        if self.current_piece and not self.game_over:
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        board_y = self.current_pos[0] + y
                        if board_y >= 0:
                            display[board_y][self.current_pos[1] + x] = cell
        return display

    def step(self) -> bool:
        if not self.move_piece(0, 1):
            self.land_piece()
            self.clear_lines()
            self.spawn_piece()
        return not self.game_over
