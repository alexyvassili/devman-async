import time
import curses
import asyncio

from animations import Fire, SpaceShip
from starsky import get_sky_coroutines
from space_garbage import garbage_fabric
from curses_tools import read_controls, draw_frame
from collisions import collision, is_game_over
from game_scenario import GameState
from messages import show_game_over
from settings import *


game_state = GameState()
coroutines = []
obstacles = dict()
fires = dict()


async def fill_orbit_with_garbage(canvas):
    while not game_state.garbage_delay_ticks:
        await asyncio.sleep(0)

    for garbage in garbage_fabric(canvas):
        delay_cadres = game_state.garbage_delay_ticks * 5
        coro = garbage.fly(canvas)
        coroutines.append(coro)
        obstacles[coro] = garbage
        for _ in range(delay_cadres):
            await asyncio.sleep(0)


async def game_object_action(canvas, game_object):
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        game_object.move(rows_direction, columns_direction)
        if space_pressed and game_object.alive and game_state.year >= GUN_YEAR:
            fire = Fire(canvas, *game_object.get_gun_coords())
            fire_coro = fire.fire(canvas)
            coroutines.append(fire_coro)
            fires[fire_coro] = fire
        await asyncio.sleep(0)


async def draw_state(canvas):
    rows, columns = canvas.getmaxyx()
    empty_text = "\n".join([" " * columns for _ in range(rows)])
    while True:
        canvas.border()
        draw_frame(canvas, 1, 1, f"Year: {game_state.year}\t\tScore: {game_state.score}")
        draw_frame(canvas, 2, 1, game_state.phrase)
        await asyncio.sleep(0)
        draw_frame(canvas, 0, 0, empty_text)


def draw(canvas, stars_count=80):
    sleep_time = 1 / FPS
    max_y, max_x = canvas.getmaxyx()
    global coroutines
    coroutines += get_sky_coroutines(canvas, max_x, max_y, stars_count)
    spaceship = SpaceShip(canvas)
    coroutines.append(spaceship.animate(canvas))
    coroutines.append(game_object_action(canvas, spaceship))
    coroutines.append(fill_orbit_with_garbage(canvas))
    coroutines.append(game_state.tick())
    curses.curs_set(False)
    canvas.nodelay(True)
    cnv = canvas.derwin(5, 30, max_y - 5, max_x - 30)
    state_coro = draw_state(cnv)

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
                        rows, columns = obstacles[obstacle].size()
                        obstacles[obstacle].destroy()
                        obstacles.pop(obstacle)
                        game_state.score += rows * columns
                        game_state.shooted += 1
                if spaceship.alive and is_game_over(spaceship, obstacles):
                    game_state.save_history()
                    spaceship.destroy()
                    coroutines.append(show_game_over(canvas))
        state_coro.send(None)
        canvas.border()
        canvas.refresh()
        cnv.refresh()
        time.sleep(sleep_time)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
