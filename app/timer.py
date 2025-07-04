import os
import threading
import time
from queue import Queue

import playsound
import pygame
from gtts import gTTS


def play_mp3(file_path: str):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        # Ждем окончания воспроизведения
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
    except Exception as err:
        print("Ошибка при воспроизведении: {err}")
        raise (err)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(file_path)


def play_sound_from_file(filename: str):
    """Воспроизводит звук из файла."""
    try:
        playsound.playsound("tick.mp3", block=False)
    except Exception as e:
        print(f"Ошибка при воспроизведении звука: {e}")


def get_voice_from_ai(message: str) -> None:
    try:
        tts = gTTS(text=message, lang="ru", slow=False)
        tts.save("elapsed_time.mp3")

    except Exception as err:
        raise err


def start_timer():
    timer_clock(duration_seconds, playback_interval_seconds)


def make_and_play_voice_message():
    while not stop_event.wait(timeout=0.1):
        text_for_voice_message: str = ""
        text_for_voice_message = str(queue_voice_message.get())
        if text_for_voice_message == "STOP":
            queue_voice_message.task_done()
            break
        if isinstance(text_for_voice_message, str):
            get_voice_from_ai(text_for_voice_message)
        else:
            print("text_for_voice_message не str")
            queue_voice_message.task_done()
            raise ()
        play_mp3("elapsed_time.mp3")
        queue_voice_message.task_done()
    else:
        queue_voice_message.task_done()


def timer_clock(duration: int, playback_interval: int):
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
        seconds_counter += 1

        if elapsed_time >= duration:
            # q.task_done()
            stop_event.set()
            break

        current_time = time.localtime(time.time())
        formatted_time = time.strftime("%H:%M:%S", current_time)
        print(
            f" Текущее время: {formatted_time}, "
            f"Прошло {str(seconds_counter)} секунд",
            end="\r",
        )  # Вывод в одну строку, обновляя

        play_event.set()
        time.sleep(1)  # Пауза в 1 секунду
        # seconds_counter += 1
        print(seconds_counter, end="\r")
        output_elapsed_time(duration, playback_interval, seconds_counter)

    print("\nТаймер завершен")
    queue_voice_message.put("STOP")


def play_tick_from_file():
    while not stop_event.wait(timeout=0.1):
        if play_event.is_set():
            play_sound_from_file("tick.mp3")
            play_event.clear()
    # else:
    #     # Чтобы избежать активного ожидания, можно добавить паузу
    #     time.sleep(0.01)


def output_elapsed_time(
    duration: int, playback_interval: int, seconds_counter: int
):
    if seconds_counter <= 1:
        voice_message: str = "Привет Матвей! Сеанс массажа начат."
        queue_voice_message.put(voice_message)
        time.sleep(1)

    if seconds_counter % playback_interval == 0:
        elapsed_seconds: int = duration - seconds_counter
        elapsed_minutes: int = elapsed_seconds // 60
        voice_message: str = (
            f"Матвей! Осталось {str(int(elapsed_minutes))}"
            f" {pluralize_ru(elapsed_minutes)}"
        )
        queue_voice_message.put(voice_message)
        time.sleep(1)

    if seconds_counter == (duration - 5):
        voice_message: str = "Сеанс массажа окончен, Матвей - ты супер!"
        queue_voice_message.put(voice_message)
        time.sleep(1)


def pluralize_ru(number: int) -> str:
    forms: list = ["минута", "минуты", "минут"]
    if number % 10 == 1 and number % 100 != 11:
        return forms[0]
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return forms[1]
    else:
        return forms[2]


# print(pluralize_ru(5, ["минута", "минуты", "минут"]))  # "минут"


if __name__ == "__main__":
    duration_munutes: int = 45
    elapse_playback_interval_minutes: int = 5
    queue_voice_message: Queue = Queue()
    duration_seconds: int = (
        duration_munutes * 60
    )  # Задайте длительность таймера в секундах
    playback_interval_seconds: int = elapse_playback_interval_minutes * 60
    stop_event = threading.Event()
    play_event = threading.Event()

    thread_speech = threading.Thread(
        target=make_and_play_voice_message, daemon=True
    )
    thread_speech.start()

    thread_click = threading.Thread(target=play_tick_from_file, daemon=True)
    thread_click.start()

    # Запуск таймера в главном потоке (можно вынести в отдельный поток)
    try:
        start_timer()
    except KeyboardInterrupt:
        queue_voice_message.put("STOP")
        stop_event.set()
        # q.task_done()
    queue_voice_message.join()
    thread_speech.join()
