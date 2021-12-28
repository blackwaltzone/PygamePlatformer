level_map = [
    '                   XXX',
    '  X   X   X   X      X',
    '                     X',
    'XXX                XXX',
    '  XX        XX        ',
    '       X    XXXXX     ',
    '      XX   XXX   X    ',
    'XP                   X',
    'XXX                XXX',
    'XXXXXXXX  XXXX    XXXX'
]

vertical_tile_number = 11
tile_size = 64
screen_width = 1280
#screen_height = len(level_map) * tile_size
screen_height = vertical_tile_number * tile_size

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GRAY = (100, 100, 100)
BLUE = (0, 0, 250)
GREEN = (0, 250, 0)