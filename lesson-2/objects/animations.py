"""
    Animations objects in Game: SpaceShip and spaceship Fire
"""

import os
import asyncio
import curses
from itertools import cycle
from typing import List

from physics.curses_tools import  draw_frame, is_frame_in_canvas, get_frame_size
from physics.spaceship import update_speed

FRAMES_FOLDER = "objects/frames"


class SpaceShip:
    def __init__(self, canvas):
        self.max_y, self.max_x = canvas.getmaxyx()
        self.row = self.max_y - 10
        self.row_delta = 0
        self.column = self.max_x // 2
        self.column_delta = 0
        self.row_speed = 0
        self.column_speed = 0
        self.animation_name = 'spaceship'
        self.frames = self.load_frames()
        self.current_frame = self.frames[0]
        self.destroyed = False

    def destroy(self) -> None:
        self.destroyed = True

    def size(self) -> tuple:
        return get_frame_size(self.current_frame)

    def get_gun_coords(self) -> tuple:
        """Get spaceship gun coords (up center)."""
        rows, columns = get_frame_size(self.current_frame)
        return self.row, self.column + columns // 2

    def get_animation_frames_files(self) -> List[str]:
        frames_files = []
        for filename in os.listdir(os.path.join(FRAMES_FOLDER, self.animation_name)):
            if filename.endswith(".txt"):
                frames_files.append(os.path.join(FRAMES_FOLDER, self.animation_name, filename))
        return sorted(frames_files)

    def load_frames(self) -> List[str]:
        """Load animations frames."""
        frames = []
        frames_files = self.get_animation_frames_files()
        for filename in frames_files:
            with open(filename) as f:
                frame = f.read()
                frames.append(frame)
        return frames

    def move(self, rows_direction: int, columns_direction: int) -> None:
        """Move Spaceship by phisycs:

            - actions coro get directions by keyboard
            - move() get current speed
            - if spaceship can move, update delta_fields
            - animate() coroutine move spaceship by delta fields
        """
        self.row_speed, self.column_speed = update_speed(self.row_speed,
                                                         self.column_speed,
                                                         rows_direction,
                                                         columns_direction)
        if is_frame_in_canvas(self.current_frame, self.column,
                              self.row + self.row_speed, self.max_x, self.max_y):
            self.row_delta = self.row_speed
        if is_frame_in_canvas(self.current_frame, self.column + self.column_speed,
                              self.row, self.max_x, self.max_y):
            self.column_delta = self.column_speed

    def _do_move(self) -> None:
        self.row, self.row_delta = self.row + self.row_delta, 0
        self.column, self.column_delta = self.column + self.column_delta, 0

    async def animate(self, canvas) -> None:
        """Spaceship animation."""
        for frame in cycle(self.frames):
            self.current_frame = frame
            draw_frame(canvas, self.row, self.column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, self.row, self.column, frame, negative=True)
            if self.destroyed:
                return
            self._do_move()


class Fire:
    def __init__(self, canvas, start_row: int, start_column: int):
        self.rows, self.columns = canvas.getmaxyx()
        self.rows_speed = -0.5
        self.columns_speed = 0
        self.row = start_row
        self.column = start_column
        self.destroyed = False

    def destroy(self) -> None:
        self.destroyed = True

    def move(self) -> None:
        self.row += self.rows_speed
        self.column += self.columns_speed

    async def animate(self, canvas) -> None:
        """Display animation of gun shot. Direction and speed can be specified."""
        canvas.addstr(round(self.row), round(self.column), '*')
        await asyncio.sleep(0)

        canvas.addstr(round(self.row), round(self.column), 'O')
        await asyncio.sleep(0)
        canvas.addstr(round(self.row), round(self.column), ' ')

        self.move()

        symbol = '-' if self.columns_speed else '|'
        max_row, max_column = self.rows - 1, self.columns - 1

        curses.beep()

        while 0 < self.row < max_row and 0 < self.column < max_column:
            canvas.addstr(round(self.row), round(self.column), symbol)
            await asyncio.sleep(0)
            canvas.addstr(round(self.row), round(self.column), ' ')
            if self.destroyed:
                return
            self.move()
