import os, subprocess, pyautogui
from win32gui import *
from time import sleep

def arrangeInstances():
    # Wait for multi-instance manager to spawn and arrange instance windows
    if not FindWindow(None, "BlueStacks Multi Instance Manager"):
        subprocess.Popen(["C:\Program Files\BlueStacks_nxt\HD-MultiInstanceManager.exe"])
        while not FindWindow(None, "BlueStacks Multi Instance Manager"):
            sleep(0.1)
    SetForegroundWindow(FindWindow(None, "BlueStacks Multi Instance Manager"))
    sleep(0.1)
    pyautogui.click(pyautogui.locateCenterOnScreen("img/bluestacks/arrange.png"))

def killInstances():
    for process in ["HD-Player", "HD-MultiInstanceManager"]:
        subprocess.run(['TASKKILL', '/F', '/IM', process + '.exe'])

def prepareInstances():
    # If less than 3 instances are running launch all instances
    while len(subprocess.check_output(('TASKLIST', '/NH', '/FO', 'CSV', '/FI', 'IMAGENAME eq HD-P*')).decode().replace('"', '').split('\r\n')[:-1]) < 3:
        print("Spawning instances")
        for i in range(3):
            subprocess.Popen(["C:\Windows\System32\cmd.exe", "/c", "start", "", "/High", "C:\Program Files\BlueStacks_nxt\HD-Player.exe",
                            "--instance", "Nougat64_" + str(i), "--hidden", "--cmd", "launchAppWithBsx",  "--package", "com.plarium.raidlegends"]).wait()
        sleep(2)
    print("All instances are running")
    arrangeInstances()
    # coords = []
    # for instance in instances:
    #     coords.append(GetWindowRect(FindWindow(None, instance)))
    # return dict(zip(instances, coords))


if __name__ == '__main__':
### ADD TO GUI
    # prepareInstances()
    # arrangeInstances()
    # killInstances()
###

    






