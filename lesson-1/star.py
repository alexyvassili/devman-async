import time
import curses
import asyncio

from itertools import cycle


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas, stars_count=5):
    row, column = (5, 20)
    couroutines = [blink(canvas, row, column+i*2) for i in range(stars_count)]
    canvas.border()
    curses.curs_set(False)
    sleeps_times = cycle([2, 0.3, 0.5, 0.3])
    while True:
        sleep_time = next(sleeps_times)
        for couroutine in couroutines:
            try:
                couroutine.send(None)
            except StopIteration:
                couroutines.remove(couroutine)
        if len(couroutines) == 0:
            break
        canvas.refresh()
        time.sleep(sleep_time)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
