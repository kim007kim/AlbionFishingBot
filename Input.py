import time
import random
import pyautogui as auto

def cast_rod():
    auto.mouseDown()
    time.sleep(random.uniform(0.05, 1.5))
    auto.mouseUp()

def click():
    auto.click()

def hold():
    auto.mouseDown()

def release():
    auto.mouseUp()

def use_fishing_bait():
    auto.typewrite('1')
