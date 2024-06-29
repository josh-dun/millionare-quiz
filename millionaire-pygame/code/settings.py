# thachlam's project
# remmeber to read the readme

import pygame 
import random, time
pygame.init()

# question box variables
QUESTION_WIDTH, QUESTION_HEIGHT = 650, 80
TEXT_GAP = 0

# answer box variables
ANSWER_GAP_X = 20
ANSWER_GAP_Y = 40
ANSWER_WIDTH = 330
ANSWER_HEIGHT = 80

# support box variables
SUPPORT_WIDTH, SUPPORT_HEIGHT = 80, 80
SUPPORT_GAP = 100
SUPPORT_START_Y = 120

FONT = {
    "question": pygame.font.SysFont('comicsans', 30),
    "instruction": pygame.font.SysFont("comicsans", 30),
    "answer": pygame.font.SysFont("comicsans", 28),
    'money': pygame.font.SysFont("comicsans", 28),
    'support': pygame.font.SysFont("comicsans", 23),
    'end': pygame.font.SysFont("comicsans", 50),


}

WIDTH, HEIGHT = 800, 600

MONEY_IN_STRING = {
    0: "0", 100: "100", 200: "200", 300: "300", 500: "500", 1000: "1.000", 
    2000: "2.000", 4000: "4.000", 8000: "8.000",
    16000: "16.000", 32000: "32.000", 64000: "64.000", 125000: "125.000", 250000: "250.000",
    500000: "500.000", 
    1000000: "1.000.000"}

ANSWERS = ["A", "B", "C", "D"]

