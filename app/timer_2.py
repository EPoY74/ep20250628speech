import os
import threading
import time
from queue import Queue

import playsound
from gtts import gTTS


def play_sound_from_file(filename: str):
    """Воспроизводит звук из файла."""
    try:
        # Проверяем существование файла
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден")
            return

        # Воспроизводим с блокировкой (block=True), чтобы избежать наложения звуков
        playsound.playsound(filename, block=True)
    except Exception as e:
        print(f"Ошибка при воспроизведении звука {filename}: {e}")


def get_voice_from_ai(message: str) -> str:
    """Генерирует аудиофайл и возвращает имя файла"""
    try:
        filename = f"voice_{int(time.time())}.mp3"
        tts = gTTS(text=message, lang="ru", slow=False)
        tts.save(filename)
        return filename
    except Exception as err:
        print(f"Ошибка генерации голоса: {err}")
        raise


def make_and_play_voice_message():
    """Поток для обработки голосовых сообщений"""
    while True:
        message = q.get()
        if message == "STOP":
            break

        try:
            print(f"Обработка сообщения: {message}")
            voice_file = get_voice_from_ai(message)
            play_sound_from_file(voice_file)
            # Удаляем временный файл после воспроизведения
            os.remove(voice_file)
        except Exception as e:
            print(f"Ошибка в голосовом потоке: {e}")
        finally:
            q.task_done()


def timer_clock(duration: int, playback_interval: int):
    """Основной поток таймера"""
    start_time = time.time()
    for seconds_counter in range(duration):
        elapsed = time.time() - start_time
        remaining = duration - seconds_counter

        # Вывод информации
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(
            f"Время: {current_time}, Прошло: {seconds_counter} сек, Осталось: {remaining} сек",
            end="\r",
        )

        # Тикающий звук
        play_sound_from_file("tick.mp3")

        # Голосовое уведомление
        if seconds_counter % playback_interval == 0:
            mins = remaining // 60
            q.put(f"Осталось {int(mins)} минут")

        time.sleep(1)

    q.put("STOP")
    print("\nТаймер завершен")


if __name__ == "__main__":
    # Настройки
    playback_interval = 20  # секунд
    duration_seconds = 300  # 5 минут

    # Очередь для межпоточного взаимодействия
    q = Queue()

    # Запуск потока для голосовых сообщений
    voice_thread = threading.Thread(
        target=make_and_play_voice_message, daemon=True
    )
    voice_thread.start()

    # Запуск таймера в главном потоке (можно вынести в отдельный поток)
    try:
        timer_clock(duration_seconds, playback_interval)
    except KeyboardInterrupt:
        q.put("STOP")

    # Ожидание завершения
