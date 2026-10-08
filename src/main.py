from contextlib import nullcontext
from enum import StrEnum
from operator import index
import random

class CardName(StrEnum):
    PROVINCE = "Province"
    GOLD = "Gold"
    DUCHY = "Duchy"
    SMITHY = "Smithy"
    VILLAGE = "Village"
    SILVER = "Silver"
    ESTATE = "Estate"
    COPPER = "Copper"

class CardType(StrEnum):
    TREASURE = "Treasure"
    VICTORY = "Victory"
    ACTION = "Action"

CARD_COSTS = {
    CardName.PROVINCE: 8,
    CardName.GOLD: 6,
    CardName.DUCHY: 5,
    CardName.SMITHY: 4,
    CardName.VILLAGE: 3,
    CardName.SILVER: 3,
    CardName.ESTATE: 2,
    CardName.COPPER: 0,
}

CARD_TYPES = {
    CardName.PROVINCE: CardType.VICTORY,
    CardName.GOLD: CardType.TREASURE,
    CardName.DUCHY: CardType.VICTORY,
    CardName.SMITHY: CardType.ACTION,
    CardName.VILLAGE: CardType.ACTION,
    CardName.SILVER: CardType.TREASURE,
    CardName.ESTATE: CardType.VICTORY,
    CardName.COPPER: CardType.TREASURE,
}

COINS_FOR_TREASURE_CARDS = {
    CardName.GOLD: 3,
    CardName.SILVER: 2,
    CardName.COPPER: 1,
}

VICTORY_POINTS_FOR_VICTORY_CARDS = {
    CardName.PROVINCE: 6,
    CardName.DUCHY: 3,
    CardName.ESTATE: 1,
}

class Card:
    def __init__(self, name: CardName):
        self.name = name
        self.coins = 0
        self.victory_points = 0
        self.cost = CARD_COSTS[name]
        self.type = CARD_TYPES[name]
        if CARD_TYPES[name] == CardType.TREASURE:
            self.coins = COINS_FOR_TREASURE_CARDS[name]
        elif CARD_TYPES[name] == CardType.VICTORY:
            self.victory_points = VICTORY_POINTS_FOR_VICTORY_CARDS[name]
        


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
    def count_action_cards_in_hand(self):
        return len([card for card in self.hand if card.type == CardType.ACTION])


    # play_action_cards --->  play_action_card ||| play_treasure_cards ||| buy_cards ||| end_turn

    def play_action_cards(self):
        while self.action > 0 and self.count_action_cards_in_hand() > 0:
            for card in self.hand:
                if card.name == CardName.VILLAGE:
                    self.play_action_card(card)
                    break
            for card in self.hand:
                if card.name == CardName.SMITHY:
                    self.play_action_card(card)
                    break
        return



    
            

    def play_treasure_cards(self):
        for card in list(self.hand):            
            if card.type == CardType.TREASURE:
                self.coins += card.coins
                self.Cards_played.append(card)
                self.hand.remove(card)
        return

    # combine play_action_card and play_card  : 
    """
    def play_card(self, card: Card, index: int):
        # dont use index
        if card.type == CardType.VICTORY:
            self.Cards_played.append(self.hand.pop(index))
        elif card.type == CardType.TREASURE:
            self.coins += card.coins
            self.Cards_played.append(self.hand.pop(index))
        elif card.type == CardType.ACTION and self.action == 0:
            self.Cards_played.append(self.hand.pop(index))
        return

    """

    def play_action_card(self, card: Card):
        self.action -= 1
        self.Cards_played.append(card)
        self.hand.remove(card)
        if card.name == CardName.VILLAGE:
            self.cards_to_draw += 1
            self.action += 2
            self.draw_cards()
            print(f"The player {self.player_name} played a Village")
        elif card.name == CardName.SMITHY:
            self.cards_to_draw += 3
            self.draw_cards()
            print(f"The player {self.player_name} played a smithy and he drew 3 more cards")
        return
        

    # understnad how to do it better?
    def buy_cards(self):
        while self.cards_to_buy > 0:
            print(f"The player {self.player_name} has {self.cards_to_buy} more cards to buy")
            if self.coins == 3 and shop[CardName.VILLAGE] > 0 and shop[CardName.SILVER] > 0: # if the player has enough coins, he can buy an estate
                random_card = random.choice([CardName.SILVER, CardName.VILLAGE])
                self.buy_card(random_card)
                break
            for card_name, amount in shop.items():
                if self.coins >= CARD_COSTS[card_name] and amount > 0:
                    self.buy_card(card_name)
                    break
    def buy_card(self, card_name: CardName):
        new_card = Card(card_name)
        self.discard_p.append(new_card)
        shop[card_name] -= 1
        print(f"The player {self.player_name} bought a {card_name}")
        if new_card.type == CardType.VICTORY:
            self.victory_points += VICTORY_POINTS_FOR_VICTORY_CARDS[new_card.name] 
        elif new_card.type == CardType.TREASURE:
            self.coins += COINS_FOR_TREASURE_CARDS[new_card.name]
        self.cards_to_buy -= 1
        return

    def end_turn(self):
        while len(self.hand) > 0:
            self.discard_p.append(self.hand.pop(0))
        while len(self.Cards_played) > 0:
            self.discard_p.append(self.Cards_played.pop(0))
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.action = 1
        self.coins = 0
        return

shop = { # for 2 players
    CardName.PROVINCE: 8,
    CardName.GOLD: 30,
    CardName.DUCHY: 8,    
    CardName.SMITHY: 10,
    CardName.VILLAGE: 10,
    CardName.SILVER: 40,
    CardName.ESTATE: 8,
    CardName.COPPER: 46
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

    """
    draw cards
    play action cards
    play treasure cards
    buy cards
    end turn
    """

def play_turn(player: Player):  
    player.draw_cards() # draw 5 cards
    player.play_action_cards()
    player.play_treasure_cards()
    player.buy_cards()
    player.end_turn()
    # print(player)


    

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
# remove the duplicate code
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

        
        