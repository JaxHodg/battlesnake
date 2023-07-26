def filter_border_collision(curr_snake: list, possible_moves: list, board: dict):
    remove = []
    for move in possible_moves:
        new_position = move['transform'](curr_snake)
        if new_position['x'] < 0 \
            or new_position['x'] >= board['width'] \
            or new_position['y'] < 0 \
            or new_position['y'] >= board['height']:
            remove.append(move)

    possible_moves = [move for move in possible_moves if move not in remove]
    return possible_moves

def filter_enemy_collision(curr_snake_id: int, curr_snake: dict, possible_moves: list, enemies: dict):
    enemy_bodies = []
    self_body = []
    for enemy in enemies:
        if enemy['id'] == curr_snake_id:
            enemy = enemy['body']
            for body in enemy:
                self_body.append(body)
        else:
            enemy = enemy['body']
            for body in enemy:
                enemy_bodies.append(body)
    
    remove = []
    for move in possible_moves:
        new_position = move['transform'](curr_snake)
        if new_position in self_body[:-1]:
            remove.append(move)
        if new_position in enemy_bodies:
            remove.append(move)

    possible_moves = [move for move in possible_moves if move not in remove]
    return possible_moves

def filter_bad_moves(curr_snake_id, curr_snake_pos: dict, possible_moves: list, board: dict):
    possible_moves = filter_border_collision(curr_snake_pos, possible_moves, board)
    possible_moves = filter_enemy_collision(curr_snake_id, curr_snake_pos, possible_moves, board['snakes'])

    return possible_moves
