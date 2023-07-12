from math import inf
import json
from const import Direction


def move_snake(game_state: dict, snake: dict, move: Direction) -> dict:
    '''
    parameter:
        game state: dictionary of game metadata (snake locations)
        snake: snake to move
        move: tuple of coordinates to move

    returns updated game_state
    '''

    snake['head'] = move.value['transform'](snake['head'])

    if snake['head']['x'] < 0 or snake['head']['x'] > game_state['board']['width']:
        raise Exception("Out of bounds")
    if snake['head']['y'] < 0 or snake['head']['y'] > game_state['board']['height']:
        raise Exception("Out of bounds")

    snake["body"] = snake['head'] + snake["body"][:-1]

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


def rec_find_move(game_state: dict, snakes: list):
    '''
    parameter:
        game state: dictionary of game metadata (snake locations)
        next_snake: list of snakes ordered by when they move (index 0 is next snake to move)

    returns tuple of (list of moves, best score possible in tree)
    '''

    if not snakes:
        return ([], score_game_board(game_state))

    curr_snake = snakes[0]

    best_move_arr = []
    best_move_score = -inf

    for move in Direction:
        move_arr, move_score = rec_find_move(
            move_snake(game_state, curr_snake, move),
            snakes[1:]
        )

        # Assume every snake chooses best move for them
        if move_score[curr_snake] > best_move_score:
            best_move_score = move_score[curr_snake]
            best_move_arr = [(curr_snake, move)] + move_arr

    return (best_move_arr, best_move_score)


# General Algo:
#   Recurse through every snake's possible moves
#

with open('move.json', 'r') as f:
    game_state = json.load(f)

rec_find_move(game_state, game_state['board']['snakes'] * 5)
