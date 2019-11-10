import time
import curses
import asyncio
import random
import os

from itertools import cycle

from animations import fire, SpaceShip
from starsky import get_sky_coroutines
from space_garbage import garbage_coroutine_fabric
from curses_tools import read_controls
from settings import *


coroutines = []


async def fill_orbit_with_garbage(canvas):
    delay = 2
    delay_cadres = delay * FPS
    for coro in garbage_coroutine_fabric(canvas):
        coroutines.append(coro)
        for _ in range(delay_cadres):
            await asyncio.sleep(0)


async def game_object_action(canvas, game_object):
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        game_object.move(rows_direction, columns_direction)
        if space_pressed:
            coroutines.append(fire(canvas, *game_object.get_gun_coords()))
        await asyncio.sleep(0)


def draw(canvas, stars_count=80, frame_animations=None):
    sleep_time = 1 / FPS
    max_y, max_x = canvas.getmaxyx()
    global coroutines
    coroutines += get_sky_coroutines(canvas, max_x, max_y, stars_count)
    coroutines.append(fire(canvas, max_y-2, max_x//2))
    spaceship = SpaceShip(canvas)
    coroutines.append(spaceship.animate(canvas))
    coroutines.append(game_object_action(canvas, spaceship))
    coroutines.append(fill_orbit_with_garbage(canvas))
    curses.curs_set(False)
    canvas.nodelay(True)

    while coroutines:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()
        canvas.refresh()
        time.sleep(sleep_time)


# def get_animation_frames_files(animation_name):
#     frames_files = []
#     for filename in os.listdir(os.path.join(ANIMATIONS_FOLDER, animation_name)):
#         if filename.endswith(".txt"):
#             frames_files.append(os.path.join(ANIMATIONS_FOLDER, animation_name, filename))
#     return sorted(frames_files)


# def load_frame_animations():
#     animations = []
#     for func, kwargs in FRAME_ANIMATIONS:
#         animation_name = func.__name__
#         frames = []
#         frames_files = get_animation_frames_files(animation_name)
#         for filename in frames_files:
#             with open(filename) as f:
#                 frame = f.read()
#                 frames.append(frame)
#         animations.append((func, frames, kwargs))
#     return animations


if __name__ == '__main__':
    # animations = load_frame_animations()
    curses.update_lines_cols()
    curses.wrapper(draw)
