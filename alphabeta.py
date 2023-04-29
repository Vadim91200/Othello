import cProfile
import io
import pstats
import const
import random


class State:
    def get_all_moves(self, player):
        pass

    def evaluate(self, depth):
        pass

    def is_end(self):
        pass

    def apply_move(self, move, player):
        pass

    def copy(self):
        pass


DEPTH = 6


def max_value(state, alpha=float('-inf'), beta=float('inf'), depth=DEPTH):
    if depth == 0 or state.is_end():
        return state.evaluate(depth), None

    v = float('-inf')
    best_move = None

    all_moves = state.get_all_moves(const.FIRST_PLAYER)
    for move in all_moves:
        next_state = state.copy().apply_move(tuple(move), const.FIRST_PLAYER)
        e, _ = min_value(next_state, alpha, beta, depth - 1)
        if e > v:
            v = e
            best_move = move

        alpha = max(alpha, v)
        if beta <= alpha:
            break

    return v, best_move


def min_value(state, alpha=float('-inf'), beta=float('inf'), depth=DEPTH):
    if depth == 0 or state.is_end():
        return state.evaluate(depth), None

    v = float('inf')
    best_move = None
    all_moves = state.get_all_moves(const.SECOND_PLAYER)
    for move in all_moves:
        next_state = state.copy().apply_move(move, const.SECOND_PLAYER)
        e, _ = max_value(next_state, alpha, beta, depth - 1)
        if e < v:
            v = e
            best_move = move

        beta = min(beta, v)
        if beta <= alpha:
            break

    return v, best_move


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        pr.print_stats()
        return result

    return wrapper


@timer_decorator
def alphabeta_search(state, player):
    return max_value(state)[1] if player == const.FIRST_PLAYER else min_value(state)[1]
