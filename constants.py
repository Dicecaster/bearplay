import PyBearLibTerminal as bl

ARROW_EVENTS = [bl.TK_UP, bl.TK_DOWN, bl.TK_RIGHT, bl.TK_LEFT]
WASD_EVENTS = [bl.TK_W, bl.TK_A, bl.TK_S, bl.TK_D]
MOUSE_EVENTS = [bl.TK_MOUSE_LEFT, bl.TK_MOUSE_RIGHT, bl.TK_MOUSE_MIDDLE,
                bl.TK_MOUSE_X1, bl.TK_MOUSE_X2, bl.TK_MOUSE_SCROLL]
MOUSE_MOVE_EVENT = bl.TK_MOUSE_MOVE

CHAR_CORNER_TL = '\u250c'
CHAR_CORNER_TR = '\u2510'
CHAR_CORNER_BL = '\u2514'
CHAR_CORNER_BR = '\u2518'
CHAR_HORIZONTAL = '\u2500'
CHAR_VERTICAL = '\u2502'