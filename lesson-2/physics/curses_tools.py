SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258
ESCAPE_KEY_CODE = 27
PAUSE_KEY_CODE = 80


def draw_frame(canvas, start_row: int, start_column: int, text: str, negative=False) -> None:
    """Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def read_controls(canvas) -> tuple:
    """Read keys pressed and returns tuple with controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False
    escape_pressed = False
    pause_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

        if pressed_key_code == ESCAPE_KEY_CODE:
            escape_pressed = True

        if pressed_key_code == PAUSE_KEY_CODE:
            pause_pressed = True

    return rows_direction, columns_direction, space_pressed, escape_pressed, pause_pressed


def get_frame_size(text):
    """Calculate size of multiline text fragment.
        Returns pair (rows number, colums number)
    """

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])

    return rows, columns


def is_frame_in_canvas(text: str, start_x: int, start_y: int, max_x: int, max_y: int) -> bool:
    rows, columns = get_frame_size(text)
    if start_x <= 0 or start_y <= 0:
        return False
    if start_x + columns >= max_x:
        return False
    if start_y + rows >= max_y:
        return False

    return True
