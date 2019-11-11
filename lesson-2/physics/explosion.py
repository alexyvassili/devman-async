import asyncio
import curses
from physics.curses_tools import draw_frame, get_frame_size

EXPLOSION_FRAMES_SOURCE = [
    """\
           (_) 
       (  (   (  (
      () (  (  )
        ( )  ()
    """,
    """\
           (_) 
       (  (   (   
         (  (  )
          )  (
    """,
    """\
            (  
          (   (   
         (     (
          )  (
    """,
    """\
            ( 
              (
            (  

    """,
]

EXPLOSION_FRAMES = []
for frame in EXPLOSION_FRAMES_SOURCE:
    EXPLOSION_FRAMES.append(frame)
    EXPLOSION_FRAMES.append(frame)


async def explode(canvas, center_row: int, center_column: int) -> None:
    rows, columns = get_frame_size(EXPLOSION_FRAMES[0])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()
    for frame in EXPLOSION_FRAMES:
        draw_frame(canvas, corner_row, corner_column, frame)

        await asyncio.sleep(0)
        draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await asyncio.sleep(0)
