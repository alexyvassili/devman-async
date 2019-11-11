"""
    Collisions module. Manage objects collisions.
"""

from typing import Dict, Coroutine, Optional
from objects.animations import Fire, SpaceShip
from objects.space_garbage import Garbage


def _is_point_inside(corner_row: int, corner_column: int,
                     size_rows: int, size_columns: int,
                     point_row: int, point_row_column: int) -> bool:
    rows_flag = corner_row <= point_row < corner_row + size_rows
    columns_flag = corner_column <= point_row_column < corner_column + size_columns

    return rows_flag and columns_flag


def has_collision(obstacle_corner: tuple, obstacle_size: tuple,
                  obj_corner: tuple, obj_size=(1, 1)) -> bool:
    """Determine if collision has occured. Return True or False."""

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


def collision(fire: Fire, obstacles: Dict[Coroutine, Garbage]) -> Optional[Coroutine]:
    """Find collisions garbage and spaceship fire"""
    fire_coords = fire.row, fire.column
    for obstacle_coro, obstacle in obstacles.items():
        obstacle_corner = obstacle.row, obstacle.column
        if has_collision(obstacle_corner, obstacle.size(), fire_coords):
            return obstacle_coro
    return None


def is_game_over(spaceship: SpaceShip, obstacles: Dict[Coroutine, Garbage]) -> Optional[Coroutine]:
    """Game Over when we have collision of spaceship and garbage"""
    spaceship_coords = spaceship.row, spaceship.column
    for obstacle_coro, obstacle in obstacles.items():
        obstacle_corner = obstacle.row, obstacle.column
        if has_collision(obstacle_corner, obstacle.size(),
                         spaceship_coords, spaceship.size()):
            return obstacle_coro
    return None
