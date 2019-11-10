import asyncio
import os
import random
from explosion import explode
from curses_tools import draw_frame, get_frame_size
from settings import FRAMES_FOLDER, GARBAGE_SPEED


class Garbage:
    def __init__(self, canvas, column, garbage_frame):
        self.rows_number, self.columns_number = canvas.getmaxyx()

        self.column = max(column, 0)
        self.column = min(column, self.columns_number - 1)
        self.row = 0
        self.frame = garbage_frame
        self.speed=GARBAGE_SPEED
        self._destroy = False

    def size(self):
        return get_frame_size(self.frame)

    def destroy(self):
        self._destroy = True

    async def fly(self, canvas):
        """Animate garbage, flying from top to bottom.
           Сolumn position will stay same, as specified on start.
        """
        while self.row < self.rows_number:
            draw_frame(canvas, self.row, self.column, self.frame)
            await asyncio.sleep(0)
            draw_frame(canvas, self.row, self.column, self.frame, negative=True)
            if self._destroy:
                rows, columns = self.size()
                end_row, end_column = self.row + rows, self.column + columns
                center_row = (self.row + end_row) // 2
                center_columns = (self.column + end_column) // 2
                await explode(canvas, center_row, center_columns)
                return
            self.row += self.speed


def create_gargabe(canvas, filename, position):
    with open(os.path.join(filename), "r") as garbage_file:
        frame = garbage_file.read()
    return Garbage(canvas, position, frame)


def get_garbage_frames():
    frames = []
    for filename in os.listdir(os.path.join(FRAMES_FOLDER, 'garbage')):
        frames.append(os.path.join(FRAMES_FOLDER, 'garbage', filename))
    return frames


def get_garbage_coords(max_x):
    return list(range(10, max_x - 10, 30))


def garbage_fabric(canvas):
    garbage_frames = get_garbage_frames()
    max_y, max_x = canvas.getmaxyx()
    while True:
        frame = random.choice(garbage_frames)
        x_coord = random.randint(1, max_x-1)
        yield create_gargabe(canvas, frame, x_coord)
