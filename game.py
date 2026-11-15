from __future__ import annotations
from contextlib import nullcontext
from enum import StrEnum
from operator import index
import random

# classes
#   card, player
#   game, strategy, main

class CardName(StrEnum):
    PROVINCE = "Province"
    GOLD = "Gold"
    DUCHY = "Duchy"
    SMITHY = "Smithy"
    VILLAGE = "Village"
    SILVER = "Silver"
    ESTATE = "Estate"
    COPPER = "Copper"
    REMODEL = "Remodel" 

class CardType(StrEnum):
    TREASURE = "Treasure"
    VICTORY = "Victory"
    ACTION = "Action"



class Card:

    def __init__(self, name: CardName, cost: int = 0, type: CardType = CardType, coins: int = 0, victory_points: int = 0):
        self.name = name
        self.cost = cost
        self.type = type
        self.coins = coins
        self.victory_points = victory_points



    def __repr__(self) -> str:
        return f"{self.name} ({self.cost})"


    @staticmethod
    def create(card_name: CardName):
        original_card = cards[card_name]
        new_card = Card(name=original_card.name, cost=original_card.cost, type=original_card.type, coins=original_card.coins, victory_points=original_card.victory_points)
        return new_card
    

cards = {
    CardName.PROVINCE: Card(name=CardName.PROVINCE, cost=8, type=CardType.VICTORY, victory_points=6),
    CardName.GOLD: Card(name=CardName.GOLD, cost=6, type=CardType.TREASURE, coins=3),
    CardName.DUCHY: Card(name=CardName.DUCHY, cost=5, type=CardType.VICTORY, victory_points=3),
    CardName.REMODEL: Card(name=CardName.REMODEL, cost=4, type=CardType.ACTION),
    CardName.SMITHY: Card(name=CardName.SMITHY, cost=4, type=CardType.ACTION),
    CardName.VILLAGE: Card(name=CardName.VILLAGE, cost=3, type=CardType.ACTION),
    CardName.SILVER: Card(name=CardName.SILVER, cost=2, type=CardType.TREASURE, coins=2),
    CardName.ESTATE: Card(name=CardName.ESTATE, cost=2, type=CardType.VICTORY, victory_points=1),
    CardName.COPPER: Card(name=CardName.COPPER, cost=0, type=CardType.TREASURE, coins=1),
}

trash = []

def push_to_trash(card: Card):
    trash.append(card)
    return

shop = { # for 2 players
    CardName.PROVINCE: 8,
    CardName.GOLD: 30,
    CardName.DUCHY: 8,
    CardName.REMODEL: 10,  
    CardName.SMITHY: 10,
    CardName.VILLAGE: 10,
    CardName.SILVER: 40,
    CardName.ESTATE: 8,
    CardName.COPPER: 46
}

def get_amount_of_card_in_shop(card_name: CardName):
    return shop[card_name]


def remove_card_from_shop(card_name: CardName):
    shop[card_name] -= 1
    return


def find_expensive_card_in_shop_by_coins(money_to_buy_new_card: int): # have a problem with this function, it returns the first card found and I order it to return the most expensive card becosuse the order is top to bottom
    expensive_card = None
    for card_name, amount in shop.items():
        if money_to_buy_new_card >= cards[card_name].cost and amount > 0:
            expensive_card = Card.create(card_name)
            break
    return expensive_card # if no card is found, return None


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
