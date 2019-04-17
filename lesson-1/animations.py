import asyncio
import curses
from itertools import cycle

from curses_tools import  draw_frame, read_controls


async def animate_spaceship(canvas, frames, start_row=None, start_column=None):
    if start_row is None:
        start_row = canvas.getmaxyx()[0] // 2
    if start_column is None:
        start_column = canvas.getmaxyx()[1] // 2

    frames = cycle(frames)
    while True:
        frame = next(frames)
        draw_frame(canvas, start_row, start_column, frame)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, start_row, start_column, frame, negative=True)
        start_row += rows_direction
        start_column += columns_direction


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
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
    (animate_spaceship, {})
]
