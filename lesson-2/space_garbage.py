from curses_tools import draw_frame
import asyncio
import os
import random
from settings import FRAMES_FOLDER, GARBAGE_SPEED


async def fly_garbage(canvas, column, garbage_frame, speed=GARBAGE_SPEED):
    """Animate garbage, flying from top to bottom.
       Сolumn position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


def create_gargabe_coroutine(canvas, filename, position):
    with open(os.path.join(filename), "r") as garbage_file:
        frame = garbage_file.read()

    return fly_garbage(canvas, position, frame)


def get_garbage_frames():
    frames = []
    for filename in os.listdir(os.path.join(FRAMES_FOLDER, 'garbage')):
        frames.append(os.path.join(FRAMES_FOLDER, 'garbage', filename))
    return frames


def get_garbage_coords(max_x):
    return list(range(10, max_x - 10, 30))


def garbage_coroutine_fabric(canvas):
    garbage_frames = get_garbage_frames()
    max_y, max_x = canvas.getmaxyx()
    while True:
        frame = random.choice(garbage_frames)
        x_coord = random.randint(1, max_x-1)
        yield create_gargabe_coroutine(canvas, frame, x_coord)
