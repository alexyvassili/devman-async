import curses
import random
import asyncio
from itertools import cycle

from settings import FPS

STAR_SYMBOLS = '+*.:'

# (star_blink, delay_time)
STAR_ANIMATION_PROFILE = [(curses.A_DIM, 2),
                          (curses.A_NORMAL, 0.3),
                          (curses.A_BOLD, 0.5),
                          (curses.A_NORMAL, 0.3)]


def get_random_stars_coords(max_x, max_y, stars_count):
    """совпадения не проверяются"""
    stars_coords = []
    for i in range(stars_count):
        x = random.randint(1, max_x-2)
        y = random.randint(1, max_y-2)
        stars_coords.append((x, y))
    return stars_coords


async def blink(canvas, row, column, symbol='*', start_from=0):
    blink_animation = [(blink_value, int(delay*FPS)) for blink_value, delay in STAR_ANIMATION_PROFILE]

    if 0 < start_from < 4:
        blink_animation = blink_animation[start_from:] + blink_animation[:start_from]
    blink_cycle = cycle(blink_animation)

    while True:
        blink_value, delay_cadres = next(blink_cycle)
        canvas.addstr(row, column, symbol, blink_value)
        for _ in range(delay_cadres):
            await asyncio.sleep(0)


def get_sky_coroutines(canvas, max_x, max_y, stars_count):
    stars_coords = get_random_stars_coords(max_x, max_y, stars_count)
    couroutines = [blink(canvas, row, column,
                         symbol=random.choice(STAR_SYMBOLS),
                         start_from=random.randint(0, 3)) for column, row in stars_coords]
    return couroutines
