'''A collection of abstract, set-based grid coordinate tools.'''
import math
from collections import namedtuple

Point = namedtuple('Point', 'x, y')

class Rectangle(namedtuple('Rectangle', 'p1, p2')):
    def __contains__(self, point):
        x, y = point.x, point.y
        return x >= self.p1.x \
               and x <= self.p2.x \
               and y >= self.p1.y \
               and y <= self.p2.y

def rectangle(x, y, x2, y2):
    for _x in range(x, x2+1):
        for _y in range(y, y2+1):
            yield Point(_x, _y)#(_x, _y)
            

def hollow_rectangle(x, y, x2, y2):
    for _x in range(x, x2+1):
        yield Point(_x, y)
        yield Point(_x, y2)
    for _y in range(y+1, y2):
        yield Point(x, _y)
        yield Point(x2, _y)
        

def bound_number(number, minimum = -math.inf, maximum = math.inf):
    '''Return the given number if it is within the minimum and maximum
    values given; otherwise, return the minimum or maximum.
    '''
    if number < minimum: return minimum
    if number > maximum: return maximum
    return number