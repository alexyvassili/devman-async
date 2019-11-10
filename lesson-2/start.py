import time
import curses
import asyncio
from multiprocessing import Process, Queue

from objects.animations import Fire, SpaceShip
from objects.starsky import get_sky_coroutines
from objects.space_garbage import garbage_fabric
from physics.curses_tools import read_controls, draw_frame
from physics.collisions import collision, is_game_over
from gameplay.scenario import GameState
from gameplay.messages import show_game_over
from sounds.sounds import Sounds, add_sound, play_queue
from settings import *


sound_queue = Queue()
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
        rows_direction, columns_direction, space_pressed, escape_pressed = read_controls(canvas)
        game_object.move(rows_direction, columns_direction)
        if space_pressed and game_object.alive and game_state.year >= GUN_YEAR:
            fire = Fire(canvas, *game_object.get_gun_coords())
            fire_coro = fire.fire(canvas)
            coroutines.append(fire_coro)
            fires[fire_coro] = fire
            add_sound(sound_queue, Sounds.FIRE, game_state.game_over)
        if game_state.game_over and escape_pressed:
            game_state.escape = True
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
                if coroutine in fires:
                    fires.pop(coroutine)
                if coroutine in obstacles:
                    obstacles.pop(coroutine)
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
                        add_sound(sound_queue, Sounds.BOOM, game_state.game_over)
                if spaceship.alive and is_game_over(spaceship, obstacles):
                    add_sound(sound_queue, Sounds.GAMEOVER)
                    game_state.game_over = True
                    game_state.save_history()
                    spaceship.destroy()
                    coroutines.append(show_game_over(canvas))
        state_coro.send(None)
        canvas.border()
        canvas.refresh()
        cnv.refresh()
        time.sleep(sleep_time)
        if game_state.escape:
            break


if __name__ == '__main__':
    player = Process(target=play_queue, args=(sound_queue,))
    player.start()
    curses.update_lines_cols()
    curses.wrapper(draw)
    sound_queue.put(None)
    player.join()
