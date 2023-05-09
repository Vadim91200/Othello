import const


class State:
    def __init__(self, depth, is_only_maximising):
        self.depth = depth
        self.is_only_maximising = is_only_maximising

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


def max_value(state, player, depth, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or state.is_end():
        return state.evaluate(player, depth), None

    v = float('-inf')
    best_move = None

    for move in state.get_all_moves(player):
        e, _ = min_value(state.copy().apply_move(move, player), 1 + player % 2, depth - 1, alpha, beta)
        if e > v:
            v = e
            best_move = move
        elif e == v and best_move is None:
            best_move = move

        if v >= beta:
            break
        alpha = max(alpha, v)

    return v, best_move


def min_value(state, player, depth, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or state.is_end():
        return state.evaluate(player, depth), None

    v = float('inf')
    best_move = None

    for move in state.get_all_moves(player):
        e, _ = max_value(state.copy().apply_move(move, player), 1 + player % 2, depth - 1, alpha, beta)
        if e < v:
            v = e
            best_move = move
        elif e == v and best_move is None:
            best_move = move

        if v <= alpha:
            break
        beta = min(beta, v)

    return v, best_move


def alphabeta_search(state, player):
    return max_value(state, player, state.depth)[1] \
        if state.is_only_maximising or player == const.FIRST_PLAYER \
        else min_value(state, player, state.depth)[1]
