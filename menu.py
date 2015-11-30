from primitives import Image, Button, Circle
from constants import *

from operator import add

'''
Button for navigating between screens. Its main attribute is the next_screen variable,
which points to an object of class Screen. This object is returned when the buttos in pressed
'''
class NavigationalButton(Button):
    def __init__(self, rect, next_screen = None, epsilon = BUTTON_TOL):
        self.next = next_screen
        Button.__init__(self, rect, epsilon)

    # Returns the screen that the object points to
    def navigate(self):
        return self.next

'''
Button for invoking a function. Its main attribute is the action variable,
which is the function to be executed when pressed
'''
class ActionButton(Button):
    def __init__(self, rect, action = None, epsilon = BUTTON_TOL):
        self.action = action
        Button.__init__(self, rect, epsilon)

    # Calls the function attached
    def act(self):
        self.action()

'''
Screen of a menu, composed of an image and a list of buttons
'''
class Screen(Image):
    def __init__(self, img_file_name, buttons = None):
        self.buttons = buttons
        Image.__init__(self,img_file_name)

    # Returns whether a button is pressed given a point of the image.
    # If there's a button pressed, that object is returned
    def buttonTouched(self, point):
        for button in self.buttons:
            if button.isTouched(point):
                return button

        return False

'''
Main class for implementing a menu. It consists of a start screen
and a loader, which is called whenever a button is being pressed
'''
class Menu:
    def __init__(self,start_screen=None,loader=None):
        self.start_screen = start_screen
        self.loader = loader

        self.current_screen = self.start_screen
        self.pointer = Circle()

        self.enabled = False

    # Returns the menu to its original state, i.e., to the start screen
    def reset(self):
        self.current_screen = self.start_screen

    # Changes between enabled or disabled. When the menu is being disabled,
    # it is also reset
    def swap(self):
        self.enabled = not self.enabled

        # Initialize
        if not self.enabled:
            self.reset()

    # Disable and reset the menu
    def disable(self):
        self.enabled = False
        self.reset()

    # Main method: it receives a point in the screen and looks for the button
    # that is being pressed. It then waits for the loader to finish, and activates
    # the action button when required.
    def process(self, point):
        self.pointer.center = point

        # Retrieves the button being pressed
        button = self.current_screen.buttonTouched(point)


        if button:
            # Set the loader center and radius to fit the button coordinates
            self.loader.center = button.getCenter()
            self.loader.loader_radius = button.getRadius()

            # Calls the loader and check whether it has finished
            if self.loader.load():
                # If it has finished, reset the loader and activates the button
                self.loader.reset()
                if isinstance(button, NavigationalButton):
                    self.current_screen = button.navigate() # Navigate!
                elif isinstance(button, ActionButton):
                    button.act() # Act!
        #If no button is being pressed, then reset the loader
        else:
            self.loader.reset()

    def draw(self):
        if self.enabled:
            self.pointer.draw()
            #for button in self.current_screen.buttons:
            #        button.draw()
            self.loader.draw()
            self.current_screen.draw()
