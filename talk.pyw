import argparse
import os, random, json
from playsound import playsound
from gtts import gTTS

pathFile = os.path.dirname(os.path.realpath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--text", required=True, help="path to input image")
args = vars(ap.parse_args())

# Output file communication that is was WORKING

def perfectString(s):
    s = s.lower()
    while "  " in s: s = s.replace("  ", " ")
    if len(s) > 0:
        while s[0] == " ": s = s[1:]
        while s[len(s)-1] == " ": s = s[:len(s) - 2]
    s = s.replace("-", " ")
    return s

jarvis = perfectString(args["text"])

def getDataJson():
    file = open(pathFile + "/Sounds/history.json", "rb")
    data = json.load(file)
    file.close()
    return data, list(data.keys()), list(data.values())

data, nameFile, texts = getDataJson()

def saveDataJson(data):
    file = open(pathFile + "/Sounds/history.json", "w")
    json.dump(data, file, indent=4)
    file.close()

def createSound(text):
    global data
    tts = gTTS(text= text, lang='en')
    fileCode = str(random.randint(1,10000000))
    nameFile = pathFile + '/Sounds/' + fileCode + '.mp3'
    tts.save(nameFile)
    data[fileCode + '.mp3'] = text
    saveDataJson(data)
    return nameFile

if jarvis in texts:
    playsound(pathFile + "/Sounds/" + nameFile[texts.index(jarvis)])
else:
    nameFile = createSound(jarvis)
    playsound(nameFile)

# Output status: everything was done
file = open("DATABASE/Status.txt", "w")
file.write("[NO_WORKING]")
file.close()
