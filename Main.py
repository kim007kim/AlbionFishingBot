import keyboard
import time
import ImageGrab as img
import Input as inp
import random
import pyaudio
import numpy as np
import winsound
import pyautogui
import cv2
import sys
import os
from PIL import ImageGrab

while True:
    # Initialize Bot
    maxValue = 2**14
    bars = 35
    p=pyaudio.PyAudio()

    #要找查的設備名稱中的關鍵字
    target = '立體聲混音'
    #逐一查找聲音設備  
    for i in range(p.get_device_count()):
        devInfo = p.get_device_info_by_index(i)   
        if devInfo['name'].find(target)>=0 and devInfo['hostApi'] == 0 :      
            print(devInfo)
            dev_idx = i
            break
    imgB = cv2.imread('bar_blue.png')
    img_B, temp1, temp2 = cv2.split(imgB)
    #wB, hB = img_B.shape[::-1]
    imgR = cv2.imread('bar_red.png')
    temp1, temp2, img_R = cv2.split(imgR)
    #wR, hR = img_R.shape[::-1]
    thresholdB = 0.88
    thresholdR = 0.99
    print("Bot Starting Up, Good Luck")

    fishpoint = 0
    fishX = []
    fishY = []
    while True:
        if keyboard.is_pressed('F11'):
            fishpoint = fishpoint+1
            x, y = pyautogui.position()
            fishX.append(x)
            fishY.append(y)
            print("add point [%d], [%d]"%(x,y))
            time.sleep(1.0)
        
        if keyboard.is_pressed('F10'):
            if fishpoint<1:
                fishpoint = fishpoint+1
                x, y = pyautogui.position()
                fishX.append(x)
                fishY.append(y)
            break
        
    while True:
        print('New round, cast rod                             ', end = ' \r')
        playerexist = False
        while True:
            print('Player detecting                            ', end = ' \r')
            capture = np.array(ImageGrab.grab(bbox=(50, 50, 1870, 1030)))  # Left, Upper, Right, Lower
            capture_R, capture_G, capture_B = cv2.split(capture)
            res = cv2.matchTemplate(capture_B,img_B,cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= thresholdB)
            #print (np.count_nonzero(res >= thresholdB))
            if np.count_nonzero(res >= thresholdB)>0:
                for pt in zip(*loc[::-1]):
                    print(pt)
                time.sleep(random.uniform(10, 20))
                playerexist = True
                continue
            res = cv2.matchTemplate(capture_R,img_R,cv2.TM_CCOEFF_NORMED)
            loc = np.where( res >= thresholdR)
            #print (np.count_nonzero(res >= thresholdR))
            if np.count_nonzero(res >= thresholdR)>0:
                for pt in zip(*loc[::-1]):
                    print(pt)
                time.sleep(random.uniform(10, 20))
                playerexist = True
                continue
            print('no player detected')
            if playerexist:
                time.sleep(random.uniform(20, 60))
            break
        fishpointselect = random.randint(0,fishpoint-1)
        pyautogui.moveTo(fishX[fishpointselect], fishY[fishpointselect])
        inp.cast_rod()
        over = False
        time.sleep(1.3)
        print('start to detect sound')
        stream=p.open(input_device_index=dev_idx,format=pyaudio.paInt16,channels=2,rate=44100, input=True, frames_per_buffer=1024)
        previoussum = 0
        while True:
            print('Sound detecting                          ', end = ' \r')
            data = np.frombuffer(stream.read(4096),dtype=np.int16)
            volume = int(np.abs(np.max(data)-np.min(data))*bars/maxValue)
            starString = "#"*volume+"-"*int(bars-volume)
            print("Vulume=[%s]"%(starString))
            #data = np.frombuffer(stream.read(1024),dtype=np.int16)
            #dataL = data[0::2]
            #dataR = data[1::2]
            #peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
            #peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue
            #lString = "#"*int(peakL*bars)+"-"*int(bars-peakL*bars)
            #rString = "#"*int(peakR*bars)+"-"*int(bars-peakR*bars)
            #print("L=[%s]\tR=[%s]"%(lString, rString))
            #volume = int(peakL*bars + peakR*bars)
            if keyboard.is_pressed('F12'):
                break
            
            if volume>=6 or volume+previoussum>=8:
                if volume>=9:
                    continue
                stream.stop_stream()
                stream.close()
                #print("L=[%s]\tR=[%s], Start to catch fish"%(np.max(dataL), np.max(dataR)))
                inp.hold()  # Move Right
                time.sleep(random.uniform(0.75, 0.8))
                inp.release()
                #winsound.Beep(frequency, duration)
                while True:  # While Fishing Bar Is On Screen
                    position = img.get_position()
                    if position == -1:  # Fishing is Over
                        print('position is ', position, ', over')
                        inp.release()
                        over = True
                        break

                    if position < 137:
                        inp.hold()  
                        time.sleep(random.uniform(0.1, 0.2))
                    elif position > 142:
                        inp.release()  
                        time.sleep(random.uniform(0.03, 0.08))
                    elif position < 142:
                        inp.hold()
                        time.sleep(random.uniform(0.0, 0.1))
            previoussum = volume
            if over==True:
                for i in range(30):
                    time.sleep(random.uniform(0.1, 0.2))
                    if keyboard.is_pressed('F12'):
                        break
                if keyboard.is_pressed('F12'):
                    break
                os.system('cls')
                print('start new round')
                break
            if keyboard.is_pressed('F12'):
                break
        if keyboard.is_pressed('F12'):
            break

    p.terminate()
    winsound.Beep(600, 200)
    os.system('cls')
