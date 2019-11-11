from winsound import PlaySound, SND_FILENAME


def playsound(wav: str) -> None:
    PlaySound(wav, SND_FILENAME)
