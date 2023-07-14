MOVES = [
    {'move': 'up', 'transform': lambda coords: {'x': coords['x'], 'y': coords['y'] + 1}},
    {'move': 'down', 'transform': lambda coords: {'x': coords['x'], 'y': coords['y'] - 1}},
    {'move': 'left', 'transform': lambda coords: {'x': coords['x'] - 1, 'y': coords['y']}},
    {'move': 'right', 'transform': lambda coords: {'x': coords['x'] + 1, 'y': coords['y']}}
]