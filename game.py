from __future__ import annotations
from contextlib import nullcontext
from enum import StrEnum
from operator import index
import random

from cards import shop
from player import Player


def check_game_over(aviv: Player, moshe: Player):
    if count_empty_paket_in_shop() >= 3:
        print(f"3 packets in shop are empty")
        print(f"The game is over")
        if aviv.victory_points > moshe.victory_points:
            print(f"{aviv.player_name} won the game")
        elif aviv.victory_points < moshe.victory_points:
            print(f"{moshe.player_name} won the game")
        else:
            print(f"The game is a draw")
        print(f"--------------------------------")
        print(f"{aviv.player_name} has {aviv.victory_points} victory points")
        aviv.print_dack()
        print(f"--------------------------------")
        print(f"{moshe.player_name} has {moshe.victory_points} victory points")
        moshe.print_dack()
        return True
    return False

def count_empty_paket_in_shop():
    return sum(1 for amount in shop.values() if amount == 0)


def play_turn(player: Player):  
    player.draw_cards() # draw 5 cards
    player.play_action_cards()
    player.play_treasure_cards()
    player.buy_cards()
    player.end_turn()
    # print(player)


def start_game(player1: Player, player2: Player):
    while True:
        if check_game_over(player1, player2):
            break
        play_turn(player1)
        print(f"{player1.player_name}'s turn is over {player1.player_name} have {player1.victory_points} victory points")
        if check_game_over(player1, player2):
            break
        play_turn(player2)
        print(f"{player2.player_name}'s turn is over {player2.player_name} have {player2.victory_points} victory points")
    return
