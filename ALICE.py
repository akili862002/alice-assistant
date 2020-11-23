import pygame
import time, os
import random
import getAnswer
import numpy as np
import getAnswer
import schedule_2 as schedule

from control import*
from pygame.locals import*
import support as sp
# get real path of current file
pathFile = os.path.dirname(os.path.realpath(__file__))

pygame.init()

# Open listen file
print("[LISTEN] Start opening listen file")
getAnswer.openFile(pathFile + "/listen.pyw")

# -----------------------------
def resizeImage_W_H(img, rs):
    img = pygame.transform.scale(img, rs)
    return img

def resizeImage(img, toW):
    (w,h) = img.get_size()
    if w != toW:
        img = pygame.transform.rotozoom(img, 0, toW/w)
    return img

def loadImage(path, changeWidth=0):
    img = pygame.image.load(path)
    if changeWidth != 0: # equal 0 means that Don't need change size
        (w,h) = img.get_size()
        img = pygame.transform.rotozoom(img, 0, changeWidth/w)
    return img

# Get Images
def getListImages(path, length, resize):
    List = []
    for i in range(length + 1):
        count = "0000" + str(i)
        if "$$$" in path:
            count = count[len(count)-3:]
            img = pygame.image.load(path.replace("$$$", count))
        elif "$$" in path:
            count = count[len(count)-2:]
            img = pygame.image.load(path.replace("$$", count))
        # resize img
        if resize != 0:
            img = resizeImage(img, resize)
        List.append(img)
    return List

# ---------- LOADING IMAGES ---------------------------------------------- ....
print("[SYSTEM] Start getting images...", end = "")
# $$$ is mean number of path
hud_circle = getListImages(pathFile + "/images/Soul/frame_$$$_delay-0.03s.gif", length=155, resize=0)
listening_circle = getListImages(pathFile + "/images/listening/frame_$$$_delay-0.04s.gif", length=100, resize=300)
listen_Alert_img = {
                        "box":  loadImage("images/Alert/Listen/alertBox.png"),
                        "text": loadImage("images/Alert/Listen/ListenAlert.png")
                   }
error_Alert_img = {
                       "box":  loadImage("images/Alert/Error/Alert_box.png"),
                       "text": loadImage("images/Alert/Error/text.png")
                   }
