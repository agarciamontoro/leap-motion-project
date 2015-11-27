from primitives import Image, Button, Circle
from constants import *

from operator import add

class NavigationalButton(Button):
    def __init__(self, rect, next_screen = None, epsilon = BUTTON_TOL):
        self.next = next_screen
        Button.__init__(self, rect, epsilon)

    def navigate(self):
        return self.next

class ActionButton(Button):
    def __init__(self, rect, action, epsilon = BUTTON_TOL):
        self.action = action
        Button.__init__(self, rect, epsilon)

    def act(self):
        self.action()

class Screen(Image):
    def __init__(self, img_file_name, buttons):
        self.buttons = buttons
        Image.__init__(self,img_file_name)

    def buttonTouched(self, point):
        for button in self.buttons:
            if button.isTouched(point):
                return button
        return False

class Menu:
    def __init__(self,start_screen=None,loader=None):
        self.start_screen = start_screen
        self.loader = loader

        self.current_screen = self.start_screen
        self.pointer = Circle()

        self.enabled = False

    def swap(self):
        self.enabled = not self.enabled

        # Initialize
        if not self.enabled:
            self.current_screen = self.start_screen

    def process(self, point):
        self.pointer.center = point

        button = self.current_screen.buttonTouched(point)
        if button:
            self.loader.center = button.getCenter()

            if self.loader.load():
                self.loader.reset()
                if isinstance(button, NavigationalButton):
                    self.current_screen = button.navigate()
                elif isinstance(button, ActionButton):
                    button.act()
        else:
            self.loader.reset()

    def draw(self):
        if self.enabled:
            self.pointer.draw()
            for button in self.current_screen.buttons:
                button.draw()
            self.loader.draw()
            self.current_screen.draw()
