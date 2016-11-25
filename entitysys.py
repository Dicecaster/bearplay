import PyBearLibTerminal as bl
from constants import *

class EntitySystem(object):
    def __init__(self, run_function, sticky = False):
        '''By default, entity systems will automatically clear
        their object registry after every run, e.g. an object in
        a drawing system will need to re-register itself every time
        it needs to be re-drawn. However, if sticky is set to True,
        then objects will have to manually unregister() themselves when
        they no longer need to be part of the system.
        '''
        self.objects = []
        if sticky:
            def run_wrapper():
                run_function(self.objects)
        else:
            def run_wrapper():
                run_function(self.objects)
                self.objects = []
        self.run = run_wrapper
        
    def register(self, *objects):
        for obj in objects:
            if obj not in self.objects:
                self.objects.append(obj)
            
    def unregister(self, obj):
        try:
            self.objects.remove(obj)
        except ValueError:
            # In case obj is not in self.objects
            pass
            
 
def draw(drawables):
    for obj in drawables:
        bl.put(obj.screen_x, obj.screen_y, obj.char)
    bl.refresh()
        
drawing_system = EntitySystem(draw)


def ui_draw(ui_elements):
    for ui_element in ui_elements:
        bl.put(ui_element.x, ui_element.y, CHAR_CORNER_TL)
        bl.put(ui_element.x2, ui_element.y, CHAR_CORNER_TR)
        bl.put(ui_element.x, ui_element.y2, CHAR_CORNER_BL)
        bl.put(ui_element.x2, ui_element.y2, CHAR_CORNER_BR)
        
        for x in range(ui_element.x+1, ui_element.x2):
            bl.put(x, ui_element.y, CHAR_HORIZONTAL)
            bl.put(x, ui_element.y2, CHAR_HORIZONTAL)
        for y in range(ui_element.y+1, ui_element.y2):
            bl.put(ui_element.x, y, CHAR_VERTICAL)
            bl.put(ui_element.x2, y, CHAR_VERTICAL)
        
ui_drawing_system = EntitySystem(ui_draw)


# This code was a pain in the butt, so I'm keeping it just in case.
#
#    def run_wrapper(self):
#            # We pass the run function only the objects which actually
#            # need to be run, i.e. the ones that are flagged for
#            # running and are not deactivated.
#            pruned_objects = [obj for obj in self.objects \
#                               if getattr(obj, self.flag) \
#                               and obj not in self.deactivated_objects]
#           run_function(pruned_objects)
#            for obj in pruned_objects:
#                setattr(obj, self.flag, False)
#       self.run = run_wrapper