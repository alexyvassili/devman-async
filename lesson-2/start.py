import time
import curses
import asyncio

from animations import Fire, SpaceShip
from starsky import get_sky_coroutines
from space_garbage import garbage_fabric
from curses_tools import read_controls
from collisions import collision, is_game_over
from messages import show_game_over
from settings import *


coroutines = []
obstacles = dict()
fires = dict()


async def fill_orbit_with_garbage(canvas):
    delay = 2
    delay_cadres = delay * FPS
    for garbage in garbage_fabric(canvas):
        coro = garbage.fly(canvas)
        coroutines.append(coro)
        obstacles[coro] = garbage
        for _ in range(delay_cadres):
            await asyncio.sleep(0)


async def game_object_action(canvas, game_object):
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        game_object.move(rows_direction, columns_direction)
        if space_pressed:
            fire = Fire(canvas, *game_object.get_gun_coords())
            fire_coro = fire.fire(canvas)
            coroutines.append(fire_coro)
            fires[fire_coro] = fire
        await asyncio.sleep(0)


def draw(canvas, stars_count=80, frame_animations=None):
    sleep_time = 1 / FPS
    max_y, max_x = canvas.getmaxyx()
    global coroutines
    coroutines += get_sky_coroutines(canvas, max_x, max_y, stars_count)
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
            else:
                if coroutine in fires:
                    obstacle = collision(fires[coroutine], obstacles)
                    if obstacle:
                        fires[coroutine].destroy()
                        fires.pop(coroutine)
                        obstacles[obstacle].destroy()
                        obstacles.pop(obstacle)
                if spaceship.alive and is_game_over(spaceship, obstacles):
                    spaceship.destroy()
                    coroutines.append(show_game_over(canvas))
        canvas.border()
        canvas.refresh()
        time.sleep(sleep_time)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
