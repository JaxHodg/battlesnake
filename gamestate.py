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

    snake_to_score = dict()

    for snake in game_state['board']['snakes']:
        snake_to_score[snake['id']] = snake['length']

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
    best_move_score = -inf

    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        move_arr, move_score = rec_find_move(
            move_snake(game_state, snake_id, move),
            next_snake[1:]
        )

        # Assume every snake chooses best move for them
        if move_score[snake_id] > best_move_score:
            best_move_score = move_score[snake_id]
            best_move_arr = [(snake_id, move)] + move_arr

    return (best_move_arr, best_move_score)


# General Algo:
#   Recurse through every snake's possible moves
#

with open('move.json', 'r') as f:
    game_state = json.load(f)

snake_ids = [snake['id'] for snake in game_state['board']['snakes']]

rec_find_move(game_state, snake_ids * 5)
