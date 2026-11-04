from player import Player
from game import start_game

Aviv = Player ("Aviv")
Moshe = Player ("Moshe")
Aviv.shuffle_discard_into_drow()
Moshe.shuffle_discard_into_drow()

start_game(Aviv, Moshe)