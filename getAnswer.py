import json, os, time
import difflib
from random import choice
import wikipedia
from control import*
import support as sp

# get real path of current file
pathFile = os.path.dirname(os.path.realpath(__file__))

# Some const:
month_Number = {"Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "May": "5",
                "Jun": "6", "Jul": "7", "Aug": "8", "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12"}

def getTime(TYPE):
    imfor = time.ctime()
    imformation = imfor.replace("  "," ").split()

    timeToday = imfor.replace(imformation[3]+ " ", "")
    ls = timeToday.split()
    day_month =  ls[2] + "/" + month_Number[ls[1]]
    result = {
        "time-now": imformation[3],
        "time-today": timeToday,
        "day-month": day_month,
        "day-of-week": ls[0]
    }
    return result[TYPE]

def convertTimeToSecond(t):
    ls = t.split(":")
    if len(ls) == 3:
        return int(ls[0])*3600 + int(ls[1])*60 + int(ls[2])
    else:
        return int(ls[0])*3600 + int(ls[1])*60

def getData_json(path):
    file = open(path, "rb")
    data = json.load(file)
    file.close()
    return data

def getNameFilesFromFolder(part):
    return os.listdir(part)

def talk(text):
    # Status that Jarvis is talking
    # print("[Jarvis] - say: ", text)
    if JARVIS_TALKING == ON:
        file = open("DATABASE/Status.txt", "w")
        file.write("[WORKING]")
        file.close()
        # print("python " + pathFile + "/talk.pyw --text " + '"{}"'.format(text))
        os.system("start " + pathFile + "/talk.pyw --text " + '"{}"'.format(text))

# ---------------- GET DATAS
print("[GetAnswer] Loading Data...", end = "")
try:
    communications = getData_json(pathFile + "/DATABASE/communication.json")
    songs = getNameFilesFromFolder("my_music")
    apps  = getNameFilesFromFolder("application")
    print(" -> DONE")
except:
    print("[WARNING!] DATABASE GOT ERROR!")
    print(" - PLEASE CHECK YOUR DATABASE THEN UPDATE SYSTEM!")
    print(" -> DONE")

# Compare all sentence with user_say
def getPersentOfSentence(userSay, userWord):
    # make sentence clear
    for i in [".", ",", "*", "?", "!", "~", "@", "#", "(", ")", "-"]:
        userSay = userSay.replace(i, " ")
        userWord = userWord.replace(i, " ")

    persent = 100
    # print(userWord)

    if userWord == "": return 0

    n = 100//len(userWord)
    goal = userWord.split(" ")
    user = userSay.split(" ")
    d = difflib.Differ()
    diffence = list(d.compare(userSay, userWord))
    for index in diffence:
        index = index.replace(" ",'')
        if '+' in index or '-' in index:
            persent -= n*len(index[1:])
    return persent

def sayHelloToUser():
    currentTime = convertTimeToSecond(getTime("time-now"))
    text = "Hello, there!"
    # Morning
    if convertTimeToSecond("3:00:00") <= currentTime <= convertTimeToSecond("8:00:00"):
        system("system.open.music(random)")
        text = choice(["Good Morning, sir. Have good day.", "Good morning. You should take a coffee!", "Good morning, Sir. Please wake up!, today gonna be a happy day!"])

    if convertTimeToSecond("8:00:00") <= currentTime <= convertTimeToSecond("12:00:00"):
        text =  choice(["Good Morning, sir."])

    if convertTimeToSecond("12:00:00") <= currentTime <= convertTimeToSecond("18:00:00"):
        text = choice(["Good Afternoon, sir. Let's do something!"])

    if convertTimeToSecond("18:00:00") <= currentTime <= convertTimeToSecond("24:00:00"):
        text = choice(["Good evening!"])

    eventToday = getEventOfToday()
    if eventToday != "<no_event>":
        text = eventToday

    return text

def getEventOfToday():
    timeToday = getTime("day-month")
    # timeToday = "8/6"
    file = open(pathFile + "/DATABASE/events.json", "rb")
    data = json.load(file)
    for day_month, sentence in data.items():
        if day_month == timeToday:
            return sentence
    return "<no_event>"


def openFile(path): #open
    path = path.replace("*",pathFile)
    os.system("start " + pathFile + "/openit.pyw --URL " + path)

def openWebsite(URL):
    os.system("start " + pathFile + "/openit.pyw --URL " + URL)

def getAnswerFromWikipedia(user):
    print("  $ - Searching Wikipedia...")
    if "what is " in user:
        ask = user[8:]
    elif "who is " in user:
        ask = user[7:]
    elif "do you know " in user:
        ask = user[12:]
    elif "where is " in user:
        ask = user[9:]

    try:
        result = wikipedia.summary(ask,1)
    except:
        result = "Sorry, I don't know that."

    result = result.replace("(listen)", "")

    return result

