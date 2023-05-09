import time

# Fonction décorateur pour mesurer le temps d'exécution de l'algorithme Alpha-Beta
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(result, elapsed_time)
        return result, elapsed_time

    return wrapper


class Player:
    # Constructeur pour la classe Player
    def __init__(self, player_number):
        self.player_number = player_number
    # Méthode pour obtenir un mouvement
    def get_move(self, board, **kwargs):
        pass
