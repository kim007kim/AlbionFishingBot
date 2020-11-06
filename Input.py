import time
import random
import pyautogui as auto
import win32gui
import win32api

def cast_rod():
    #x, y = auto.position()
    #long_position = win32api.MAKELONG(x, y)
    #win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    #time.sleep(random.uniform(0.05, 1.5))
    #win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
    
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
