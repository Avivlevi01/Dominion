from __future__ import annotations
from contextlib import nullcontext
from operator import index
from cards import shop, reset_shop, reset_trash
from player import Player
from cards import CardName, get_amount_of_card_in_shop


def count_empty_paket_in_shop():
    return sum(1 for amount in shop.values() if amount == 0)


def play_turn(player: Player):  
    player.draw_cards() 
    player.play_action_cards()
    player.play_treasure_cards()
    player.buy_cards()
    player.end_turn()

def start_game(player1: Player, player2: Player):
    reset_shop()
    reset_trash()
    player1.reset_player()
    player2.reset_player()

    while True:
        play_turn(player1)
        if count_empty_paket_in_shop() >= 3 or get_amount_of_card_in_shop(CardName.PROVINCE) == 0:
            return game_over(player1, player2)
        play_turn(player2)
        if count_empty_paket_in_shop() >= 3 or get_amount_of_card_in_shop(CardName.PROVINCE) == 0:
            return game_over(player1, player2)



def game_over(player1: Player, player2: Player) -> str:
            if player1.victory_points > player2.victory_points:
                return player1.player_name
            elif player1.victory_points < player2.victory_points:
                return player2.player_name
            else:
                return "draw"