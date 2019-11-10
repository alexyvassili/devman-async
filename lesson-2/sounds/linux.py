from pyalsaaudio import playwav


def playsound(wav):
    device = 'default'
    f = playwav.wave.open(wav, 'rb')
    device = playwav.alsaaudio.PCM(device=device)
    playwav.play(device, f)
    f.close()
