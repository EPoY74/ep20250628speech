"""
Востроизведение текстовых сообщений
"""

from gtts import gTTS
import pygame
import os
import time

SOUND_FILE_NAME = "output.mp3"
IS_DELETE_AFTER_PLAY = False


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


def timer_clock(duration):
    """
    Запускает таймер, имитирующий часы, с тикающим звуком.

    Args:
        duration: Продолжительность работы таймера в секундах.
    """
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        current_time = time.localtime(time.time())
        formatted_time = time.strftime("%H:%M:%S", current_time)
        print(formatted_time, end="\r")  # Вывод в одну строку, обновляя

        play_mp3("tick.mp3")
        time.sleep(1)  # Пауза в 1 секунду
    print("\nТаймер завершен")


# text = b"\xd0\x9f\xd0\xbe\xd0\xb6\xd0\xb0\xd0\xbb\xd1\x83\xd0\xb9\xd1\x81\xd1\x82\xd0\xb0, \xd0\xb8\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5 \xd0\xbd\xd0\xb0\xd1\x85\xd1\x83\xd0\xb9!"
text = "Какое всё красивое"
language = "ru"

if __name__ == "__main__":
    duration_seconds = 20  # Задайте длительность таймера в секундах
    timer_clock(duration_seconds)
    try:
        # tts = gTTS(text=text.decode("utf-8"), lang=language, slow=False)
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(SOUND_FILE_NAME)
        # os.system("start output.mp3")
        play_mp3(SOUND_FILE_NAME)
        if IS_DELETE_AFTER_PLAY is not False:
            time.sleep(1)
            try:
                os.remove(SOUND_FILE_NAME)
            except PermissionError as err:
                raise (err)

    except Exception as err:
        raise err
