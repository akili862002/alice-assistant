import speech_recognition as sr
import time
import pyaudio
import struct
import math
import time

PATH_FILE = "DATABASE/result_listen.txt"
# Set recognize

# Clear everything
file = open(PATH_FILE, "w")
file.write("Clear")
file.close()

def get_status_of_main_program():
    file = open(PATH_FILE, "r")
    res = file.readlines()[0]
    file.close()
    return res

def listen_user():
    result = ""
    rec = sr.Recognizer()
    # Start listen user from Microphone --
    with sr.Microphone() as source:
        file = open(PATH_FILE, "w")
        file.write("[LISTENING][READY]")
        file.close()
        audio = rec.listen(source)

    # Convert audio data to text ---
    try:
        result = rec.recognize_google(audio)
    except:
        result = "[UNDEFINDED]"

    del rec
    # Save data:
    file = open(PATH_FILE, "w")
    file.write(result)
    file.close()

# ------- Main() --------
count = 0
run = True
while run:
    time.sleep(0.3)
    order_from_main_program = get_status_of_main_program()
    if order_from_main_program == "[START]":
        # print(" [ON]  Start listening --")
        listen_user()
        # print(" [OFF] Stop listening --")

    elif order_from_main_program == "[CLOSE_PROGRAM]":
        run = False
        # Change text in file, to make that, next run program will be shuted down
