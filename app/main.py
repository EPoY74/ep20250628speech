"""
Востроизведение текстовых сообщений
"""

from gtts import gTTS
import pygame
import os
import time


def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Ждем окончания воспроизведения
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


SOUND_FILE_NAME = "output.mp3"
IS_DELETE_AFTER_PLAY = False
# text = b"\xd0\x9f\xd0\xbe\xd0\xb6\xd0\xb0\xd0\xbb\xd1\x83\xd0\xb9\xd1\x81\xd1\x82\xd0\xb0, \xd0\xb8\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5 \xd0\xbd\xd0\xb0\xd1\x85\xd1\x83\xd0\xb9!"
text = "Миля! Ты хочешь пешком пойти?"
language = "ru"


try:
    # tts = gTTS(text=text.decode("utf-8"), lang=language, slow=False)
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(SOUND_FILE_NAME)
    # os.system("start output.mp3")
    play_mp3(SOUND_FILE_NAME)
    if IS_DELETE_AFTER_PLAY is not False:
        time.sleep(1)
        os.remove(SOUND_FILE_NAME)

except Exception as err:
    raise err
