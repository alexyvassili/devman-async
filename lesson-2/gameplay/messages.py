import asyncio
from physics.curses_tools import draw_frame, get_frame_size


async def show_game_over(canvas) -> None:
    max_y, max_x = canvas.getmaxyx()
    filename = 'gameplay/frames/game_over.txt'
    with open(filename) as f:
        frame = f.read()
    rows, columns = get_frame_size(frame)
    draw_row = max_y // 2 - rows // 1.5
    draw_column = max_x // 2 - columns // 1.5
    while True:
        draw_frame(canvas, draw_row, draw_column, frame)
        await asyncio.sleep(0)
