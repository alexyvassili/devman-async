from curses_tools import draw_frame
import asyncio
import os
from settings import FRAMES_FOLDER


async def fly_garbage(canvas, column, garbage_frame, speed=0.2):
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
    with open(os.path.join(FRAMES_FOLDER, filename), "r") as garbage_file:
        frame = garbage_file.read()

    return fly_garbage(canvas, position, frame)


def get_garbage_coroutines(canvas):
    coroutines = []
    for filename in ['duck.txt']:
        coroutines.append(create_gargabe_coroutine(canvas, filename, 10))
    return coroutines
