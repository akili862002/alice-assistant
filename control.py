import  os
import pygame
pygame.init()
pathFile = os.path.dirname(os.path.realpath(__file__))
# Functions --------
JARVIS_TALKING = True
JARVIS_LISTEN = True

# Path files
PATH_SCHEDULE = "DATABASE/time_table.json"


# Some CONST
FPS = 60
PI = 3.14159265359

ON = True
OFF = False

OPEN = True
CLOSE = False

DONE = False
NOT_YET = True
IMPORTANT = 2

LEFT = -1
RIGHT = 2
MID = 1

# Mouse type press
NONE = -1
DOWN = 5
UP = 4

HIDE_TEXT = "<$hide_text>"
DISAPPEARANCE = -2
NOTE_CUT = "<br/>"
NOT_FOUND = "<$404_not_found>"
# belonger ---
USER = True
JARVIS = False

# FONT TEXT
USER_FONT = "Berlin Sans FB Demi"
JARVIS_FONT = "Berlin Sans FB Demi"

TIME_TABLE_FONT = "Berlin Sans FB"

# Logic
EQUAL = 0
GREATER = 1
LESS_THAN = -1

# FONT ----
FONT_TypoSlab_Irregular_Demo = {
    "20":pygame.font.Font(pathFile + "/Font_text/TypoSlab-Irregular-Demo.otf",20),
    "26":pygame.font.Font(pathFile + "/Font_text/TypoSlab-Irregular-Demo.otf",26),
    "34":pygame.font.Font(pathFile + "/Font_text/TypoSlab-Irregular-Demo.otf",34)
}

FONT_QuickSand = {
    "25":pygame.font.Font(pathFile + "/Font_text/quicksand/Quicksand-Bold.ttf", 25)
}
FONT_AldotheApache = {
    "60":pygame.font.Font(pathFile + "/Font_text/VanFonting.otf", 72)
}

FONT_Century_Gothic = {
    "20":pygame.font.SysFont("Century Gothic", 20)
}
