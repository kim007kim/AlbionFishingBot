import keyboard
import pyaudio
import numpy as np

maxValue = 2**16
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

stream=p.open(input_device_index=dev_idx,format=pyaudio.paInt16,channels=2,rate=44100,
              input=True, frames_per_buffer=1024)
while True:
    data = np.fromstring(stream.read(1024),dtype=np.int16)
    dataL = data[0::2]
    dataR = data[1::2]
    peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
    peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue
    lString = "#"*int(peakL*bars)+"-"*int(bars-peakL*bars)
    rString = "#"*int(peakR*bars)+"-"*int(bars-peakR*bars)
    print("L=[%s]\tR=[%s]"%(lString, rString))
    if keyboard.is_pressed('F12'):
        break
stream.stop_stream()
stream.close()
p.terminate()
