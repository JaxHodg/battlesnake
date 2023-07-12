from enum import Enum

class Direction(Enum):
    UP = {'move': 'up', 'transform': lambda coords: {'x': coords['x'], 'y': coords['y'] + 1}}
    DOWN = {'move': 'down', 'transform': lambda coords: {'x': coords['x'], 'y': coords['y'] - 1}}
    LEFT = {'move': 'left', 'transform': lambda coords: {'x': coords['x'] - 1, 'y': coords['y']}}
    RIGHT = {'move': 'right', 'transform': lambda coords: {'x': coords['x'] + 1, 'y': coords['y']}}
    