import PyBearLibTerminal as bl
from constants import *
import gridtools
import eventhandler
from entitysys import *
import bearplayui as ui

def paint(positions):
    bl.bkcolor('darker red')
    for pos in positions:
        bl.put(pos[0], pos[1], ' ')
    bl.bkcolor('black')

class ToyReceiver(object):
    def __init__(self):
        eventhandler.register(self)
    def receive_event(self, event):
        bl.printf(0, 0, '    ')
        bl.printf(0, 0, str(event))
            
receiver = ToyReceiver()

class Tile(object):
    def __init__(self, x, y, char, parent_map, *contents):
        '''The contents of the cell are organized in layers, represented
        by a list. The end of the list (contents[-1]) represents the top
        of the tile.
        '''
        self.x = x
        self.y = y
        self.parent_map = parent_map
        # The display character of the tile itself:
        self.base_char = char
        self.contents = list(contents)
        
    def draw(self):
        try:
            self.char = self.contents[-1].char
        except (IndexError, AttributeError):
            # If the contents list is empty, or the top object
            # has no char attribute
            self.char = self.base_char
        drawing_system.register(self)
        
    def append(self, obj):
        self.contents.append(obj)
        
    def remove(self, obj):
        self.contents.remove(obj)
        
    def __iter__(self, obj):
        for obj in self.contents:
            yield obj
        
        
class Map(object):
    def __init__(self, width, height, \
                view_x, view_y, view_x2=None, view_y2=None, view_offset=(0,0)):
        if view_x2 is None: view_x2 = view_x + width
        if view_y2 is None: view_y2 = view_y + height
        self.width = width
        self.height = height
        self.view_x = view_x
        self.view_y = view_y
        self.view_x2 = view_x2
        self.view_y2 = view_y2
        # This is the only time where the view offset will be set manually.
        # After this, all view adjustments must be made through Map.scroll().
        self.offset_x, self.offset_y = view_offset[0], view_offset[1]
        
        # Before going any further, we need to do some error checking; 
        # the view should always be completely within the map area
        error_string=("View boundaries ({0},{1}-{2},{3}) extend "
                    "beyond map boundaries ({4},{5}-{6},{7}).")
        error_string = error_string.format(view_x, view_y, view_x2, view_y2, \
                            view_x+self.offset_x, view_y+self.offset_y, \
                            view_x2+self.offset_x+width, view_y+self.offset_y+height)
        view_error = ValueError(error_string)
        if (self.offset_x > 0 or
            self.offset_y > 0 or
            view_x2 > width + self.offset_x or
            view_y2 > height + self.offset_y):
            raise view_error
        
        # Here we set up the Tile objects within the map
        self.tiles = dict()
        for position in gridtools.rectangle(0, 0, width, height):
            new_tile = Tile(*position, ' ', parent_map = self)
            self.tiles[position] = new_tile
            new_tile.screen_x = new_tile.x + view_x + self.offset_x
            new_tile.screen_y = new_tile.y + view_y + self.offset_y
            
        self.draw_view()
            
    def __call__(self, x, y):
        '''This way, you can conveniently reference any tile within
        the map by typing, say, some_map(5, 34).
        '''
        try:
            return self.tiles[(x, y)]
        except KeyError:
            return None
        
    def __iter__(self):
        '''The map, when iterated over, will return each of its
        subordinate Tile objects.
        '''
        for tile in self.tiles.values():
            yield tile
            
    def receive_event(self, event):
        if event in ARROW_EVENTS:
            self.draw_view()
        elif event == bl.TK_W: self.scroll(0, -1)
        elif event == bl.TK_A: self.scroll(-1, 0)
        elif event == bl.TK_S: self.scroll(0, 1)
        elif event == bl.TK_D: self.scroll(1, 0)
            
    def move(self, obj, target):
        '''Move an object from one tile to another.'''
        if target in self.tiles:
            self(obj.x, obj.y).remove(obj)
            self(*target).append(obj)
            obj.x, obj.y = target[0], target[1]
            
    def scroll(self, delta_x, delta_y):
        '''Move the portion of the map currently in view.
        
        map.scroll(5,-3) will scroll 5 tiles to the right and
        3 tiles upward, for example.
        
        scroll() will not move the view beyond the edges of the map.
        Attempting to do so will do nothing.
        '''
        self.offset_x += delta_x
        self.offset_y += delta_y
        # Then we have to make sure that the map doesn't scroll beyond
        # the edges of the view, which means beyond (0,0), the top-left
        # corner, or (mapWidth-viewWidth,mapHeight-viewHeight), which is
        # the bottom-right corner.
        view_width = self.view_x2 - self.view_x
        view_height = self.view_y2 - self.view_y
        self.offset_x = gridtools.bound_number(self.offset_x, maximum = 0,
            minimum = -(self.width - view_width))
        self.offset_y = gridtools.bound_number(self.offset_y, maximum = 0,
            minimum = -(self.height - view_height))
        
        self.draw_view()
            
    def draw_view(self):
        # This draws all the tiles currently in the view.
        for view_coord in gridtools.rectangle(
                            self.view_x, self.view_y, self.view_x2, self.view_y2):
            _x, _y = view_coord[0], view_coord[1]
            # Yes, MINUS self.offset; don't ask me why, math is chaos
            offset_tile_coord = (_x - self.offset_x - self.view_x,
                                 _y - self.offset_y - self.view_y)
            
            offset_tile = self(*offset_tile_coord)
            if offset_tile is not None:
                offset_tile.screen_x, offset_tile.screen_y = _x, _y
                offset_tile.draw()
            
            
class MapChild(object):
    def __init__(self, x, y, char, parent_map):
        self.x = x
        self.y = y
        self.char = char
        self.parent_map = parent_map
        self.parent_map(self.x, self.y).append(self)
            

class AtMan(MapChild):
    def __init__(self, x, y, parent_map):
        MapChild.__init__(self, x, y, '@', parent_map)
        eventhandler.register(self, *ARROW_EVENTS)
        
    def receive_event(self, event):
        if event == bl.TK_RIGHT: new_pos = (self.x+1, self.y)
        elif event == bl.TK_LEFT: new_pos = (self.x-1, self.y)
        elif event == bl.TK_UP: new_pos = (self.x, self.y-1)
        elif event == bl.TK_DOWN: new_pos = (self.x, self.y+1)
        self.parent_map.move(self, new_pos)
        

bl.open()
bl.refresh()
SCREEN_WIDTH = bl.state(bl.TK_WIDTH)
SCREEN_HEIGHT = bl.state(bl.TK_HEIGHT)
        
the_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT, 3,3,9,9)
at = AtMan(5, 5, the_map)
left_apostrophe = MapChild(0, 1, "'", the_map)
right_apostrophe = MapChild(2, 1, "'", the_map)
dud = MapChild(4, 4, "\u2193", the_map)
the_map.draw_view()
eventhandler.register(the_map, *ARROW_EVENTS+WASD_EVENTS)

menu = ui.Menu(60, 0, SCREEN_WIDTH-1, SCREEN_HEIGHT-1)

paint(gridtools.hollow_rectangle(2,2,10,10))
paint(gridtools.rectangle(60, 0, SCREEN_WIDTH-1, SCREEN_HEIGHT-1))

while True:
    drawing_system.run()
    ui_drawing_system.run()
    event = bl.read()
    if event == bl.TK_CLOSE or event == bl.TK_ESCAPE:
        break
        
    eventhandler.fire(event)
    bl.put(1, 1, bl.state(bl.TK_WCHAR))
    bl.refresh()
    
bl.close()