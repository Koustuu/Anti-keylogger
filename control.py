from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

def controlMouse():
    mouse = MouseController()
    mouse.position = (10, 20)  # Sets the mouse position to coordinates (10, 20)

def controlKeyboard():
    keyboard = KeyboardController()
    keyboard.type("i am awesome!")  # Types the string using the keyboard controller

# Run both functions
controlKeyboard()
controlMouse()
