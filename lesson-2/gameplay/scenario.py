"""
    Description of game scenario.
    Load and save history.
    Game State Object:
        - keep current year
        - year ticking coroutine
        - keep game over state
"""

import asyncio
from typing import List, Optional
from datetime import datetime
import time
import re
from settings import FPS, START_YEAR


PHRASES = {
    # Только на английском, Repl.it ломается на кириллице
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station\nSalute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun!\nShoot the garbage!",
}


def get_garbage_delay_tics(year: int) -> Optional[int]:
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


def load_history() -> List[str]:
    with open('stat/history.txt') as f:
        history = list(f.readlines())
    return history


def parse_history_records(history: List[str]) -> List[int]:
    records = []
    for item in history:
        record = re.search(r"Score:\s(\d+)", item)[1]
        records.append(int(record))
    return records


def load_record() -> int:
    """Load must cool score result from history"""
    history = load_history()
    records = parse_history_records(history)
    return max(records) if records else 0


class GameState:
    def __init__(self):
        self.year = START_YEAR
        self.phrase = PHRASES.get(self.year, "Let's go the game!")
        self.garbage_delay_ticks = get_garbage_delay_tics(self.year)
        self.change_ticks = int(FPS * 1.5)
        self.score = 0
        self.record = load_record()
        self.shooted = 0
        self.start_time = time.time()
        self.start_date = datetime.today().strftime("%d-%m-%Y %H:%M")
        self.game_over = False  # Is game over flag
        self.escape = False  # If user can exit by key flag

    def switch_year(self) -> None:
        """Switch year in game state"""
        self.year += 1
        if self.year in PHRASES:
            self.phrase = PHRASES[self.year]
        self.garbage_delay_ticks = get_garbage_delay_tics(self.year)

    def save_history(self) -> None:
        playing_time = (time.time() - self.start_time) / 60
        playing_time = round(playing_time, 2)
        stat_str = f"{self.start_date}\tScore: {self.score}" \
            f"\tShooted: {self.shooted}\tTime: {playing_time} min.\n"
        with open("stat/history.txt", "a") as myfile:
            myfile.write(stat_str)

    async def tick(self) -> None:
        """Years ticking by FPS"""
        while True:
            for i in range(self.change_ticks):
                await asyncio.sleep(0)
            self.switch_year()
