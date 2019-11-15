"""
Core Game object:

    - manage game coroutines
    - process async loop
    - keep sound queue
    - remove empty coroutines
    - read control keys
    - fill orbit with garbage
    - manage game over
"""

import asyncio
from multiprocessing import Queue
from typing import Coroutine
from objects.starsky import get_sky_coroutines
from objects.animations import Fire, SpaceShip
from objects.space_garbage import garbage_fabric
from physics.collisions import find_collision, find_spaceship_collision
from sounds.play import add_sound, Sounds
from gameplay.messages import show_game_over
from gameplay.scenario import GameState
from physics.curses_tools import read_controls
from settings import GUN_YEAR


class Core:
    def __init__(self):
        self.coroutines = []  # list of game coroutines, main async loop
        self.sound_queue = Queue()  # queue of game sounds
        self.obstacles = dict()  # Dict[coroutine, Garbage] of garbages
        self.fires = dict()  # Dict[coroutine, Fire] of spaceship shots coros
        self.spaceship = None  # Spaceship object

    def load_coroutines(self, canvas, game_state: GameState) -> None:
        """Load All coroutines to async loop:

            - sky coroutines
            - spaceship coroutines
            - garbage fabric coroutine
            - game state ticking years coroutine
        """
        self.coroutines += get_sky_coroutines(canvas)
        self.spaceship = SpaceShip(canvas)
        self.coroutines.append(self.spaceship.animate(canvas))
        self.coroutines.append(self.do_spaceship_action(canvas, game_state))
        self.coroutines.append(self.fill_orbit_with_garbage(canvas, game_state))
        self.coroutines.append(game_state.tick())

    def _remove_empty_coro(self, coroutine: Coroutine) -> None:
        """If coroutine is empty, remove it from main loop, fires and obstacles"""
        self.coroutines.remove(coroutine)
        if coroutine in self.fires:
            self.fires.pop(coroutine)
        if coroutine in self.obstacles:
            self.obstacles.pop(coroutine)

    def _process_fire_collision(self, coroutine: Coroutine,
                                game_state: GameState) -> None:
        """Fire collision: if fire meet garbage - garbage destroy.

            And player get scores equal garbage square
        """
        obstacle = find_collision(self.fires[coroutine], self.obstacles)
        if not obstacle:
            return
        self.fires[coroutine].destroy()
        self.fires.pop(coroutine)
        rows, columns = self.obstacles[obstacle].size()
        self.obstacles[obstacle].destroy()
        self.obstacles.pop(obstacle)
        game_state.score += rows * columns
        game_state.shooted += 1
        add_sound(self.sound_queue, Sounds.BOOM, game_state.game_over)

    def _game_over(self, canvas, game_state: GameState) -> None:
        """Game over actions"""
        add_sound(self.sound_queue, Sounds.GAMEOVER)
        game_state.game_over = True
        game_state.save_history()
        self.spaceship.destroy()
        self.coroutines.append(show_game_over(canvas))

    def flip_coroutines(self, canvas, game_state: GameState):
        """Main async loop process - sending None to all coroutines."""
        for coroutine in self.coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                self._remove_empty_coro(coroutine)
            else:
                if coroutine in self.fires:
                    self._process_fire_collision(coroutine, game_state)
                if not self.spaceship.destroyed and find_spaceship_collision(self.spaceship,
                                                                     self.obstacles):
                    self._game_over(canvas, game_state)

    async def fill_orbit_with_garbage(self, canvas,
                                      game_state: GameState) -> None:
        """Filling orbit with garbage."""
        while not game_state.garbage_delay_ticks:
            await asyncio.sleep(0)

        for garbage in garbage_fabric(canvas):
            delay_cadres = game_state.garbage_delay_ticks * 5
            coro = garbage.fly(canvas)
            self.coroutines.append(coro)
            self.obstacles[coro] = garbage
            for _ in range(delay_cadres):
                await asyncio.sleep(0)

    async def do_spaceship_action(self, canvas, game_state: GameState) -> None:
        """Read controls and manage gameplay:

            - spaceship moves and shooting
            - pause and exit
            - player can exit only if Game Over
        """
        pause_flag = False
        while True:
            rows_direction, columns_direction, space_pressed, \
            escape_pressed, pause_pressed = read_controls(canvas)
            if pause_pressed:
                add_sound(self.sound_queue, Sounds.PAUSE, game_state.game_over)
                pause_flag = not pause_flag
            if pause_flag:
                continue
            self.spaceship.move(rows_direction, columns_direction)
            if (space_pressed and not self.spaceship.destroyed
                    and game_state.year >= GUN_YEAR):
                fire = Fire(canvas, *self.spaceship.get_gun_coords())
                fire_coro = fire.animate(canvas)
                self.coroutines.append(fire_coro)
                self.fires[fire_coro] = fire
                add_sound(self.sound_queue, Sounds.FIRE, game_state.game_over)
            if game_state.game_over and escape_pressed:
                # ESC working only on game over
                game_state.escape = True
            await asyncio.sleep(0)
