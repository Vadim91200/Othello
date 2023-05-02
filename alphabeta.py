import cProfile
import io
import pstats
import const
import random
import time


class State:
    def __init__(self, depth):
        self.depth = depth

    def get_all_moves(self, player):
        pass

    def evaluate(self, player, depth):
        pass

    def is_end(self):
        pass

    def apply_move(self, move, player):
        pass

    def copy(self):
        pass


DEFAULT_DEPTH = 6


def max_value(state, player, alpha=float('-inf'), beta=float('inf'), depth=DEFAULT_DEPTH):
    if depth == 0 or state.is_end():
        return state.evaluate(player, depth), None

    v = float('-inf')
    best_move = None

    all_moves = state.get_all_moves(player)
    for move in all_moves:
        next_state = state.copy().apply_move(tuple(move), player)
        e, _ = min_value(next_state, 1 + player % 2, alpha, beta, depth - 1)
        if e > v:
            v = e
            best_move = move

        if v >= beta:
            break
        alpha = max(alpha, v)

    return v, best_move


def min_value(state, player, alpha=float('-inf'), beta=float('inf'), depth=DEFAULT_DEPTH):
    if depth == 0 or state.is_end():
        return state.evaluate(player, depth), None

    v = float('inf')
    best_move = None
    all_moves = state.get_all_moves(player)
    for move in all_moves:
        next_state = state.copy().apply_move(move, player)
        e, _ = max_value(next_state, 1 + player % 2, alpha, beta, depth - 1)
        if e < v:
            v = e
            best_move = move

        if v <= alpha:
            break
        beta = min(beta, v)

    return v, best_move


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        # to do : changer plus tard
        # pr = cProfile.Profile()
        # pr.enable()
        # result = func(*args, **kwargs)
        # pr.disable()
        # pr.print_stats()
        # print(result)
        # return result
        t = time.time()
        result = func(*args, **kwargs)
        print(time.time() - t)
        return result
    return wrapper


@timer_decorator
def alphabeta_search(state, player):
    return max_value(state, player, depth=state.depth)[1]
