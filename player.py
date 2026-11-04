from game import Card, CardName, CardType, buy_from_shop, find_card_to_buy, push_to_trash, get_amount_of_card_in_shop, find_expensive_card_to_buy
import random

class Player:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.drow_p = []
        self.discard_p = [Card.create(CardName.COPPER) for _ in range(7)] + [Card.create(CardName.ESTATE) for _ in range(3)]
        self.hand = []
        self.victory_points = 3
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.coins = 0
        self.action = 1
        self.cards_played = []

    def __repr__(self) -> str:
        return f"{self.player_name} has {self.victory_points} victory points and {self.hand} cards in his hand and {self.discard_p} cards in his discard pile and {self.drow_p} cards in his draw pile"
    
    def shuffle_discard_into_drow(self):
        random.shuffle(self.discard_p)
        self.drow_p.extend(self.discard_p)
        self.discard_p = []
        print("shuffled discard into_drow")

    def print_dack(self):
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


    def play_action_cards(self):
        while self.action > 0 and self.count_action_cards_in_hand() > 0:
            for card in self.hand:
                if card.name == CardName.VILLAGE:
                    self.play_action_card(card)
                    self.play_action_cards()
                    return 
            for card in self.hand:
                if card.name == CardName.REMODEL:
                    self.play_action_card(card)
                    self.play_action_cards()
                    return 
            for card in self.hand:
                if card.name == CardName.SMITHY:
                    self.play_action_card(card)
                    self.play_action_cards()
                    return

    def play_treasure_cards(self):
        for card in list(self.hand):            
            if card.type == CardType.TREASURE:
                self.coins += card.coins
                self.cards_played.append(card)
                self.hand.remove(card)

    def play_action_card(self, card: Card):
        self.action -= 1
        if self.action < 0:
            raise Exception(f"The player {self.player_name} try to play an action card {card.name} but he has no actions")
        self.cards_played.append(card)
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
        elif card.name == CardName.REMODEL:
            self.play_remodel()
        return

    def play_remodel(self):
        remodeled_card = None # the card to remodel
        new_card = None # the card to buy
        money_to_buy_new_card = 0 # the money to buy the new card

        for card in self.hand:
            if remodeled_card is None or card.cost < remodeled_card.cost:
                remodeled_card = card

        money_to_buy_new_card = remodeled_card.cost + 2 # 2 coins to buy the new card
        push_to_trash(remodeled_card)
        self.hand.remove(remodeled_card)
        new_card = find_card_to_buy(money_to_buy_new_card)
        if new_card is None:
            print(f"The player {self.player_name} tried to buy a new card but no card is found the player lost is action card")
            self.hand.append(remodeled_card) #TODO: add the card to the trash? or just leave it in the hand?
            # push_to_trash(remodeled_card)
            return
        self.discard_p.append(new_card)
        print(f"The player {self.player_name} played a remodel and put a {remodeled_card.name} in the trush and put a {new_card.name} in his discard pile")
    

    def buy_cards(self):
        while self.cards_to_buy > 0:
            print(f"The player {self.player_name} has {self.cards_to_buy} more cards to buy")
            if self.coins == 3 and get_amount_of_card_in_shop(CardName.VILLAGE) > 0 and get_amount_of_card_in_shop(CardName.SILVER) > 0: # if the player has enough coins, he can buy an estate
                name_of_random_card = random.choice([CardName.SILVER, CardName.VILLAGE])
                self.buy_card(name_of_random_card)
                break
            if self.coins == 4 and get_amount_of_card_in_shop(CardName.SMITHY) > 0 and get_amount_of_card_in_shop(CardName.REMODEL) > 0: # if the player has enough coins, he can buy an estate
                name_of_random_card = random.choice([CardName.SMITHY, CardName.REMODEL])
                self.buy_card(name_of_random_card)
                break

            expensive_card = find_expensive_card_to_buy(self.coins)
            if expensive_card is not None:
                self.buy_card(expensive_card.name)
                break
            '''
            for card_name, amount in shop.items():
                if self.coins >= card_name.cost and amount > 0:
                    self.buy_card(card_name)
                    break
            '''

    def buy_card(self, card_name: CardName):
        new_card = Card.create(card_name)
        self.discard_p.append(new_card)
        buy_from_shop(card_name) 
        print(f"The player {self.player_name} bought a {card_name}")
        if new_card.type == CardType.VICTORY:
            self.victory_points += new_card.victory_points 
        elif new_card.type == CardType.TREASURE:
            self.coins += new_card.coins
        self.cards_to_buy -= 1
        return

    def end_turn(self):
        while len(self.hand) > 0:
            self.discard_p.append(self.hand.pop(0))
        while len(self.cards_played) > 0:
            self.discard_p.append(self.cards_played.pop(0))
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.action = 1
        self.coins = 0
        return