from math import inf
import json


def move_snake(game_state: dict, snake_id: int, move: tuple) -> dict:
    '''
    parameter:
        game state: dictionary of game metadata (snake locations)
        snake_id: snake ID to move
        move: tuple of coordinates to move

    returns updated game_state
    '''
    if not move in {(0, 1), (1, 0), (0, -1), (-1, 0)}:
        raise Exception("Invalid Move")

    for snake in game_state['board']['snakes']:
        if snake['id'] == snake_id:
            snake['head']['x'] += move[0]
            snake['head']['y'] += move[1]

            snake['health'] -= 1
            if snake['head'] in snake['board']['food']:
                snake['health'] = 100
                snake['board']['food'].remove(snake['head'])

            if snake['health'] < 5:
                raise Exception("Out of health")

            if snake['head']['x'] < 0 or snake['head']['x'] > game_state['board']['width']:
                raise Exception("Out of bounds")
            if snake['head']['y'] < 0 or snake['head']['y'] > game_state['board']['height']:
                raise Exception("Out of bounds")

            snake["body"] = \
                [{'x': snake['head']['x'], 'y': snake['head']['y']}] + \
                snake["body"][:-1]

        return game_state


def score_game_board(game_state: dict) -> dict:
    '''
    parameter:          
        game state: dictionary of game metadata (snake locations)

    returns map of snake IDs to a score
    '''

    # Flood Fill Algo?
    W = game_state['board']['width']
    H = game_state['board']['height']

    board = [[""] * W] * H

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

        if is_valid(x + 1, y):
            q.append({'id': id, 'x': x + 1, 'y': y})

        if is_valid(x - 1, y):
            q.append({'id': id, 'x': x - 1, 'y': y})

        if is_valid(x, y + 1):
            q.append({'id': id, 'x': x, 'y': y + 1})

        if is_valid(x, y - 1):
            q.append({'id': id, 'x': x, 'y': y - 1})

    snake_to_score = dict()
    for i in board:
        for j in i:
            if j not in snake_to_score:
                snake_to_score[j] = 0
            snake_to_score[j] += 1

    return snake_to_score


def rec_find_move(game_state: dict, next_snake: list):
    '''
    parameter:
        game state: dictionary of game metadata (snake locations)
        next_snake: list of snakes ordered by when they move (index 0 is next snake to move)

    returns tuple of (list of moves, best score possible in tree)
    '''

    if not next_snake:
        return ([], score_game_board(game_state))

    snake_id = next_snake[0]

    best_move_arr = []
    best_move_score = None

    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        try:
            move_arr, move_score = rec_find_move(
                move_snake(game_state, snake_id, move),
                next_snake[1:]
            )

            # Assume every snake chooses best move for them
            if not best_move_score or move_score[snake_id] > best_move_score[snake_id]:
                best_move_score = move_score
                best_move_arr = [(snake_id, move)] + move_arr
        except:
            pass

    return (best_move_arr, best_move_score)


# General Algo:
#   Recurse through every snake's possible moves
def find_move(game_state):
    snake_ids = [snake['id'] for snake in game_state['board']['snakes']]

    res = rec_find_move(game_state, snake_ids)

    move_to_text = {
        (0, 1): 'up',
        (0, -1): 'down',
        (1, 0): 'right',
        (-1, 0): 'left'
    }

    for move in res[0]:
        if move[0] == game_state['you']['id']:
            return move_to_text(move[1])
