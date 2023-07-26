import json
from collections import defaultdict
from copy import deepcopy
from const import MOVES
from filter_bad_moves import filter_bad_moves


def move_snake(old_game_state: dict, snake_id: str, move: dict) -> dict:
    '''
    parameter:
        old_game_state: full json dict of game data
        snake_id: snake ID to move
        move: tuple representing change in coordinates

    returns updated game_state
    '''

    # Copies state
    game_state = deepcopy(old_game_state)

    # Creates set of coords on board that cause death
    hazards = set()
    for h in game_state['board']['hazards']:
        hazards.add(tuple(h.values()))
    for snake in game_state['board']['snakes']:
        for b in snake['body']:
            hazards.add(tuple(b.values()))

    # Searches for snake in board
    for snake in game_state['board']['snakes']:
        if snake['id'] == snake_id:
            # Moves snake's head
            snake['head'] = move['transform'](snake['head'])

            # Verifies head not in neck
            if len(snake['body']) >= 2 and snake['head'] == snake['body'][1]:
                raise Exception("Hit Neck")

            # Verifies head not in hazard
            if tuple(snake['head'].values()) in hazards:
                raise Exception("Hit Hazard")

            # Subtacts health
            snake['health'] -= 1
            # Handles food logic
            if snake['head'] in game_state['board']['food']:
                snake['health'] = 100
                game_state['board']['food'].remove(snake['head'])

            # Verifies health is not empty
            if snake['health'] < 1:
                raise Exception("Out of health")

            # Verifies head not out of bounds
            if snake['head']['x'] < 0 or game_state['board']['width'] <= snake['head']['x']:
                raise Exception("Out of bounds")
            if snake['head']['y'] < 0 or game_state['board']['height'] <= snake['head']['y']:
                raise Exception("Out of bounds")

            # Updates body coordinates
            snake["body"] = \
                [{'x': snake['head']['x'], 'y': snake['head']['y']}] + \
                snake["body"][:-1]

            return game_state


def delete_snake(old_game_state: dict, snake_id: str) -> dict:
    '''
    parameter:
        old_game_state: full json dict of game data
        snake_id: snake ID to delete

    returns updated game_state
    '''

    game_state = deepcopy(old_game_state)

    for snake in game_state['board']['snakes']:
        if snake['id'] == snake_id:
            game_state['board']['snakes'].remove(snake)
            return game_state


def score_game_board(game_state: dict) -> dict:
    '''
    parameter:
        game_state: full json dict of game data

    returns dict of snake_id to float score
    '''

    # Gets scores from both algorithms
    snake_flood_score = get_flood_score(game_state)
    snake_length_score = get_length_score(game_state)

    # Combines scores together
    snake_to_score = defaultdict(float)

    for k, v in snake_flood_score.items():
        snake_to_score[k] += v

    for k, v in snake_length_score.items():
        snake_to_score[k] += v

    return snake_to_score


def get_flood_score(game_state: dict) -> dict:
    '''
    parameter:
        game state: full json dict of game data

    returns map of snake IDs to a float score (based on floodfill)
    '''

    # Flood Fill Algo?
    W = game_state['board']['width']
    H = game_state['board']['height']

    board = [[""] * H] * W

    q = list()

    for snake in game_state['board']['snakes']:
        # Adds head to queue
        q.append(snake['head'] | {'id': snake['id']})

        # Marks area where snake sits as controlled
        for b in snake['body']:
            board[b['x']][b['y']] = snake['id']

    def is_valid(x, y):
        if x < 0 or W <= x:
            return False
        if y < 0 or H <= y:
            return False
        if board[x][y] != '':
            return False
        return True

    # Loops through snake moves until board filled
    while q:
        cur_coord = q.pop(0)
        x = cur_coord['x']
        y = cur_coord['y']
        id = cur_coord['id']

        board[x][y] = id

        valid_moves = filter_bad_moves(id, {'x':x, 'y':y}, MOVES, game_state['board'])

        for move in valid_moves:
            q.append(move['transform']({'x':x, 'y':y}))
            q[-1]['id'] = id

        # if is_valid(x + 1, y):
        #     q.append({'id': id, 'x': x + 1, 'y': y})

        # if is_valid(x - 1, y):
        #     q.append({'id': id, 'x': x - 1, 'y': y})

        # if is_valid(x, y + 1):
        #     q.append({'id': id, 'x': x, 'y': y + 1})

        # if is_valid(x, y - 1):
        #     q.append({'id': id, 'x': x, 'y': y - 1})

    snake_to_score = defaultdict(float)
    for i in board:
        for j in i:
            if j == '':
                continue
            snake_to_score[j] += 1

    total = sum(snake_to_score.values())
    for i in snake_to_score:
        snake_to_score[i] /= total

    return snake_to_score


def get_length_score(game_state: dict) -> dict:
    '''
    parameter:
        game state: full json dict of game data

    returns map of snake IDs to a float score (based on length)
    '''

    snake_to_score = defaultdict(float)

    for snake in game_state['board']['snakes']:
        snake_to_score[snake['id']] = snake['length']

    total = sum(snake_to_score.values())
    for i in snake_to_score:
        snake_to_score[i] /= total

    return snake_to_score

def rec_find_move(game_state: dict, next_snake: list):
    '''
    parameter:
        game state: full json dict of game data
        next_snake: queue of snakes to move

    returns tuple of (list of moves, best score dict possible in tree)
    '''

    # Base case
    if not next_snake:
        return ([], score_game_board(game_state))

    snake_id = next_snake[0]

    best_move_arr = []
    best_move_score = defaultdict(float)

    for move in MOVES:
        try:
            # Recurse when snake moves
            new_game_state = move_snake(game_state, snake_id, move)
            move_arr, move_score = rec_find_move(
                new_game_state,
                next_snake[1:]
            )
        except Exception as e:
            # Recurse when snake dies
            new_game_state = delete_snake(game_state, snake_id)
            move_arr, move_score = rec_find_move(
                new_game_state,
                list(filter(lambda i: i != snake_id, next_snake))
            )

        # Assume current snake_id will choose best move for them
        if move_score[snake_id] >= best_move_score[snake_id]:
            best_move_score = move_score
            best_move_arr = [(snake_id, move)] + move_arr

    return (best_move_arr, best_move_score)


def find_move(game_state):
    '''
    parameter:
        game state: full json dict of game data

    returns str of snake move
    '''

    self_id = game_state['you']['id']

    # Builds list of snake_ids where first is self
    snake_ids = [self_id]
    for snake in game_state['board']['snakes']:
        if snake['id'] == self_id:
            continue
        snake_ids.append(snake['id'])

    res = rec_find_move(game_state, snake_ids * 1)

    print(res)

    # Extracts text move for self snake
    for move in res[0]:
        if move[0] == self_id:
            return move[1]['move']
