from contextlib import nullcontext
from enum import StrEnum
import random

class CardName(StrEnum):
    COPPER = "Copper"
    SILVER = "Silver"
    GOLD = "Gold"
    ESTATE = "Estate"
    DUCHY = "Duchy"
    PROVINCE = "Province"
    SMITHY = "Smithy"
    VILLAGE = "Village"

class CardType(StrEnum):
    TREASURE = "Treasure"
    VICTORY = "Victory"
    ACTION = "Action"

class Card:

    def __init__(self, name: CardType):
        self.name = name
        self.coins = 0
        self.victory_points = 0
        if name == CardName.COPPER:
            self.coins = 1
            self.cost = 0
            self.type = CardType.TREASURE
        elif name == CardName.SILVER:
            self.coins = 2
            self.cost = 3
            self.type = CardType.TREASURE
        elif name == CardName.GOLD:
            self.coins = 3
            self.cost = 6
            self.type = CardType.TREASURE
        elif name == CardName.ESTATE:
            self.victory_points = 1
            self.cost = 2
            self.type = CardType.VICTORY
        elif name == CardName.DUCHY:
            self.victory_points = 3
            self.cost = 5
            self.type = CardType.VICTORY
        elif name == CardName.PROVINCE:
            self.victory_points = 6
            self.cost = 8
            self.type = CardType.VICTORY
        elif name == CardName.SMITHY:
            self.cost = 4
            self.type = CardType.ACTION
        elif name == CardName.VILLAGE:
            self.cost = 3
            self.type = CardType.ACTION
        else:
            raise ValueError("Invalid card name")   


    def __repr__(self) -> str:
        return f"{self.name} ({self.cost})"


class Player: 
    def __init__(self, player_name: str):
        self.player_name = player_name
        start = []
        for _ in range(7):
            start.append(Card(CardName.COPPER))
        for _ in range(3):
            start.append(Card(CardName.ESTATE))
        self.drow_p = []
        self.discard_p = start
        self.hand = []
        self.victory_points = 3
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.coins = 0
        self.action = 1
        self.Cards_played = []

    def __repr__(self) -> str:
        return f"{self.player_name} has {self.victory_points} victory points and {self.hand} cards in his hand and {self.discard_p} cards in his discard pile and {self.drow_p} cards in his draw pile"


    def shuffle_discard_into_drow(self):
        random.shuffle(self.discard_p)
        self.drow_p.extend(self.discard_p)
        self.discard_p = []
        print("shuffled discard into_drow")

    def print_dack (self):
        count_cards = 0
        for card in self.drow_p:
            print(card.name)
            count_cards += 1
        for card in self.discard_p:
            print(card.name)
            count_cards += 1
        for card in self.hand:
            print(card.name)
            count_cards += 1
        print("The player " + self.player_name + " has " + str(count_cards) + " cards in his dack")

    def draw_cards(self):
        while self.cards_to_draw > 0:
            if len(self.discard_p) == 0 and len(self.drow_p) == 0:
                print(f"The player {self.player_name} no more cards to draw the player use all of his cards")
                self.cards_to_draw = 0
                return
            if len(self.drow_p) == 0:
                self.shuffle_discard_into_drow()
            self.hand.append(self.drow_p.pop(0))
            self.cards_to_draw -= 1
        return 

    def count_action_cards_in_hand(self):
        return sum(1 for card in self.hand if card.type == CardType.ACTION)

    def choose_and_play_action_cards(self):
        index = 0
        while index < len(self.hand):
            if self.hand[index].type == CardType.ACTION and self.hand[index].name == CardName.VILLAGE:
                self.play_action_card(self.hand[index], index)
                return
            index += 1
        index = 0
        while index < len(self.hand):
            if self.hand[index].type == CardType.ACTION and self.hand[index].name == CardName.SMITHY:
                self.play_action_card(self.hand[index], index)
                return
            index += 1
        return
            
    def play_hand_cards(self):
        while self.action > 0 and self.count_action_cards_in_hand() > 0:
            self.choose_and_play_action_cards()
        while len(self.hand) > 0:
            self.play_card(self.hand[0], 0)
        return


    def play_card(self, card: Card, index: int):
        if card.type == CardType.VICTORY:
            self.Cards_played.append(self.hand.pop(index))
        elif card.type == CardType.TREASURE:
            self.coins += card.coins
            self.Cards_played.append(self.hand.pop(index))
        elif card.type == CardType.ACTION and self.action == 0:
            self.Cards_played.append(self.hand.pop(index))
        return

    def play_action_card(self, card: Card, index: int):
        self.action -= 1
        if card.name == CardName.VILLAGE:
            self.cards_to_draw += 1
            self.action += 2
            self.Cards_played.append(self.hand.pop(index))
            self.draw_cards()
            print(f"The player {self.player_name} played a Village")
            return
        elif card.name == CardName.SMITHY:
            self.cards_to_draw += 3
            self.Cards_played.append(self.hand.pop(index))
            self.draw_cards()
            print(f"The player {self.player_name} played a smithy and he drew 3 more cards")
            return
        return
        

    def choose_card_to_buy(self):
        while self.cards_to_buy > 0:
            random_card = random.choice([CardName.SILVER, CardName.VILLAGE])
            print("The player " + self.player_name + " has " + str(self.cards_to_buy) + " more cards to buy")
            if self.coins >= 8 and shop["Province"] > 0: # if the player has enough coins, he can buy a province
                self.buy_card(CardName.PROVINCE)
            elif self.coins >= 6 and shop["Gold"] > 0: # if the player has enough coins, he can buy a gold
                self.buy_card(CardName.GOLD)
            elif self.coins >= 5 and shop["Duchy"] > 0: # if the player has enough coins, he can buy a duchy
                self.buy_card(CardName.DUCHY)
            elif self.coins >= 4 and shop["Smithy"] > 0: # if the player has enough coins, he can buy a smithy
                self.buy_card(CardName.SMITHY)
            elif self.coins >= 3 and shop["Village"] > 0 and shop["Silver"] > 0: # if the player has enough coins, he can buy an estate
                self.buy_card(random_card)
            elif self.coins >= 3 and shop["Village"] > 0: # if the player has enough coins, he can buy a village
                self.buy_card(CardName.VILLAGE)
            elif self.coins >= 3 and shop["Silver"] > 0: # if the player has enough coins, he can buy an estate
                self.buy_card(CardName.SILVER)
            elif self.coins >= 2 and shop["Estate"] > 0: # if the player has enough coins, he can buy an estate
                self.buy_card(CardName.ESTATE)
            elif self.coins >= 0 and shop["Copper"] > 0: # if the player no money, he can buy a copper
                self.buy_card(CardName.COPPER)


    def buy_card(self, card_name: CardName):
        self.discard_p.append(Card(card_name))
        shop[card_name] -= 1
        print(f"The player {self.player_name} bought a {card_name}")
        self.coins -= Card(card_name).cost # did it correctly?
        self.cards_to_buy -= 1
        self.victory_points += Card(card_name).victory_points # did it correctly?
        return            

    def end_turn(self):
        if len(self.hand) > 0:
            print("eror!!!!!!!!")
        while len(self.Cards_played) > 0:
            self.discard_p.append(self.Cards_played.pop(0))
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.action = 1
        self.coins = 0
        return
    
