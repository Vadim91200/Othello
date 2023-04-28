import const
import random
import time

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
    random.shuffle(all_moves)
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
    random.shuffle(all_moves)
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
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.5f} seconds to execute.")
        return result
    return wrapper

@timer_decorator
def alphabeta_search(state, player):
    return max_value(state)[1] if player == const.FIRST_PLAYER else min_value(state)[1]
