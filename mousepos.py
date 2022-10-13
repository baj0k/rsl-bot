import pyautogui
from time import sleep
import keyboard

while keyboard.is_pressed('Esc') == False:
    if keyboard.is_pressed('Left Shift'):
        print((pyautogui.position()[0], pyautogui.position()[1], pyautogui.pixel(*pyautogui.position())), end='\r')
    if keyboard.is_pressed('Left Alt'):
        print()
        sleep(0.5)
    sleep(0.1)