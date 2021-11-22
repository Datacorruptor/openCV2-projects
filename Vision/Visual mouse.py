import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import win32api, win32con

SCREEN_WIDTH =  win32api.GetSystemMetrics(0)
SCREEN_HEIGHT =  win32api.GetSystemMetrics(1)


import keyboard
################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)
l,r,t,b =0,wCam,0,hCam
x1,y1=0,0
virtual = False
keyboard.on_press_key("1", lambda _: changeL(x1))
keyboard.on_press_key("2", lambda _: changeT(y1))
keyboard.on_press_key("3", lambda _: changeR(x1))
keyboard.on_press_key("4", lambda _: changeB(y1))
keyboard.on_press_key(" ", lambda _: space())

def space():
    global virtual
    virtual = not virtual
def changeL(x):
    global l
    l=x
def changeR(x):
    global r
    r=x
def changeT(x):
    global t
    t=x
def changeB(x):
    global b
    b=x


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = cv2.flip(img, 0)
    # Find Hand
    img = detector.findHands(img)
    lmList,_ = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        i=8
        x1, y1 = lmList[i][1], lmList[i][2]
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        if virtual:
            x = np.interp(x1, [l, r], [0, SCREEN_WIDTH])
            y = np.interp(y1, [t, b], [0, SCREEN_HEIGHT])
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/SCREEN_WIDTH*65535.0), int(y/SCREEN_HEIGHT*65535.0))



    # Frame rate
    cv2.rectangle(img, (l, t), (r, b), (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)