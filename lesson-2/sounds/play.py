from multiprocessing import Queue, Event
from typing import Callable
import os
import sys

if sys.platform == 'linux':
    from sounds.linux import playsound
if sys.platform == 'win32':
    from sounds.win32 import playsound


class Sounds:
    FOLDER = 'sounds/wav'
    FIRE = os.path.join(FOLDER, 'smb_fireball.wav')
    BOOM = os.path.join(FOLDER, 'smb_vine.wav')
    GAMEOVER = os.path.join(FOLDER, 'smb_gameover.wav')
    PAUSE = os.path.join(FOLDER, 'smb_pause.wav')
    BACKGROUND = os.path.join(FOLDER, 'POL-outer-space-short.wav')


def play_loop(wav: str, event: Event) -> None:
    while not event.is_set():
        playsound(wav)


def play_queue(queue: Queue) -> None:
    while True:
        wav = queue.get()
        if not wav:
            break
        playsound(wav)


def add_sound(queue: Queue, sound: str, game_over=False) -> None:
    if not game_over and queue.qsize() < 2:
        queue.put(sound)
