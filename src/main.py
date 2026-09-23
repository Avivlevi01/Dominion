import random
class Card:
    def __init__(self, Name: str, Coins: int, Victori_points: int, Cost: int, Type: str):
        self.name = Name
        self.Coins = Coins
        self.Victori_points = Victori_points
        self.Cost = Cost
        self.Type = Type


# cards:
#              name  coins VP cost
copper = Card("Copper", 1, 0,  0, "Treasure")
silver = Card("Silver", 2, 0, 3, "Treasure")
gold = Card("Gold", 3, 0, 6, "Treasure")
estate = Card("Estate", 0, 1, 2, "Victory")
duchy = Card("Duchy", 0, 3, 5, "Victory")
province = Card("Province", 0, 6, 8, "Victory")
Smithy = Card("Smithy", 0, 0, 4, "Action")

class Player: 
    def __init__(self, Player_name: str):
        self.Player_name = Player_name
        start = []
        for _ in range(7):
            start.append(Card("Copper", 1, 0,  0, "Treasure"))
        for _ in range(3):
            start.append(Card("Estate", 0, 1, 2, "Victory"))
        self.Drow_p = []
        self.Discard_p = start
        self.Hand = []
        self.Victory_points = 3
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.coins = 0
        self.action = 1

    def shuffle_discard_into_drow(self):
        random.shuffle(self.Discard_p)
        self.Drow_p.extend(self.Discard_p)
        self.Discard_p = []
        print("X")

    def print_dack (self):
        count_cards = 0
        for card in self.Drow_p:
            print(card.name)
            count_cards += 1
        for card in self.Discard_p:
            print(card.name)
            count_cards += 1
        for card in self.Hand:
            print(card.name)
            count_cards += 1
        print("The player " + self.Player_name + " has " + str(count_cards) + " cards in his dack")

    def draw_card(self):
        if len(self.Discard_p) == 0 and len(self.Drow_p) == 0:
            print("The player " + self.Player_name + " finished his turn and he use all of his cards")
            return False # return false if the player finished his turn and he use all of his cards
        if len(self.Drow_p) == 0:
            self.shuffle_discard_into_drow()
        self.Hand.append(self.Drow_p.pop(0))
        self.cards_to_draw -= 1
        return 

    def play_card(self, card: Card):
        if card.Type == "Victory":
            return
        elif card.Type == "Treasure":
            self.coins += card.Coins
        elif card.Type == "Action" and self.action > 0:
            self.action -= 1
            self.play_action_card(card)
        return

    def play_action_card(self, card: Card):
        if card.name == "Smithy":
            self.cards_to_draw += 3
            print("The player " + self.Player_name + " played a smithy and he drew 3 more cards")
        return

    def buy_treasure(self):
        if self.coins >= 6 and shop["gold"] > 0: # if the player has enough coins, he can buy a gold
            self.Hand.append(Card("Gold", 3, 0, 6, "Treasure"))
            shop["gold"] -= 1
            print("The player " + self.Player_name + " bought a gold")
            self.coins -= 6
        elif self.coins >= 3 and shop["silver"] > 0: # if the player has enough coins, he can buy a silver
            self.Hand.append(Card("Silver", 2, 0, 3, "Treasure"))
            shop["silver"] -= 1
            print("The player " + self.Player_name + " bought a silver")
            self.coins -= 3
        elif self.coins >= 0 and shop["copper"] > 0: # if the player has enough coins, he can buy a copper
            self.Hand.append(Card("Copper", 1, 0, 0, "Treasure"))
            shop["copper"] -= 1
            print("The player " + self.Player_name + " bought a copper")
            self.coins -= 0
        self.cards_to_buy -= 1
        return

    def buy_province(self):
        if self.coins >= 8 and shop["province"] > 0: # if the player has enough coins, he can buy a province
            self.Hand.append(Card("Province", 0, 6, 8, "Victory"))
            shop["province"] -= 1
            print("The player " + self.Player_name + " bought a province")
            self.coins -= 8
            self.cards_to_buy -= 1
            self.Victory_points += 6
        return

    def buy_duchy(self):
        if self.coins >= 5 and shop["duchy"] > 0: # if the player has enough coins, he can buy a duchy
            self.Hand.append(Card("Duchy", 0, 3, 5, "Victory"))
            shop["duchy"] -= 1
            print("The player " + self.Player_name + " bought a duchy")
            self.coins -= 5
            self.cards_to_buy -= 1
            self.Victory_points += 3
        return
    def buy_smithy(self):
        if self.coins >= 4 and shop["smithy"] > 0: # if the player has enough coins, he can buy a smithy
            self.Hand.append(Card("Smithy", 0, 0, 4, "Action"))
            shop["smithy"] -= 1
            print("The player " + self.Player_name + " bought a smithy")
            self.coins -= 4
            self.cards_to_buy -= 1
        return
    def buy_estate(self):
        if self.coins >= 2 and shop["estate"] > 0: # if the player has enough coins, he can buy an estate
            self.Hand.append(Card("Estate", 0, 1, 2, "Victory"))
            shop["estate"] -= 1
            print("The player " + self.Player_name + " bought an estate")
            self.coins -= 2
            self.cards_to_buy -= 1
            self.Victory_points += 1
        return

    def buy_card(self):
        print("The player " + self.Player_name + " has " + str(self.cards_to_buy) + " more cards to buy")
        if self.coins >= 8 and shop["province"] > 0: # if the player has enough coins, he can buy a province
            self.buy_province()
        elif self.coins >= 6 and shop["gold"] > 0: # if the player has enough coins, he can buy a gold
            self.buy_treasure()
        elif self.coins >= 5 and shop["duchy"] > 0: # if the player has enough coins, he can buy a duchy
            self.buy_duchy()
        elif self.coins >= 4 and shop["smithy"] > 0: # if the player has enough coins, he can buy a smithy
            self.buy_smithy()
        elif self.coins >= 3 and shop["silver"] > 0: # if the player has enough coins, he can buy an estate
            self.buy_treasure()
        elif self.coins >= 2 and shop["estate"] > 0: # if the player has enough coins, he can buy an estate
            self.buy_estate()
        elif self.coins >= 0 and shop["copper"] > 0: # if the player no money, he can buy a copper
            self.buy_treasure()

    def end_turn(self):
        while len(self.Hand) > 0:
            self.Discard_p.append(self.Hand.pop(0))
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.action = 1
        self.coins = 0
        return
    
