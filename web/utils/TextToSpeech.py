import os
import sys

import pyttsx3
import random


def gen_speech(speech_text):
    synthesizer = pyttsx3.init()
    random_int = random.randrange(0, sys.maxsize)
    synthesizer.save_to_file(speech_text, f'{os.getcwd()}/web/utils/synthesized/{random_int}.mp3')
    synthesizer.runAndWait()
    return f"{random_int}.mp3"