def system(code):
    global communications, songs, apps
    result = "Code error!"
    if "open" in code:
        if "music" in code: # MUSIC --------------------------------------------
            try:
                songUserWant = code[code.index("(")+1:code.index(")")].replace("-"," ").replace(".mp3", "")
                if songUserWant != "random": # open determined music
                    bestSearch = ""
                    maxPersent = 0
                    for song in songs:
                        songPredict = song.replace("-"," ").replace(".mp3", "")
                        persent = getPersentOfSentence(songUserWant.lower(), songPredict.lower())
                        if persent > maxPersent:
                            maxPersent = persent
                            bestSearch = song
                        if persent == 100: break
                    print(maxPersent)
                    if maxPersent == 100:
                        openFile(pathFile + "/my_music/" + bestSearch)
                        result = bestSearch + " is playing"
                    elif maxPersent > 60:
                        result = "Do you mean " + bestSearch + "? [yes/no->{system.open.music(%s)}]" % bestSearch
                    else: result = "Sorry, I cannot find your song."
                else: # open random music
                    song = choice(songs)
                    openFile(pathFile + "/my_music/" + song)
                    result = song + " is playing"
            except:
                result = "Check your code!"

        elif "app" in code: # open Application ------------------------------------------------
            try:
                appUserWant = code[code.index("(")+1:code.index(")")].replace("-"," ").replace(".lnk", "")
                bestSearch = ""
                maxPersent = 0
                for app in apps:
                    appPredict = app.replace("-"," ").replace(".lnk", "")
                    persent = getPersentOfSentence(appUserWant.lower(), appPredict.lower())
                    if persent > maxPersent:
                        maxPersent = persent
                        bestSearch = app
                    if persent == 100: break
                print(maxPersent, bestSearch)
                if maxPersent == 100:
                    openFile(pathFile + "/application/" + bestSearch)
                    result = bestSearch + " is opened"
                elif maxPersent > 60:
                    result = "Do you mean '" + bestSearch + "'? [yes/no->{system.open.app(%s)}]" % bestSearch
                else: result = "Sorry, I cannot find your app."
            except: # If error code
                result = "Check your code!"

        elif "website" in code: # Open Website -----------------------------------------------------------------
            try:
                URL = code[code.index("(")+1:code.index(")")]
                openWebsite(URL)
                result = "Opening your website!"
            except:
                result = "Check you URL!"
        elif "file" in code:
            try:
                URL = code[code.index("(")+1:code.index(")")]
                openFile(URL)
                result = ""
            except:
                result = "Something wrong with your path image!"

    elif ".update" in code:
        try:
            communications = getData_json("DATABASE/communication.json")
            songs = getNameFilesFromFolder("my_music")
            apps  = getNameFilesFromFolder("application")
            result = "Completely update!"
        except:
            result = "I got some bug in your database!"

    elif ".list" in code:
        if ".communication" in code:
            openFile(pathFile + "/DATABASE/communication.json")
        if ".app" in code:
            openFile(pathFile + "/application")
        if ".music" in code:
            openFile(pathFile +"/my_music")
        result = "This is yours..."
    return result

def perform(jarvis):
    if "{" in jarvis:
        code = jarvis[jarvis.index("{")+1:jarvis.index("}")]
        jarvis = jarvis.replace("{" + code + "}","")
        system(code)

    talk(jarvis)
    return jarvis


def remove_ignore_word(text):
    texts = text.split(" ")
    remove_word = ["please", "dude", "bro", "now", "right now", "alice", "today", "ok", "thank you", "thanks", "oh", "well", "okay", "okey", "i said", "i told", "i said that", "i told that"]
    for s in remove_word:
        if (text != s) and (s in texts):
            text = text.replace(s, "")

    return text

def get_INFO_of_user(user, search):
    search_list = search.split(" ")
    user_list = user.split(" ")

    text = user
    number_word_in_user = len(search_list)
    for word in search_list:
        # print(word)
        if (word in text):
            text = text.replace(word, "")
        else:
            number_word_in_user -= 1

    text = sp.delete_wrong_spaces_in_text(text)
    info = ""
    if (text in user) and (number_word_in_user/(len(user_list)) >= 0.5):
        info = text

    return info



def get_the_best_answer(user):
    t1 = time.time()
    user = remove_ignore_word(user)
    user = sp.beautiful_text(user, for_display=False)

    result = NOT_FOUND
    # get the best matching answer ---------
    maxPersent = 0
    for _, data in communications.items():
        for sentence in data["user"]:
            if "<a>" in sentence:
                # If this sentence have a code <a> mean just sentence appears in userSay,
                # it's ok, choose it.
                sentence = sentence.replace("<a>", "")
                sentence = sp.beautiful_text(sentence, for_display=False)
                if sentence in user:
                    # Choose a random answer ----
                    result = choice(data["jarvis"])

            persent = getPersentOfSentence(user.lower(), sentence.lower())
            if (persent > 70) and (persent > maxPersent):
                maxPersent = persent
                # Choose a random answer ----
                result = choice(data["jarvis"])
                if persent == 100:
                    break

            if "<info>" in sentence:
                info = get_INFO_of_user(user, sentence)
                if info != "":
                    print("  INFO = " + info)
                    result = choice(data["jarvis"])
                    result = result.replace("<info>", info)
                    break


    print("  <+> Best matching: [{}%] -- time_search: {:.5f}s".format(maxPersent, time.time()-t1))
    print("      (i) User: [%s]" % user)
    print("         -> Match: [%s]" % result)

    return result
