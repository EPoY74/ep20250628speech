import asyncio
import threading
import time
from queue import Queue

import playsound


async def play_tick():
    """Воспроизводит звук "тика"."""
    try:
        playsound.playsound(
            "tick.mp3", block=False
        )  # Замените "tick.mp3" на ваш звуковой файл
    except Exception as e:
        print(f"Ошибка при воспроизведении звука: {e}")


async def timer_clock(duration: int, playback_interval: int):
    """
    Запускает таймер, имитирующий часы, с тикающим звуком.

    Args:
        duration(int): Продолжительность работы таймера в секундах.
        playback_interval(int): Период воспроизведения сообщения
    """
    seconds_counter: int = 0
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= duration:
            break

        current_time = time.localtime(time.time())
        formatted_time = time.strftime("%H:%M:%S", current_time)
        print(formatted_time, end="\r")  # Вывод в одну строку, обновляя
        print()
        await play_tick()
        await asyncio.sleep(1)  # Пауза в 1 секунду
        seconds_counter += 1
        print(seconds_counter, end="\r")
        if seconds_counter % playback_interval == 0:
            elapsed = (duration / 60) - (seconds_counter / 60)
            print(f"Прошло {elapsed} минут")

    print("\nТаймер завершен")


if __name__ == "__main__":
    playback_interval: int = 1 * 60
    # ready_event = threading.Event()
    q = Queue()
    duration_seconds = 300  # Задайте длительность таймера в секундах
    asyncio.run(timer_clock(duration_seconds, playback_interval))
