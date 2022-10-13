# import logging, sys, random, copy
import os, win32api, win32clipboard
import pyautogui as gui
from win32gui import *
from tkinter import *
from time import sleep

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
# logging.disable(logging.DEBUG) # uncomment to block debug log messages

def clickxy(instance, button):
    pos = (instance[2] - button[0], instance[3] - button[1])
    print(pos)
    gui.click(pos)

def getCoords():
    while True:
        if win32api.GetKeyState(0x02) < 0:
            exit()
        elif win32api.GetKeyState(0x01) < 0:
            pos = win32api.GetCursorPos()
            sleep(0.1)
            hwnd = GetForegroundWindow()
            coords = GetWindowRect(hwnd)
            name = GetWindowText(hwnd)
            diff = (coords[2] - pos[0], coords[3] - pos[1])
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(str(diff))
            win32clipboard.CloseClipboard()
            break
    return pos, diff, name

def killall():
    for process in ["HD-Player", "HD-MultiInstanceManager"]:
        os.system("taskkill /f /im " + process + ".exe")

def lunchGui():
    window = Tk()
    window.title("RSL bot")
    window.geometry('250x100')
        
    # launchBT = Button(window, text="Launch", command=print("haha"))
    # launchBT.grid(column=1, row=0)

    killallBT = Button(window, text="Kill All", command=killall)
    killallBT.grid(column=2, row=0)

    # coordsBT = Button(window, text="Get Coords", command=print("haha"))
    # coordsBT.grid(column=3, row=0)

    # arenaBT = Button(window, text="Arena", command=print("haha"))
    # arenaBT.grid(column=1, row=1)

    window.mainloop()

def prepareInstances(instances):
    x = 0
    for instance in instances + ["BlueStacks Multi Instance Manager"]:
        while True:
            if FindWindow(None, instance):
                print(instance, "spawned")
                break
            x = 1
            os.startfile(os.path.join(os.environ['USERPROFILE'], 'Desktop', instance))
            sleep(1)
    if x:
        MoveWindow(FindWindow(None, "BlueStacks Multi Instance Manager"), 0, 0, 672, 512, 0)
        gui.click(550, 470)

    coords = []
    for instance in instances:
        coords.append(GetWindowRect(FindWindow(None, instance)))
    return dict(zip(instances, coords))

def repeatClicks(instances):
        pos, diff, name = getCoords()
        if win32api.GetKeyState(0xA0) < 0: 
            if name in instances.keys():
                for instance in without_keys(instances, name).values():
                    gui.click(instance[2] - diff[0], instance[3] - diff[1])
                    sleep(.1)
                win32api.SetCursorPos(pos)
        
def without_keys(dict, keys):
    return {x: dict[x] for x in dict if x not in keys}

if __name__ == '__main__':

    # battle = (120, 53)
    # arena = (263, 309)
    # classic_arena = (821, 348)
    # arena_battle = (144, 423)
    # start = (152, 67)

    instances = prepareInstances(["raid1", "raid2", "raid3", "main"])
    while True:
        repeatClicks(instances)
        

    # lunchGui()

    # for instance in instances.values():
    #     clickxy(instance, battle)
    
    
            # pos = gui.locateOnScreen('img/forge.png', confidence=0.9, region=instance)
        # print(pos)
        # gui.click(pos)
        # while True:
        #     if gui.locateOnScreen('img/forge.png', confidence=0.9, region=instance):
        #         break