def _is_point_inside(corner_row, corner_column, size_rows, size_columns, point_row, point_row_column):
    rows_flag = corner_row <= point_row < corner_row + size_rows
    columns_flag = corner_column <= point_row_column < corner_column + size_columns

    return rows_flag and columns_flag


def has_collision(obstacle_corner, obstacle_size, obj_corner, obj_size=(1, 1)):
    '''Determine if collision has occured. Return True or False.'''

    opposite_obstacle_corner = (
        obstacle_corner[0] + obstacle_size[0] - 1,
        obstacle_corner[1] + obstacle_size[1] - 1,
    )

    opposite_obj_corner = (
        obj_corner[0] + obj_size[0] - 1,
        obj_corner[1] + obj_size[1] - 1,
    )

    return any([
        _is_point_inside(*obstacle_corner, *obstacle_size, *obj_corner),
        _is_point_inside(*obstacle_corner, *obstacle_size, *opposite_obj_corner),

        _is_point_inside(*obj_corner, *obj_size, *obstacle_corner),
        _is_point_inside(*obj_corner, *obj_size, *opposite_obstacle_corner),
])


def collision(fire, obstacles):
    fire_coords = fire.row, fire.column
    for obstacle_coro, obstacle in obstacles.items():
        obstacle_corner = obstacle.row, obstacle.column
        if has_collision(obstacle_corner, obstacle.size(), fire_coords):
            return obstacle_coro
    return None


def is_game_over(spaceship, obstacles):
    spaceship_coords = spaceship.row, spaceship.column
    for obstacle_coro, obstacle in obstacles.items():
        obstacle_corner = obstacle.row, obstacle.column
        if has_collision(obstacle_corner, obstacle.size(), spaceship_coords, spaceship.size()):
            return obstacle_coro
    return None
