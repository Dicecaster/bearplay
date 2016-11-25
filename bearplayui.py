'''The bearplay ui library.'''
import PyBearLibTerminal as bl
from constants import *
import eventhandler
from entitysys import *

class Menu(object):
    def __init__(self, x, y, x2, y2):
        # To be clear, xy and x2y2 are direct screen coordinates,
        # not internal coordinates like the Map module.
        self.x = x
        self.x2 = x2
        self.y = y
        self.y2 = y2
        self.width = x2 - x
        self.height = y2 - y
        self.contents = []
        self.mouse_hovering = False
        self.update_mouse_hovering()
        
        eventhandler.register(self, *MOUSE_EVENTS + [MOUSE_MOVE_EVENT])
        ui_drawing_system.register(self)
        
    def receive_event(self, event):
        if event == MOUSE_MOVE_EVENT:
            mouse_was_hovering = self.mouse_hovering
            self.update_mouse_hovering()
            if mouse_was_hovering and not self.mouse_hovering:
                self.mouse_exit()
            elif self.mouse_hovering and not mouse_was_hovering:
                self.mouse_enter()
    
    def update_mouse_hovering(self):
        mouse_x = bl.state(bl.TK_MOUSE_X)
        mouse_y = bl.state(bl.TK_MOUSE_Y)
        
        if mouse_x >= self.x and \
           mouse_x <= self.x2 and \
           mouse_y >= self.y and \
           mouse_y <= self.y2:
            self.mouse_hovering = True
        else:
            self.mouse_hovering = False
            
    def mouse_enter(self):
        print("The package has arrived.")
        
    def mouse_exit(self):
        print("The package has departed.")