shop = { # name, amount after divide for 2 players
    "Copper": 46,
    "Silver": 40,
    "Gold": 30,
    "Estate": 8,
    "Duchy": 8,
    "Province": 8,    
    "Smithy": 10,
    "Village": 10,
}

def game_over():
    print("The game is over")
    if Aviv.victory_points > Moshe.victory_points:
        print("Aviv won the game")
    elif Aviv.victory_points < Moshe.victory_points:
        print("Moshe won the game")
    else:
        print("The game is a draw")
    print("--------------------------------")
    print(f"Aviv has {Aviv.victory_points} victory points")
    Aviv.print_dack()
    print("--------------------------------")
    print(f"Moshe has {Moshe.victory_points} victory points")
    Moshe.print_dack()

def count_empty_paket_in_shop():
    return sum(1 for amount in shop.values() if amount == 0)

def play_turn(player: Player):  
    player.draw_cards() # draw 5 cards
    player.play_hand_cards()
    player.choose_card_to_buy()
    player.end_turn()
    print(player)


    

Aviv = Player ("Aviv")
Moshe = Player ("Moshe")
Aviv.shuffle_discard_into_drow()
Moshe.shuffle_discard_into_drow()
print(Aviv.drow_p)
print(Moshe.drow_p)
for card in Aviv.drow_p:
    print(f"{card.name}")
print("--------------------------------")
for card in Moshe.drow_p:
    print(f"{card.name}")
print("--------------------------------")

Aviv_turn = True # Aviv's start
# Moshe_turn = False # Moshe's second start 

victory_points_to_win = 60
while True:
    if count_empty_paket_in_shop() >= 3:
        print("3 packets in shop are empty")
        break
    if Aviv_turn == True:
        play_turn(Aviv)
        Aviv_turn = False
        print(f"Aviv's turn is over Aviv have {Aviv.victory_points} victory points")
        if Aviv.victory_points >= victory_points_to_win:
            break
    else:
        play_turn(Moshe)
        print(f"Moshe's turn is over Moshe have {Moshe.victory_points} victory points")
        Aviv_turn = True
        if Moshe.victory_points >= victory_points_to_win:
            break
game_over()

        
        