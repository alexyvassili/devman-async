import os
import asyncio
import curses
from itertools import cycle

from curses_tools import  draw_frame, read_controls, is_frame_in_canvas, get_frame_size
from settings import ANIMATIONS_FOLDER


class SpaceShip:
    def __init__(self, canvas):
        self.max_y, self.max_x = canvas.getmaxyx()
        self.row = self.max_y // 2
        self.row_delta = 0
        self.column = self.max_x // 2
        self.column_delta = 0
        self.animation_name = 'animate_spaceship'
        self.frames = self.load_frames()
        self.current_frame = self.frames[0]

    def get_gun_coords(self):
        rows, columns = get_frame_size(self.current_frame)
        return self.row, self.column + columns // 2

    def get_animation_frames_files(self):
        frames_files = []
        for filename in os.listdir(os.path.join(ANIMATIONS_FOLDER, self.animation_name)):
            if filename.endswith(".txt"):
                frames_files.append(os.path.join(ANIMATIONS_FOLDER, self.animation_name, filename))
        return sorted(frames_files)

    def load_frames(self):
        frames = []
        frames_files = self.get_animation_frames_files()
        for filename in frames_files:
            with open(filename) as f:
                frame = f.read()
                frames.append(frame)
        return frames

    def move(self, rows_direction, columns_direction):
        if is_frame_in_canvas(self.current_frame, self.column,
                              self.row + rows_direction, self.max_x, self.max_y):
            self.row_delta += rows_direction
        if is_frame_in_canvas(self.current_frame, self.column + columns_direction,
                              self.row, self.max_x, self.max_y):
            self.column_delta += columns_direction

    def _do_move(self):
        self.row, self.row_delta = self.row + self.row_delta, 0
        self.column, self.column_delta = self.column + self.column_delta, 0

    async def animate(self, canvas):
        for frame in cycle(self.frames):
            self.current_frame = frame
            # draw_frame(canvas, self.row, self.column, frame, negative=True)
            draw_frame(canvas, self.row, self.column, frame)
            # await asyncio.sleep(0)  # из-за того, что fps стал 20
            await asyncio.sleep(0)
            draw_frame(canvas, self.row, self.column, frame, negative=True)
            self._do_move()




async def animate_spaceship(canvas, frames, start_row=None, start_column=None):
    max_y, max_x = canvas.getmaxyx()
    if start_row is None:
        start_row = max_y // 2
    if start_column is None:
        start_column = max_x // 2

    for frame in cycle(frames):
        draw_frame(canvas, start_row, start_column, frame)
        # await asyncio.sleep(0)  # из-за того, что fps стал 20
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, start_row, start_column, frame, negative=True)
        if is_frame_in_canvas(frame, start_column,
                              start_row + rows_direction, max_x, max_y):
            start_row += rows_direction
        if is_frame_in_canvas(frame, start_column + columns_direction,
                              start_row, max_x, max_y):
            start_column += columns_direction


async def fire(canvas, start_row, start_column, rows_speed=-0.5, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


FRAME_ANIMATIONS = [
    (animate_spaceship, {}),
]
