"""
    Garbage objects and garbage fabric
"""

import asyncio
import os
import random
import math
from typing import List, Iterable, Tuple
from physics.explosion import explode
from physics.curses_tools import draw_frame, get_frame_size
from settings import GARBAGE_SPEED

FRAMES_FOLDER = 'objects/frames'


class Garbage:
    def __init__(self, canvas, column: int, garbage_frame: str):
        self.rows_number, self.columns_number = canvas.getmaxyx()
        self.column = max(column, 0)
        self.column = min(column, self.columns_number - 1)
        self.row = 0
        self.frame = garbage_frame
        x, y = get_frame_size(self.frame)
        self.speed=GARBAGE_SPEED - math.sqrt(x * y) / 100
        self.destroyed = False
    
    @property
    def size(self) -> Tuple[int, int]:
        return get_frame_size(self.frame)
    
    @property
    def scores(self) -> int:
        rows, columns = self.size
        return rows * columns

    def destroy(self) -> None:
        self.destroyed = True

    async def fly(self, canvas) -> None:
        """Animate garbage, flying from top to bottom.

           Сolumn position will stay same, as specified on start.
        """
        while self.row < self.rows_number:
            draw_frame(canvas, self.row, self.column, self.frame)
            await asyncio.sleep(0)
            draw_frame(canvas, self.row, self.column, self.frame, negative=True)
            if self.destroyed:
                rows, columns = self.size
                end_row, end_column = self.row + rows, self.column + columns
                center_row = (self.row + end_row) // 2
                center_columns = (self.column + end_column) // 2
                await explode(canvas, center_row, center_columns)
                return
            self.row += self.speed


def create_gargabe(canvas, filename: str, position: int) -> Garbage:
    with open(os.path.join(filename), "r") as garbage_file:
        frame = garbage_file.read()
    return Garbage(canvas, position, frame)


def get_garbage_frames() -> List[str]:
    frames = []
    for filename in os.listdir(os.path.join(FRAMES_FOLDER, 'garbage')):
        frames.append(os.path.join(FRAMES_FOLDER, 'garbage', filename))
    return frames


def garbage_fabric(canvas) -> Iterable[Garbage]:
    garbage_frames = get_garbage_frames()
    max_y, max_x = canvas.getmaxyx()
    while True:
        frame = random.choice(garbage_frames)
        x_coord = random.randint(1, max_x-1)
        yield create_gargabe(canvas, frame, x_coord)