bar_shape = {
                "ON":    loadImage("images/Alert/shape/bar_ON.png", changeWidth=444),
                "OFF":   loadImage("images/Alert/shape/bar_OFF.png", changeWidth=444),
                "border":loadImage("images/Alert/shape/border.png", changeWidth=444),
                "half":loadImage("images/Alert/shape/half_bar.png", changeWidth=444*90//239)
            }

back_button = {
                "ON": loadImage("images/button/back_on.png", changeWidth=70),
                "OFF":loadImage("images/button/back_off.png", changeWidth=70)
              }
(back_button["w"], back_button["h"]) = back_button["ON"].get_size()

recycle_icon = {
                "ON": loadImage("images/icon/recycle_on.png", changeWidth=40),
                "OFF": loadImage("images/icon/recycle_off.png", changeWidth=40)
                }
(recycle_icon["w"], recycle_icon["h"]) = recycle_icon["ON"].get_size()


print(" -> Done")
# -----------------------------------

# Create screen ... -------------- <. <. <. <. <.
fpsClock = pygame.time.Clock()

(wScr, hScr) = (700, 400)
win = pygame.display.set_mode((wScr, hScr))
pygame.display.set_caption("ALICE - Assistant")
pygame.display.set_icon(pygame.image.load(pathFile + "/images/icon/icon1.png"))


# ------------------- Functions -------------------------------------- .....
def getTime(TYPE): #getTime
    imfor = time.ctime()
    imformation = imfor.split()
    clock = imformation[3].split(":")
    result = {
        "time-now": imformation[3],
        "time-today": imfor.replace(imformation[3]+" ", ""),
        "hour-minute": "{}:{}".format(clock[0],clock[1])
    }
    return result[TYPE]

def convertTimeToSecond(t):
    ls = t.split(":")
    if len(ls) == 3:
        return int(ls[0])*3600 + int(ls[1])*60 + int(ls[2])
    else:
        return int(ls[0])*3600 + int(ls[1])*60

def get_length_of_mp3(path):
    # Load imformation of file
    audio = MP3("my_music/go-again.mp3")
    return int(audio.info.length)

def perfectText(text):
    while "  " in text: text = text.replace("  ", " ")
    if text == " ": text = ""
    if len(text) > 0:
        while text[0] == " ": text = text[1:]
        text = text[0].upper() + text[1:]
    # while text[len(text)-1] == " ": text = text[:(len(text)-2)]
    return text

def showSingleText(text, local, color, size, font, isMid=False):
    font = pygame.font.SysFont(font, size)
    textIMG = font.render(text, True, color)
    if not isMid:
        win.blit(textIMG, local)
    else:
        (w, h) = textIMG.get_size()
        win.blit(textIMG, (wScr//2 - w//2, hScr//2 - h//2))

def getSizeText(text, size, font):
    font = pygame.font.SysFont(font, size)
    textIMG = font.render(text, True, (0 , 0, 0))
    return textIMG.get_size()

def checkSize(text, size, font, width):
    font = pygame.font.SysFont(font, size)
    textIMG = font.render(text, True, (0, 0, 0))
    if textIMG.get_width() > width:
        return False
    else: return True

def createTransparentRect(size, color, alpha):
    s = pygame.Surface(size)  # the size of your rect
    s.set_alpha(alpha)        # alpha level
    s.fill(color)             # this fills the entire surface
    return s
diaphragm = createTransparentRect((wScr, hScr), (0, 0, 0), 150)

def split_text(s, limitLengthString):
    texts = []
    i = limitLengthString

    if i >= len(s): # if i >= len(s) then we needn't split it. Return it
        texts = [s]
    else:
        while i < len(s):
            # Find space to split text
            pos = i
            while s[i] != " ":
                i -= 1
                if i == 0:  # if text have a big word. then just split this word
                    i = pos
                    break
            # Append tick to string. to split
            s = s[:i] + NOTE_CUT + s[i+1:]
            i += limitLengthString
        # Split text to create list text with NOTE_CUT was tick before
        texts = s.split(NOTE_CUT)

        if len(texts) > 2: texts = ["..." + texts[len(texts)-2], texts[len(texts)-1]]
    return texts

def createImageFromText(text, size, color, font):
    font = pygame.font.SysFont(font, size)
    Image = font.render(text, True, color)
    return Image

def show_text_with_font(text, pos, color, font):
    Image = font.render(text, True, color)
    win.blit(Image, pos)

def createImageFromText_font(text, color, font):
    return font.render(text, True, color)

def jarvis_stop_saying():
    # This file and talk.py communicate
    try:
        file = open("DATABASE/Status.txt", "r")
        status = file.readlines()[0]
        file.close()
        cannot_read_file = False
    except: # If that try to read file is Fail, retun False for next turn try
        return False

    # print(status)
    if status == "[WORKING]":
        return False
    elif status == "[NO_WORKING]":
        return True

def system(code):  #system
    global runProgram, JARVIS_LISTEN, JARVIS_TALKING
    print("  => [CODE SYS]: " + code)
    codes = sp.get_all_code(code)
    for code in codes:
        if "change" in code:
            if ".title" in code:
                new_title = sp.get_code(code, '(', ')')
                main_title_mid.change_text(new_title)
            elif ".icon" in code:
                new_title = sp.get_code(code, '(', ')')
                main_title_mid.change_icon(new_title)
        elif "voice" in code:
            if ".off" in code:
                JARVIS_TALKING = OFF
            elif ".on" in code:
                JARVIS_TALKING = ON
        elif "listen" in code:
            if ".off" in code:
                JARVIS_LISTEN = OFF
            elif ".on" in code:
                JARVIS_LISTEN = ON
            elif ".start" in code:
                listen.start()
                alert_listening.reset()

        elif "mission" in code: #sys.mission
            if ".on" in code:
                aboard_duty.start()
            elif ".off" in code:
                aboard_duty.close()
            elif "get_next_plan" in code:
                aboard_duty.next_plan()

        elif "countdown" in code:
            if ".start" in code:
                tm = sp.get_code(code, '(', ')')
                countDown.start(tm)
            elif ".pause" in code:
                print("pause-----")
                countDown.pause()
            elif ".resume" in code:
                countDown.resume()
            elif ".stop" in code:
                countDown.stop()
        elif "get" in code:
            if ".time" in code:
                animation_text.change([sp.get_perfect_time(currentTime)])
                main_title_mid.change_text("<clock>")

        elif "close_program" in code:
            runProgram = False
        elif "shut_down_computer" in code:
            # turn off all programs are running
            for program in ["chrome.exe", "atom.exe", "opera.exe"]:
                os.system("TASKKILL /F /IM " + program)

            time_countDown = sp.get_code(code, '(', ')')
            os.system("shutdown -s -t " + time_countDown)
            runProgram = False


        else: # If in this code in main_file have no function, Use it for getAnswer
            getAnswer.system(code)
# Class region ------------------ -- -- - - -
class gif(object):  #gif
    def __init__(self, images, local ,startCount):
        self.images = images
        (self.real_x, self.real_y) = local
        (self.x, self.y) = local
        (self.w, self.h) = hud_circle[0].get_size()
        (self.x_mid, self.y_mid) = (self.x + self.w//2, self.y + self.h//2)
        self.move = 0
        self.count = startCount
        self.isMove = False
        self.degree = 90
        self.direct = 0


    def move_left(self, new_pos_x, speed=2):
        self.isMove = True
        self.direct = LEFT
        self.height_line = abs(new_pos_x - self.x)
        self.degree = 90
        self.speed = speed

    def move_mid(self):
        self.isMove = True
        self.direct = RIGHT
        if self.degree <= 0:
            self.degree = 90

    def draw(self):
        self.count += 30/FPS
        if self.count >= len(self.images):
            self.count = 0

        # Moving process:
        if self.isMove:
            # self.degree -= self.speed
            if self.degree > 0:
                self.degree -= self.speed
            else:
                self.isMove = False

            angle = PI*self.degree/180
            self.move = int(self.height_line*np.cos(angle))*self.direct

        if self.direct == LEFT:
            self.x = self.real_x + self.move
        elif self.direct == RIGHT:
            self.x = self.real_x - self.height_line + self.move//2

        (self.x_mid, self.y_mid) = (self.x + self.w//2, self.y + self.h//2)
        # Draw ----
        try:
            win.blit(self.images[int(self.count)], (self.x, self.real_y))
        except:
            print("Fail with:", self.count, int(self.count))

class alert(object):
    def __init__(self, img, imgAfter, position, isMid=False, speed=3):
        self.img = img
        self.imgAfter = imgAfter
        (self.wImg, self.hImg) = img.get_size()
        if isMid == False:
            self.pos = position
        else: self.pos = [wScr//2, hScr//2 - self.hImg//2]
        self.time = time

        # We use circle Cos to show animation.
        #Speed of box appears Slow down, so degree decrease --
        self.degree = 0
        self.speed = speed
        self.type = DISAPPEARANCE

    def persent(self):
        return (90-self.degree)/90

    def status(self):
        return self.type

    def reset(self):
        self.degree = 90

    def draw(self, TYPE):
        # increase half size of alert box and resize
        self.type = TYPE # get current type of function
        if TYPE == OPEN:
            win.blit(diaphragm, (0, 0))
            if self.degree > 0:
                self.degree -= self.speed
                angle = PI*self.degree/180
                width = int(self.wImg*np.cos(angle))

                outputImg = pygame.transform.scale(self.img, (width, self.hImg))
                # change x position
                self.pos[0] = wScr//2 - width//2
            else:
                outputImg = self.img
                self.pos[0] = wScr//2 - self.wImg//2

            # Draw alert box
            win.blit(outputImg, self.pos)
            if self.degree <= 0:
                (w, h) = self.imgAfter.get_size()
                win.blit(self.imgAfter, (wScr//2 - w//2, hScr//2 - h//2))

        else:# TYPE == CLOSE ---
            if self.degree > 0:
                self.degree -= self.speed
                angle = PI*self.degree/180
                width = int(self.wImg*(1 - np.cos(angle)))
                outputImg = pygame.transform.scale(self.img, (width, self.hImg))
                # change x position
                self.pos[0] = wScr//2 - width//2
            else:
                outputImg = self.img
                self.pos[0] = wScr//2 - self.wImg//2
            # Draw alert box
            if self.degree > 0:
                win.blit(outputImg, self.pos)

            # Update status when it close
            if self.degree <= 0:
                self.type = DISAPPEARANCE

class showText(object):
    def __init__(self, text, position, sizeBreak, font, color, isMid=False, limitLengthString=50):
        self.text = text
        (self.x, self.y) = position
        self.font = font
        self.color = color
        self.isMid = isMid
        self.sizeBreak = sizeBreak
        self.limitLengthString = limitLengthString
        self.time_appear = -1 #-1 is mean always appear

        # to break sentence
        self.texts = split_text(text, self.limitLengthString)
        self.images = []
        # Create images
        for string in self.texts:
            if string != "":
                img = createImageFromText(string, size, color, font)
                self.images.append(img)

        # if break size is negative, that means belonger is user
        self.belonger = JARVIS if sizeBreak > 0  else USER

    def change_text(self, newText, time_appear=-1):
        # just new Text then create new img list. To optimize system
        if newText != self.text:
            self.texts = split_text(newText, self.limitLengthString)
            self.images = []
            for string in self.texts:
                # img = createImageFromText(string, self.size, self.color, self.font)
                img = createImageFromText_font(string, self.color, self.font)
                self.images.append(img)

        self.text = newText
        if time_appear != -1:
            self.time_appear = time_appear

    def showShape(self, start, end):
        width = 8
        w = 5*len(self.texts) + width//2
        h = end["y"] - start["y"] + width
        color = (54, 188, 201)

        # Line Left: -----
        #   Top:
        pygame.draw.line(win, color, (start["x"] - width//2, start["y"] - width//2), (start["x"] - width//2 + w, start["y"] - width//2), width)
        #   Bot:
        pygame.draw.line(win, color, (start["x"] - width//2, end["y"] + width//2), (start["x"] - width//2 + w, end["y"] + width//2), width)
        #   Mid:
        pygame.draw.line(win, color, (start["x"] - width, start["y"] - width + 1), (start["x"] - width, end["y"] + width), width)

        # Line Right: -----
        #   Top:
        pygame.draw.line(win, color, (end["x"] + width//2, start["y"] - width//2), (end["x"] + width//2 - w, start["y"] - width//2), width)
        #   Bot:
        pygame.draw.line(win, color, (end["x"] + width//2, end["y"] + width//2), (end["x"] + width//2 - w, end["y"] + width//2), width)
        #   Mid:
        pygame.draw.line(win, color, (end["x"] + width, start["y"] - width + 1), (end["x"] + width, end["y"] + width), width)

        # Test rectangle
        # pygame.draw.rect(win, (255, 255, 255), (start["x"], start["y"], end["x"] - start["x"], end["y"] - start["y"]), 2)

    def draw(self):
        if self.time_appear != -1:
            if self.time_appear > 0:
                self.time_appear -= 1
            else:
                self.time_appear = -1 # Reset
                self.text = ""

        if self.text != "": # if empty, not showing
            yPos = self.y
            sizeBreak = self.sizeBreak
            x_min = wScr
            y_min = hScr

            # If output text is bot, Fliping that
            if self.sizeBreak < 0:
                yPos -= (len(self.texts)-1)*(-self.sizeBreak)
                sizeBreak = -self.sizeBreak

            for img in self.images:
                if self.isMid:
                    (w,h) = img.get_size()
                    xPos = wScr//2 - w//2
                    win.blit(img, (xPos, yPos))
                    # update minimum of x position
                    x_min = min(x_min, xPos)
                else:
                    win.blit(img, (self.x, yPos))
                # Update minimum of y position
                y_min = min(y_min, yPos)
                # Update new y_position when <break line>
                yPos += sizeBreak

            # Draw Shape around text ----
            if self.isMid:
                if self.belonger == USER:
                    start = {"x": x_min, "y": y_min}
                    end = {"x": wScr//2 + (wScr//2 - x_min), "y": self.y + 25}
                    self.showShape(start, end)
                else: # Jarvis
                    start = {"x": x_min, "y": y_min}
                    end = {"x": wScr//2 + (wScr//2 - x_min), "y": yPos}
                    self.showShape(start, end)

class listenFunction(object): #listen
    def __init__(self):
        self.isListening = DISAPPEARANCE
        self.text = ""
        self.PATH_FILE_GET_RESULT = pathFile + "/DATABASE/result_listen.txt"
        self.ready = False

    def start(self):
        print("   [+] Listen: ON")
        # Put result in it!
        file = open(self.PATH_FILE_GET_RESULT, "w")
        file.write("[LISTENING]")
        file.close()

        # Open file listen.pyw to get voice, and convert to text. When it got a text, saving it in a file result.
        if JARVIS_LISTEN:
            # Order with listen file that main program will be on listen mode
            file = open(self.PATH_FILE_GET_RESULT, "w")
            file.write("[START]")
            file.close()
        self.isListening = ON

    def stop(self):
        print("   [-] Listen: OFF")
        # if press Stop listen, we close listen.pyw program
        # os.system("TASKKILL /F /IM listen.pyw") # code to call system, stop this file
        file = open(self.PATH_FILE_GET_RESULT, "w")
        file.write("[UNDEFINDED]")
        file.close()
        self.isListening = OFF

    def get_result(self):
        try:
            file = open(self.PATH_FILE_GET_RESULT, "r")
            result = file.readlines()[0]
            file.close()
        except:
            result = "[LISTENING]"

        if ("[LISTENING]" not in result) and ("[START]" not in result): # if listening was DONE or FAIL, getting text
            self.isListening = OFF
            self.ready = False
            print("   [-] Listen: OFF")
            if result != "[UNDEFINDED]":
                self.text = result
                return result
            else:
                self.text = result
                print("     [Notice] Fail --")
                return "[FAIL]"
        else:
            if "[READY]" in result:
                self.ready = True
            return "NONE"

class titleFunction(object): #title
    def __init__(self, text):
        self.text = text
        self.text_bot = ""
        self.text_top = ""
        # self.main_title = createImageFromText(self.text, 50, (19, 209, 198), "Berlin Sans FB Demi")
        self.main_title = createImageFromText_font(self.text, (19, 209, 198), FONT_AldotheApache["60"])
        self.img = self.main_title
        self.img_bot = None
        self.list_img = []
        (w,h) = self.img.get_size()
        self.pos = (wScr//2 - w//2, hScr//2 - h//2)
        self.count = 0
        self.is_change_title = False

    def change_text(self, newTitle, size=40, time_change=4):
        if newTitle.lower() != "alice":
            if newTitle != self.text:
                self.text = newTitle
                self.img = createImageFromText(self.text, size, (255, 255, 255), "Century Gothic")
        else:
            self.img = self.main_title
            self.text = "alice"
            self.text_bot = ""
            self.text_top = ""

        (w,h) = self.img.get_size()
        self.pos = (soulOfJarvis_gif.x_mid - w//2, soulOfJarvis_gif.y_mid - h//2)
        # Reset
        self.is_change_title = True
        self.count = time_change*FPS

    def change_text_bot(self, text):
        if self.text_bot != text:
            self.text_bot = text
            self.img_bot = createImageFromText_font(text, (200, 200, 200), FONT_Century_Gothic["20"])

    def change_icon(self, path_icon, time_change=4):
        self.img = loadImage(path_icon, size)
        (w,h) = self.img.get_size()
        self.pos = (soulOfJarvis_gif.x_mid - w//2, soulOfJarvis_gif.y_mid - h//2)
        #Reset
        self.is_change_title = True
        self.count = time_change*FPS

    def draw(self):

        # Update title:
        if self.text == "<clock>":
            self.img = createImageFromText(currentTime, 40, (255, 255, 255), "Century Gothic")

        if self.is_change_title:
            if self.count > 0:
                self.count -= 1
            else:
                self.is_change_title = False
                # Reset title return
                self.img = self.main_title
                self.text = "alice"
                self.text_bot = ""
                self.text_top = ""
        # Big mid title
        (w,h) = self.img.get_size()
        self.pos = (soulOfJarvis_gif.x_mid - w//2, soulOfJarvis_gif.y_mid - h//2)
        win.blit(self.img, self.pos)
        # Small bot title
        if (self.text_bot != "") and (self.img_bot != None):
            (w,h) = self.img_bot.get_size()
            pos = (soulOfJarvis_gif.x_mid - w//2, soulOfJarvis_gif.y_mid + h*2//3)
            win.blit(self.img_bot, pos)

class time_table(object): #timetable #duty #mission
    def __init__(self):
        # schedule.missions = schedule.missions
        # self.status = schedule.status
        # self.times = schedule.status
        # Just use anything from schedule file, so we don't need to make a new var
        self.current_line = schedule.get_current_line()
        self.is_show = False
        self.display_texts = schedule.get_missions_appearence_by_current_line(self.current_line, schedule.missions)
        self.pos = [(280, 95),(300, 135),(316, 182),(300, 240),(280, 280)]
        self.size = [20, 26, 34, 26, 20]
        self.color = [(145, 145, 145),(218, 218, 218),(255, 255, 255),(218, 218, 218),(145, 145, 145)]
        self.title = "Today"

        self.count_animation = 0
        self.count =0
    def get_new_display_list(self):
        if mouse_type == DOWN:
            if self.current_line < len(schedule.missions)-1:
                self.current_line += 1
                self.display_texts = schedule.get_missions_appearence_by_current_line(self.current_line, schedule.missions)

        elif mouse_type == UP:
            if self.current_line > 0:
                self.current_line -= 1
                self.display_texts = schedule.get_missions_appearence_by_current_line(self.current_line, schedule.missions)


    def start(self):
        if self.is_show != True:
            # Move big mid circle to left to make room for texts
            soulOfJarvis_gif.move_left(-60, speed=1.6)

            self.is_show = True
            self.display_texts = schedule.get_missions_appearence_by_current_line(self.current_line, schedule.missions)
            self.current_line = schedule.get_current_line()

            #Reset animation
            self.count_animation = 0
            self.n = 0

    def close(self):
        if self.is_show != False:
            soulOfJarvis_gif.move_mid()
            self.is_show = False
            main_title_mid.change_text("ALICE")

    def next_plan(self):
        animation_text.change([schedule.get_next_plan()])

    def change_title(self):
        time_line = schedule.times[self.current_line].split("-") # startTime -> endTime or just startTime

        time_left_num = sp.convertTimeToSecond(time_line[0]) - sp.convertTimeToSecond(currentTime)
        time_left_text = sp.convertSecondToTime_text(time_left_num)

        if time_left_num >= 0:
            main_title_mid.change_text(schedule.times[self.current_line].split("-")[0])
            main_title_mid.change_text_bot(time_left_text + " left")
        else:
            # 2 case, one is during and one was done
            # if currentTime is time which happening
            if (len(time_line)==2) and (sp.compare_time(currentTime, time_line[1]) == LESS_THAN):
                main_title_mid.change_text("Currently")
                main_title_mid.change_text_bot(schedule.times[self.current_line])
            else: # or Done
                main_title_mid.change_text("Done")
                main_title_mid.change_text_bot(schedule.times[self.current_line])

    def show_figure_hide_sentence_top(self):
        num = (self.current_line-2)
        num_text = '(' + str(num) + ')'
        if num > 0:
            show_text_with_font(num_text, (265, 70), (145, 145, 145), FONT_TypoSlab_Irregular_Demo["20"])

    def show_figure_hide_sentence_bot(self):
        num = (len(schedule.missions) - self.current_line - 3)
        num_text = '(' + str(num) + ')'
        if num > 0:
            show_text_with_font(num_text, (265, 310), (145, 145, 145), FONT_TypoSlab_Irregular_Demo["20"])

    def show_all_sentences_in_list_missions(self):
        for i in range(self.n):
            if self.display_texts[i] != HIDE_TEXT:
                show_text_with_font(self.display_texts[i], self.pos[i], self.color[i], FONT_TypoSlab_Irregular_Demo[str(self.size[i])])

    def show_back_button(self, pos):
        if (pos[0] < xMouse < pos[0] + back_button["w"]) and (pos[1] < yMouse < pos[1] + back_button["h"]):
            win.blit(back_button["ON"], pos)
            if isClick:
                self.close()
        else:
            win.blit(back_button["OFF"], pos)

    def draw(self):  #time table draw
        if self.is_show:
            main_title_mid.change_text(self.title)
            self.get_new_display_list()

            # Draw all missions out screen
            # If big mid title didn't move
            if not soulOfJarvis_gif.isMove:

                # Start count to appear all sentences to screen
                if self.count_animation <= 50:
                    self.count_animation += 1
                    self.n = self.count_animation//10
                    if self.display_texts[self.n-1] == HIDE_TEXT:
                        self.count_animation += 10

                self.show_all_sentences_in_list_missions()

                # Show number of missions are being hiden
                if self.n == 5: # if animation was done
                    self.change_title()
                    self.show_figure_hide_sentence_top()
                    self.show_figure_hide_sentence_bot()

                self.show_back_button(pos=(590, 49))



class text_process():
    def __init__(self):
        self.texts = []
        self.current_text = ""
        self.count = 0
        self.run_word = 0
        self.speed = 0.5
        self.time_appear = 0
        self.time_limit_appear = 5*60

    def remove_code(self, s):
        code = sp.sub_string_inside(s, '{', '}', get_bracket=True)
        # Apply this code for System --
        system(code)
        return s.replace(code, "")

    def change(self, newList):
        # Make newList beautiful text
        for i in range(len(newList)):
            newList[i] = sp.beautiful_text(newList[i])
            print(newList)

        # print((self.count,len(self.texts)-1), (self.run_word,len(self.current_text) - 1))
        if newList != ['']:
            if (self.count < len(self.texts)-1) or (self.run_word < len(self.current_text)-1):
                self.texts += newList
            else:
                self.time_appear = 0
                self.texts = newList
                self.current_text = self.remove_code(newList[0])
                self.count = 0
                self.run_word = 0
                getAnswer.talk(self.current_text)
                history.add(self.current_text, JARVIS)
                print()
                print(self.texts, self.current_text)

    def process(self):
        if self.run_word < len(self.current_text):
            self.run_word += self.speed
            jarvis.change_text(self.current_text[:int(self.run_word)])
            self.time_appear = 0
        elif self.count < len(self.texts)-1:
            if jarvis_stop_saying():
                self.count += 1
                self.current_text = self.remove_code(self.texts[self.count])
                self.run_word = 0
                getAnswer.talk(self.current_text)
                history.add(self.current_text, JARVIS)
                self.time_appear = 0
        else:
            if self.time_appear < self.time_limit_appear:
                self.time_appear += 1
            else:
                jarvis.change_text("")
        # print((self.count,len(self.texts)-1), (self.run_word,len(self.current_text) - 1))

class communication_user_and_jarvis(object):
    def __init__(self):
        self.current_answer = ""
        self.list_next_answer = ["[EMPTY]"]

    def is_next_answer(self):
        if self.list_next_answer == ["[EMPTY]"]:
            return False
        return True

    def input(self, user_text):
        user_text = user_text.lower()
        history.add(user_text)
        if not self.is_next_answer():
            raw_answer = getAnswer.get_the_best_answer(user_text)
            self.list_next_answer = sp.split_text(sp.sub_string_inside(raw_answer, '[', ']'))
            self.current_answer = raw_answer.replace(sp.sub_string_inside(raw_answer, '[', ']', get_bracket=True), "")
        else:
            is_got_answer = False
            for situation in self.list_next_answer:
                code = sp.get_code(situation, '(', ')') # "(yes)->abcddasd" ----> "yes"
                print("CODE: " + code)
                print(code == "_")
                if code == "y":
                    # print(user_text, self.is_user_accept(user_text))
                    if sp.is_user_accept(user_text):
                        is_got_answer = True
                        raw_answer = sp.sub_string_inside(situation, '[', ']')
                        self.current_answer = raw_answer.replace(sp.sub_string_inside(raw_answer, '[', ']', True), "")
                        self.list_next_answer = sp.split_text(sp.sub_string_inside(raw_answer, '[', ']'))
                        break
                elif code == "n":
                    if sp.is_user_refuse(user_text):
                        is_got_answer = True
                        raw_answer = sp.sub_string_inside(situation, '[', ']')
                        self.current_answer = raw_answer.replace(sp.sub_string_inside(raw_answer, '[', ']', True), "")
                        self.list_next_answer = sp.split_text(sp.sub_string_inside(raw_answer, '[', ']'))
                        break
                elif code == "_":
                    is_got_answer = True
                    raw_answer = sp.sub_string_inside(situation, '[', ']')
                    self.current_answer = raw_answer.replace(sp.sub_string_inside(raw_answer, '[', ']', True), "")
                    self.list_next_answer = sp.split_text(sp.sub_string_inside(raw_answer, '[', ']'))
                    break
                elif (code != ""):
                    codes = code.split(",") # '(yes,please,yeah)' -> ['yes','please','yeah']
                    if (sp.is_exit_in_string(codes, user_text)):
                        is_got_answer = True
                        raw_answer = sp.sub_string_inside(situation, '[', ']')
                        self.current_answer = raw_answer.replace(sp.sub_string_inside(raw_answer, '[', ']', True), "")
                        self.list_next_answer = sp.split_text(sp.sub_string_inside(raw_answer, '[', ']'))
                        break

            if not is_got_answer: # if user neither agreed nor refused, get a new text
                raw_answer = getAnswer.get_the_best_answer(user_text)
                self.list_next_answer = sp.split_text(sp.sub_string_inside(raw_answer, '[', ']'))
                self.current_answer = raw_answer.replace(sp.sub_string_inside(raw_answer, '[', ']', get_bracket=True), "")

        # If we cannot find any answer ->
        if self.current_answer == NOT_FOUND:
            self.current_answer = random.choice(["I'm not getting that", "What do you mean?", "Sorry, I didn't catch on that", "What does this mean?"])

        # Process with main Alice
        if "<br/>" in self.current_answer:
            list_current_answer = self.current_answer.split("<br/>")
        else:
            list_current_answer = [self.current_answer]


        animation_text.change(list_current_answer)

class count_down_time(object):
    def __init__(self):
        self.setTime = 0
        self.time_left = 0
        self.is_counting = False
        self.is_pause = False
    def start(self,setTime):
        self.time_left = getAnswer.convertTimeToSecond(setTime)*FPS # *FPS mean, each frame, time will be dec
        self.setTime = self.time_left
        self.is_counting = True
    def stop(self):
        self.is_counting = False
        self.is_pause = False
        main_title_mid.change_text("Stop")
    def pause(self):
        self.is_counting = False
        self.is_pause = True
    def resume(self):
        self.is_counting = True
        self.is_pause = False
    def draw(self):
        if self.is_counting:
            self.time_left -= 1
            if self.time_left > 0:
                second = self.time_left//FPS
                text = sp.convertSecondToTime_text(second)
                if self.time_left == self.setTime//2:
                    animation_text.change(["Half time!"])
                elif self.time_left == 30*60*FPS:
                    animation_text.change(["You have 30 minutes left!"])
                elif self.time_left == 10*60*FPS:
                    animation_text.change(["You have 10 minutes left!"])
                elif self.time_left == 5*60*FPS:
                    animation_text.change(["5 minutes left!"])
                elif self.time_left == 60*FPS:
                    animation_text.change(["You have 1 minutes left!, please quickly."])
                elif self.time_left == 5*FPS:
                    animation_text.change(["5 seconds!"])
            else:
                self.is_counting = False
                text = "Time over!"
                animation_text.change(["Time is over!. Please stop anything you do."])
            # Change title ---
            main_title_mid.change_text(text)
            main_title_mid.change_text_bot(str((1 - self.time_left/self.setTime)*100)[:4]+"%")
        elif self.is_pause:
            main_title_mid.change_text("Pause")

class history_function(object):
    def __init__(self):
        self.history_user = []
        self.history_jarivs = []
    def add(self, text, whose=True): # that whose=True means USER
        if whose == USER:
            self.history_user.append(text)
        else:
            self.history_jarivs.append(text)
    def get_last_word(self, whose=True): # that whose=True means USER
        if whose == USER:
            return self.history_user[len(self.history_user)-1]
        else:
            return self.history_jarivs[len(self.history_jarivs)-1]

#    ---- object ---- #class
soulOfJarvis_gif = gif(hud_circle, (wScr//2 - hud_circle[0].get_width()//2, 30), startCount=138)
main_title_mid = titleFunction("A.L.I.C.E")
main_title_mid.change_text("Hi", size=50)
listen_gif = gif(listening_circle, (wScr//2 - listening_circle[0].get_width()//2, 338), startCount=0)
alert_listening = alert(listen_Alert_img["box"], listen_Alert_img["text"], (0,0), isMid=True, speed=3)
alert_error = alert(error_Alert_img["box"], error_Alert_img["text"], (0,0), isMid=True, speed=3)

user = showText("", (0,hScr - 50), -25, FONT_QuickSand["25"], (255, 255,255), isMid=True)
jarvis = showText("", (0, 10), 25, FONT_QuickSand["25"], (67, 226, 192), isMid=True)
listen = listenFunction()
animation_text = text_process()
aboard_duty = time_table()
communication = communication_user_and_jarvis()
countDown = count_down_time()
history = history_function()
# -----------------------------------< MAIN PROCESS >-----------------------------------
animation_text.change([getAnswer.sayHelloToUser(), "Sir. Here is your works of today!{mission.on}"])
text = ""
last_remind = ""
countdown_to_optimize_FPS = 60*FPS # 1 minute

runProgram = True
while runProgram:
    if countdown_to_optimize_FPS > 0:
        if FPS == 30:
            print(" [ACTIVE] Recognize user's action")
            print("    -> Return high FPS = 60")
        FPS = 60
        active_on_program = True
        countdown_to_optimize_FPS -= 1
    else: # mean in a moment, it will
        FPS = 30
        active_on_program = False
        aboard_duty.close()
    # print(countdown_to_optimize_FPS)

    currentTime = getTime("time-now")
    # Remind User: ---
    if convertTimeToSecond(currentTime) % 60 == 0:
        remind = schedule.remind_user(currentTime)
        if (remind != "") and (last_remind != remind):
            animation_text.change([remind])
            last_remind = remind

    Press_Space = False
    isClick = False
    mouse_type = NONE
    keyDown = False
    for event in pygame.event.get():
        # print(event.type == ACTIVEEVENT)
        if event.type == QUIT:
            runProgram = False
        if (event.type == ACTIVEEVENT) or (event.type == KEYDOWN):
             # If user is opening countdown mode, so don't do it
            countdown_to_optimize_FPS = 60*FPS # 1 minute


        if event.type == MOUSEMOTION:
            (xMouse, yMouse) = event.pos
        if event.type == MOUSEBUTTONDOWN:
            isClick = True
            mouse_type = event.button
            print("  |>> Mouse: ",(xMouse, yMouse), event.button)

        # get text from KEYBOARD:
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                # input user say to communication process
                communication.input(text)
                pressEnter = True
                text = ""

            elif event.key == K_BACKSPACE:
                text = text[:-1]
            elif listen.isListening != ON:
                text += event.unicode
            keyDown = True

            user.change_text(perfectText(text))
            # Get space key
            if event.key == K_SPACE:
                Press_Space = True

        # --------
    # Screen process ------------------------------ >>>>>>>
    win.fill((0, 0, 0)) # Black color for background
    soulOfJarvis_gif.draw()
    main_title_mid.draw()

    user.draw()
    jarvis.draw()

    if aboard_duty.is_show:
        aboard_duty.draw()

    # Turn on or OFF Listen mode--
    if (Press_Space) and (perfectText(text) == ""):
        if (listen.isListening == OFF) or (listen.isListening == DISAPPEARANCE):
            listen.start()
        else:
            listen.stop()
        # reset degree of object. Because of using Cos() to animate shape!
        alert_listening.reset()


    if listen.isListening == ON: # if system was listening
        # alert_listening.draw(OPEN)
        main_title_mid.change_text("Listening")
        if listen.ready:
            listen_gif.draw()
        result = listen.get_result()

        # If Jarvis can hear something from user ->
        if (result != "NONE") and (result != "[FAIL]"):
            text = ""
            communication.input(result)
            user.change_text(result, time_appear=120)
            alert_listening.reset()
            main_title_mid.change_text("ALICE")

        if result == "[FAIL]": # this is mean, Jarvis cannot hear anything!
            main_title_mid.change_text("Fail")

    # else: # listen.isListening == OFF:
    #     alert_listening.draw(CLOSE)

    #Create animation for output texting of Jarvis sentence.
    animation_text.process()
    countDown.draw()
    if countDown.is_counting:
        countdown_to_optimize_FPS = 60*FPS

    # update frame ---
    fpsClock.tick(FPS)
    pygame.display.update()

# Save Time-Table
# print("[SAVE] Save schedule... -> DATABASE/time-table.json")
# schedule.save_schedule_to_timeTable(schedule.week, aboard_duty.REMIND, aboard_duty.TOMORROW)

# Order that Turn Off listen.pyw file
file = open(listen.PATH_FILE_GET_RESULT, "w")
file.write("[CLOSE_PROGRAM]")
file.close()


pygame.quit()
