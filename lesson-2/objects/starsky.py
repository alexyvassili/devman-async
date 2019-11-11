import curses
import random
import asyncio
from itertools import cycle
from collections import deque
from typing import List, Tuple, Coroutine

from settings import FPS

STAR_SYMBOLS = '+*.:'

# (star_blink, delay_time)
STAR_ANIMATION_PROFILE = [(curses.A_DIM, 2),
                          (curses.A_NORMAL, 0.3),
                          (curses.A_BOLD, 0.5),
                          (curses.A_NORMAL, 0.3)]


def get_random_stars_coords(max_x: int, max_y: int,
                            stars_count: int) -> List[Tuple[int, int]]:
    """совпадения не проверяются"""
    stars_coords = []
    for i in range(stars_count):
        x = random.randint(1, max_x-2)
        y = random.randint(1, max_y-2)
        stars_coords.append((x, y))
    return stars_coords


async def blink(canvas, row: int, column: int, symbol='*',
                start_from=0) -> None:
    blink_animation = deque([(blink_value, int(delay*FPS))
                             for blink_value, delay in STAR_ANIMATION_PROFILE])
    if 0 < start_from < 4:
        blink_animation.rotate(-start_from)

    for blink_value, delay_cadres in cycle(blink_animation):
        canvas.addstr(row, column, symbol, blink_value)
        for _ in range(delay_cadres):
            await asyncio.sleep(0)


def get_sky_coroutines(canvas, stars_count=80) -> List[Coroutine]:
    max_y, max_x = canvas.getmaxyx()
    stars_coords = get_random_stars_coords(max_x, max_y, stars_count)
    couroutines = [blink(canvas, row, column,
                         symbol=random.choice(STAR_SYMBOLS),
                         start_from=random.randint(0, 3))
                   for column, row in stars_coords]
    return couroutines
