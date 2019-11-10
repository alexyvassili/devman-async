import asyncio
from datetime import datetime
import time
from settings import FPS, START_YEAR


PHRASES = {
    # Только на английском, Repl.it ломается на кириллице
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


class GameState:
    def __init__(self):
        self.year = START_YEAR
        self.phrase = PHRASES.get(self.year, "Let's go the game!")
        self.garbage_delay_ticks = get_garbage_delay_tics(self.year)
        self.change_ticks = int(FPS * 1.5)
        self.score = 0
        self.shooted = 0
        self.start_time = time.time()
        self.start_date = datetime.today().strftime("%d-%m-%Y %H:%M")
        self.game_over = False
        self.escape = False

    def switch_year(self):
        self.year += 1
        if self.year in PHRASES:
            self.phrase = PHRASES[self.year]
        self.garbage_delay_ticks = get_garbage_delay_tics(self.year)

    def save_history(self):
        playing_time = (time.time() - self.start_time) / 60
        playing_time = round(playing_time, 2)
        stat_str = f"{self.start_date}\tScore: {self.score}\tShooted: {self.shooted}\tTime: {playing_time} min.\n"
        with open("stat/history.txt", "a") as myfile:
            myfile.write(stat_str)

    async def tick(self):
        while True:
            for i in range(self.change_ticks):
                await asyncio.sleep(0)
            self.switch_year()
