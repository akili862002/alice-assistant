import argparse
import os, random, json
from playsound import playsound
from gtts import gTTS
import support as sp

pathFile = os.path.dirname(os.path.realpath(__file__))

def perfectString(s):
    s = s.lower()
    while "  " in s: s = s.replace("  ", " ")
    if len(s) > 0:
        while s[0] == " ": s = s[1:]
        while s[len(s)-1] == " ": s = s[:len(s) - 2]
    s = s.replace("-", " ")
    return s

def getDataJson():
    file = open(pathFile + "/Sounds/history.json", "rb")
    data = json.load(file)
    file.close()
    return data, list(data.keys()), list(data.values())

data, nameFile, texts = getDataJson()

def getDataCommunication(path):
    file = open(path, "rb")
    data = json.load(file)
    file.close()
    return data

communications = getDataCommunication(pathFile + "/DATABASE/communication.json")
events = getDataCommunication(pathFile + "/DATABASE/events.json")

ListJarvis = []
for jarvis in list(communications.values()):
    for text in jarvis["jarvis"]:
        text = text.replace(sp.sub_string_inside(text, '[', ']', True),"")

        for code in sp.get_all_code(text):
            # print("code: " + code)
            text = text.replace(code, "")

        list_text = text.split("<br/>")
        for text in list_text:
            text = perfectString(text)
            if text not in texts and text not in ListJarvis:
                ListJarvis.append(text)

for text in list(events.values()):
    text = perfectString(text)
    if text not in texts and text not in ListJarvis:
        ListJarvis.append(text)

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

    return nameFile

print("[INFO] Start render communication file: --")
count = 0
for text in ListJarvis:
    try:
        nameFile = createSound(text)
        count += 1
        persent = str(100*(count/len(ListJarvis)))[:5]
        print("  |-> {}% -- [{}] - ({})".format(persent, nameFile[nameFile.index("Sounds"):], text))
    except:
        print("[ERROR]: "+ text)

print("--> 100%")
print("[End] Done!")
saveDataJson(data)
wait = input("Press to end program!")
