from multiprocessing import Queue
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


def play_queue(queue: Queue):
    while True:
        wav = queue.get()
        if not wav:
            break
        playsound(wav)


def add_sound(queue: Queue, sound, game_over=False):
    if not game_over and queue.qsize() < 2:
        queue.put(sound)
