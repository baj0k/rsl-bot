import pyautogui, subprocess, os
from win32gui import *
from time import sleep
from tkinter import *

# buttons (x, y, (ready), (not ready))
dungeons = (1090, 670)
minotaur = (1670, 700)
minotaur15 = ()
replay = (2050, 1330)

def click(button):
    pyautogui.click(button)
    sleep(1)

def launchGui():
    window = Tk()
    window.title("RSL bot")
    window.geometry('250x100')
        
    arenaBT = Button(window, text="Classic Arena", command=lambda: arenaRun("classic"))
    arenaBT.grid(column=1, row=0)

    arenaBT = Button(window, text="Tag Team Arena", command=lambda: arenaRun("tagteam"))
    arenaBT.grid(column=2, row=0)

    window.mainloop()

def prepareInstance(instance, pos):
    if FindWindow(None, instance):
        print(instance, "is running")
    else:
        subprocess.Popen([os.path.join(os.getenv('LOCALAPPDATA'), 'PlariumPlay\PlariumPlay.exe'), '--args', '-gameid=101', '-tray-start'])
        print("Starting", instance)
        while not FindWindow(None, instance):
            print("Waiting for ", instance, "to spawn")
            sleep(2)
    MoveWindow(FindWindow(None, instance), *pos, 0)

def arenaRun(name):
    window_pos = (1460, 0, 1105, 1395)
    battle = (2450, 1345)
    arena = (2320, 720)
    arenaRefresh = (2430, 150, (21,124,156))
    arenaBattle = (2440, 240, (186, 130, 5))
    arenaLastEmpty = (2285, 250, (16,  80,  110))
    arenaStart = (2420, 1325)
    tapToContinue = (2015, 1335)
    if name == "classic":
        arenaType = (1590, 760)
        battleNextInc = 106
    elif name == "tagteam":
        arenaType = (2400, 700)
        battleNextInc = 116

    prepareInstance("Raid: Shadow Legends", window_pos)
    click(battle)
    click(arena)
    click(arenaType)

    if pyautogui.pixelMatchesColor(*arenaRefresh):
        click(arenaRefresh[:-1])

    for i in range(10):
        if not pyautogui.pixelMatchesColor(arenaBattle[0], arenaBattle[1] + battleNextInc * i, arenaBattle[2]):
            print("Skipping ", i + 1)

        elif name == "classic":
            if pyautogui.pixelMatchesColor(arenaLastEmpty[0], arenaLastEmpty[1] + battleNextInc * i, arenaLastEmpty[2], tolerance=10):
                print("Found match", i + 1)
                click((arenaBattle[0], arenaBattle[1] + battleNextInc * i))
                click(arenaStart)
                while 1:
                    if pyautogui.locateOnScreen('img/tapToContinue.png', region=(1800, 1250, 500, 200), confidence=0.8, grayscale=True) == None:
                        sleep(2)
                    else:
                        click(tapToContinue)
                        click(tapToContinue)
                        break
        
        elif name == "tagteam":
            print("Found match", i + 1)
            click((arenaBattle[0], arenaBattle[1] + battleNextInc * i))
            click(arenaStart)
            while 1:
                if pyautogui.locateOnScreen('img/tapToContinue.png', region=(1800, 1250, 500, 200), confidence=0.8, grayscale=True) == None:
                    sleep(2)
                else:
                    click(tapToContinue)
                    click((2000, 600))
                    break

# def minotaurRun():
#     click(battle)
#     click(dungeons)
#     drag(*minotaurDrag)
#     click(minotaur)

if __name__ == '__main__':

    arenaRun("classic")
    # arenaRun("tagteam")

    # minotaurRun()
    # launchGui()

    # while 1:
    #     click(replay)
    #     sleep(2)

### DEBUG ###

    # print(pyautogui.pixel(*arenaBattle[:-1]))
    # print(arenaBattle)


    # while 1:
    #     if pyautogui.locateOnScreen('img/tapToContinue.png', region=(1800, 1250, 500, 200), confidence=0.8, grayscale=True) != None:
    #         print("OK")
    #     else:
    #         print("Not OK")
    #     sleep(0.5)

### DEBUG END ###