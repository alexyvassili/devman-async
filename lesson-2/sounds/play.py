"""
    Play game sounds: actions and background.
    Linux: need pyalsaaudio pip package and libasound2-dev deb package
    Windows: using python embedded winsound
"""

from multiprocessing import Queue, Event
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
    BACKGROUND = os.path.join(FOLDER, 'limbo_soundtrack_4.wav')


def play_loop(wav: str, event: Event) -> None:
    """Play wav file forever"""
    while not event.is_set():
        playsound(wav)


def play_queue(queue: Queue) -> None:
    """play sounds from queue"""
    while True:
        wav = queue.get()
        if not wav:
            break
        playsound(wav)


def add_sound(queue: Queue, sound: str, game_over=False) -> None:
    """Manage game sounds queue"""
    if not game_over and queue.qsize() < 2:
        queue.put(sound)
