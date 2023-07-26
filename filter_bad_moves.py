
def filter_self_collision(curr_snake: list, possible_moves: list):
    remove = []
    for move in possible_moves:
        new_position = move['transform'](curr_snake[0])
        if new_position in curr_snake[:-1]:
            remove.append(move)

    possible_moves = [move for move in possible_moves if move not in remove]
    return possible_moves

def filter_border_collision(curr_snake: list, possible_moves: list, board: dict):
    remove = []
    for move in possible_moves:
        new_position = move['transform'](curr_snake[0])
        if new_position['x'] < 0 \
            or new_position['x'] >= board['width'] \
            or new_position['y'] < 0 \
            or new_position['y'] >= board['height']:
            remove.append(move)

    possible_moves = [move for move in possible_moves if move not in remove]
    return possible_moves

def filter_enemy_collision(curr_snake: list, possible_moves: list, enemies: dict):
    enemy_bodies = []
    for enemy in enemies:
        enemy = enemy['body']
        for body in enemy:
            enemy_bodies.append(body)
    
    remove = []
    for move in possible_moves:
        new_position = move['transform'](curr_snake[0])
        if new_position in enemy_bodies:
            remove.append(move)

    possible_moves = [move for move in possible_moves if move not in remove]
    return possible_moves

def filter_bad_moves(curr_snake: list, possible_moves: list, board: dict):
    possible_moves = filter_self_collision(curr_snake, possible_moves)
    possible_moves = filter_border_collision(curr_snake, possible_moves, board)
    possible_moves = filter_enemy_collision(curr_snake, possible_moves, board['snakes'])

    return possible_moves
