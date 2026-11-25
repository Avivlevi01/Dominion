from player import Player
from easy_strategy import EasyStrategy
from hard_strategy import HardStrategy
from game import start_game

Aviv = Player ("Aviv", EasyStrategy())
Moshe = Player ("Moshe", HardStrategy())
Aviv_wins = 0
Moshe_wins = 0
draw_wins = 0
for i in range(100):
    winner = start_game(Aviv, Moshe)
    if winner == "Aviv":
        Aviv_wins += 1
    elif winner == "Moshe":
        Moshe_wins += 1
    else:
        draw_wins += 1
    print(f"The winner of the match is {winner}")
    print(f"--------------------------------")

print(f"Aviv won {Aviv_wins} times")
print(f"Moshe won {Moshe_wins} times")
print(f"Draw {draw_wins} times")

    
