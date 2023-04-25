import subprocess, pyautogui
from win32gui import *
from tkinter import *
from time import sleep

####################
# CONFIG VARIABLES #
####################

instance_names = ['raid1', 'raid2', 'raid3']
instance_version = "Nougat64"

######################
# PYAUTOGUI WRAPPERS #
######################

def click(button, delay=1):
    pyautogui.click(button)
    sleep(delay)

def locateCenter(button, confidence=0.9):
    return pyautogui.locateCenterOnScreen(button + ".png", grayscale=True, confidence=confidence)

def locateAll(button, confidence=0.9):
    return [pyautogui.center(pos) for pos in pyautogui.locateAllOnScreen(button + ".png", grayscale=True, confidence=confidence)]

########################
# BLUESTACKS FUNCTIONS #
########################

# Wait for multi-instance manager to spawn and arrange instance windows
def arrangeInstances():
    if not FindWindow(None, "BlueStacks Multi Instance Manager"):
        manager = subprocess.Popen(["C:\Program Files\BlueStacks_nxt\HD-MultiInstanceManager.exe"])
        while not FindWindow(None, "BlueStacks Multi Instance Manager"):
            sleep(0.1)
        SetForegroundWindow(FindWindow(None, "BlueStacks Multi Instance Manager"))
        sleep(0.5)
        click(locateCenter("img/bluestacks/arrange"))
        manager.kill()
    else:
        subprocess.run(['TASKKILL', '/F', '/IM', 'HD-MultiInstanceManager.exe'])
        arrangeInstances()        

# Force close all bluestacks processess
def killInstances():
    for process in ["HD-Player", "HD-MultiInstanceManager"]:
        subprocess.run(['TASKKILL', '/F', '/IM', process + '.exe'])

# Toggle synchronization of instances
def toggleSyncOff():
    if locateCenter("img/bluestacks/sync_pause", 0.8):
        click(locateCenter("img/bluestacks/sync_pause"))

def toggleSyncOn():
    if locateCenter("img/bluestacks/sync_play"):
        click(locateCenter("img/bluestacks/sync_play"))

# If less than 3 instances are running launch all instances
def prepareInstances():
    while len(subprocess.check_output(('TASKLIST', '/NH', '/FO', 'CSV', '/FI', 'IMAGENAME eq HD-P*')).decode().replace('"', '').split('\r\n')[:-1]) < len(instance_names):
        print("Spawning instances")
        for i in range(len(instance_names)):
            subprocess.Popen(["C:\Windows\System32\cmd.exe", "/c", "start", "", "/High", "C:\Program Files\BlueStacks_nxt\HD-Player.exe",
                            "--instance", instance_version + "_" + str(i), "--hidden", "--cmd", "launchAppWithBsx",  "--package", "com.plarium.raidlegends"]).wait()
        sleep(5)
    print("All instances are running")
    
    # Sync all instances to the top left one if not already synchronized
    if not locateCenter("img/bluestacks/sync_on"):
        sleep(5)
        if locateCenter("img/bluestacks/sidebar_close"):
            for pos in [pyautogui.center(pos) for pos in pyautogui.locateAllOnScreen("img/bluestacks/sidebar_close.png")]:
                click(pos)  
        click(locateCenter("img/bluestacks/sidebar_open"))
        click(locateCenter("img/bluestacks/sync"))
        click([pyautogui.center(pos) for pos in pyautogui.locateAllOnScreen("img/bluestacks/sync_checkbox.png", grayscale=True, confidence=0.9)][-1:][0])
        click(locateCenter("img/bluestacks/start_sync"))
        click(locateCenter("img/bluestacks/sidebar_close"))
    print("All instances are synchronized")

    # Arrange windows if not arranged
    coords = []
    for instance in instance_names:
        x,y,w,h = GetWindowRect(FindWindow(None, instance))
        coords.append((x,y,w,h))
    
    if coords[0][2] != coords[1][0] or coords[0][3] != coords[2][1]:
        arrangeInstances()
    print("Windows arranged")

##################
# RAID FUNCTIONS #
##################

# Do classic or tagteam arena run depending on parameter provided
def arenaRun(arena_type):
    # If not in arena, go to arena
    toggleSyncOn()
    if not locateCenter("img/arena/battle"):
        # for button in ["battle", "arena/arena", "arena/classic_arena"]:
            # click(locateCenter("img/arena/" + button))
        click(locateCenter("img/battle"))
        click(locateCenter("img/arena/arena"))
        click(locateCenter("img/arena/" + arena_type))

    # Battle until all battles completed or refresh is not available for all instances
    while (locateCenter("img/arena/battle") or len(locateAll("img/arena/refresh_off")) != len(instance_names)):
        for button in ['refresh', 'battle', 'battle_start', 'continue', 'return']:
            if locateCenter("img/arena/" + button):
                click(locateCenter("img/arena/" + button))

# Go to market and buy an item preferably one of the cheaper ones
def marketBuy():
    if locateCenter("img/market"):
        toggleSyncOn()
        click(locateCenter("img/market"))
        toggleSyncOff()
        if locateCenter("img/market/price_low", 0.8):
            [click(pos) for pos in locateAll("img/market/price_low", 0.8)]
            [click(pos) for pos in locateAll("img/market/get", 0.8)]
        elif locateCenter("img/market/price_high", 0.8):
            [click(pos) for pos in locateAll("img/market/price_high", 0.8)]
            [click(pos) for pos in locateAll("img/market/get", 0.8)]

def tavernUpgrade():
    if locateCenter("img/tavern"):
        toggleSyncOn()
        for button in ['tavern', 'tavern/sort', 'tavern/one_star', 'tavern/brew', 'tavern/brew_plus', 'tavern/upgrade']:
            click(locateCenter("img/" + button, 0.8))

# TODO
def goToBastion():
    closeAds()

# Temporarily disable sync operations and close any ads that pop up
def closeAds():
    toggleSyncOff()
    while len(locateAll("img/battle")) != len(instance_names):
        for button in ["img/close_ad", "img/close_chat"]:
            for pos in locateAll(button, 0.8):
                click(pos)
                sleep(2)
    toggleSyncOn()

# Launch gui
def launchGui():
    # NOT YET ADDED
    # arrangeInstances()
    # killInstances()
    # toggleSync()
    # goToBastion()

    window = Tk()
    window.title("RSL bot")
    window.geometry('250x100')
        
    cArenaBT = Button(window, text="Classic Arena", command=lambda: arenaRun("classic"))
    cArenaBT.grid(column=1, row=0)

    tArenaBT = Button(window, text="Tag Team Arena", command=lambda: arenaRun("tagteam"))
    tArenaBT.grid(column=2, row=0)

    # marketBT = Button(window, text="Market daily", command=marketBuy())
    # marketBT.grid(column=1, row=1)

    tavernBT = Button(window, text="Tavern daily", command=tavernUpgrade())
    tavernBT.grid(column=2, row=1)

    window.mainloop()

if __name__ == '__main__':
    # Spawn bluestacks instances, arrange windows and enable sync operations.
    prepareInstances()
    # Wait until all instances load the town menu and close any ads that pop up
    # closeAds()
    # launchGui()
    arenaRun("classic")

    # PLAYTIME REWARDS UNFINISHED
    # if locateCenter("img/playtime_rewards"):
    #     click(locateCenter("img/playtime_rewards"))
    #     while locateCenter("img/playtime_reward_get"):
    #         click(locateCenter("img/playtime_reward_get"))