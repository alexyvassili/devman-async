from multiprocessing import Queue
from pyalsaaudio import playwav
import os


class Sounds:
    FOLDER = 'sounds/wav'
    FIRE = os.path.join(FOLDER, 'smb_fireball.wav')
    BOOM = os.path.join(FOLDER, 'smb_vine.wav')
    GAMEOVER = os.path.join(FOLDER, 'smb_gameover.wav')


def playsound(wav):
    device = 'default'
    f = playwav.wave.open(wav, 'rb')
    device = playwav.alsaaudio.PCM(device=device)
    playwav.play(device, f)
    f.close()


def play_queue(queue: Queue):
    while True:
        wav = queue.get()
        if not wav:
            break
        playsound(wav)


def add_sound(queue: Queue, sound, game_over=False):
    if not game_over and queue.qsize() < 2:
        queue.put(sound)
