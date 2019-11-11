import time
import curses
import asyncio
from multiprocessing import Process
from physics.curses_tools import draw_frame
from gameplay.scenario import GameState
from gameplay.core import Core
from sounds.sounds import play_queue
from settings import *


game_state = GameState()
core = Core()


async def draw_state(canvas):
    rows, columns = canvas.getmaxyx()
    empty_text = "\n".join([" " * columns for _ in range(rows)])
    while True:
        canvas.border()
        draw_frame(canvas, 1, 1, f"Year: {game_state.year}\t\tScore: {game_state.score}")
        draw_frame(canvas, 2, 1, game_state.phrase)
        await asyncio.sleep(0)
        draw_frame(canvas, 0, 0, empty_text)


def draw(canvas):
    sleep_time = 1 / FPS
    max_y, max_x = canvas.getmaxyx()
    core.load_coroutines(canvas, game_state)
    curses.curs_set(False)
    canvas.nodelay(True)
    cnv = canvas.derwin(5, 40, max_y - 5, max_x - 40)
    state_coro = draw_state(cnv)
    while True:
        core.flip_coroutines(canvas, game_state)
        state_coro.send(None)
        canvas.border()
        canvas.refresh()
        cnv.refresh()
        time.sleep(sleep_time)
        if game_state.escape:
            break


if __name__ == '__main__':
    if SOUNDS == "ON":
        player = Process(target=play_queue, args=(core.sound_queue,))
        player.start()
    curses.update_lines_cols()
    curses.wrapper(draw)
    if SOUNDS == "ON":
        core.sound_queue.put(None)
        player.join()