shop = { # name, amount after divide for 2 players
    "copper": 46,
    "silver": 40,
    "gold": 30,
    "estate": 8,
    "duchy": 8,
    "province": 8,    
    "smithy": 10,
}

def game_over():
    print("The game is over")
    if Aviv.Victory_points > Moshe.Victory_points:
        print("Aviv won the game")
    elif Aviv.Victory_points < Moshe.Victory_points:
        print("Moshe won the game")
    else:
        print("The game is a draw")
    print("--------------------------------")
    print("Aviv has " + str(Aviv.Victory_points) + " victory points")
    Aviv.print_dack()
    print("--------------------------------")
    print("Moshe has " + str(Moshe.Victory_points) + " victory points")
    Moshe.print_dack()

def empty_paket_in_shop():
    count = 0
    for name, amount in shop.items():
        if amount == 0:
            count += 1
    return count

def turn(player: Player):  # the turn of the player, #
    while player.cards_to_draw > 0:
        player.draw_card()
        player.play_card(player.Hand[-1])
    while player.cards_to_buy > 0:
        player.buy_card()
    player.end_turn()
    


    

Aviv = Player ("Aviv")
Moshe = Player ("Moshe")
Aviv.shuffle_discard_into_drow()
Moshe.shuffle_discard_into_drow()
print(Aviv.Drow_p)
print(Moshe.Drow_p)
for card in Aviv.Drow_p:
    print(card.name)
print("--------------------------------")
for card in Moshe.Drow_p:
    print(card.name)
print("--------------------------------")

Aviv_turn = True # Aviv's start
# Moshe_turn = False # Moshe's second start 

victory_points_to_win = 60
while True:
    if empty_paket_in_shop() >= 3:
        print("3 packet in shop is empty")
        break
    if Aviv_turn == True:
        turn(Aviv)
        Aviv_turn = False
        print("Aviv's turn is over Aviv have " + str(Aviv.Victory_points) + " victory points")
        if Aviv.Victory_points >= victory_points_to_win:
            break
    else:
        turn(Moshe)
        print("Moshe's turn is over Moshe have " + str(Moshe.Victory_points) + " victory points")
        Aviv_turn = True
        if Moshe.Victory_points >= victory_points_to_win:
            break
game_over()

        
        