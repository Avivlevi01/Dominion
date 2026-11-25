from cards import Card, CardName, CardType, push_card_to_trash, remove_card_from_shop
from strategy import Strategy
import random

class Player:
    def __init__(self, player_name: str, strategy: Strategy):
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
        self.strategy = strategy

    def __repr__(self) -> str:
        return f"{self.player_name} has {self.victory_points} victory points and {self.hand} cards in his hand and {self.discard_p} cards in his discard pile and {self.drow_p} cards in his draw pile"
    
            
    def reset_player(self):
        self.drow_p = []
        self.discard_p = [Card.create(CardName.COPPER) for _ in range(7)] + [Card.create(CardName.ESTATE) for _ in range(3)]
        self.hand = []
        self.victory_points = 3
        self.cards_to_draw = 5
        self.cards_to_buy = 1
        self.coins = 0
        self.action = 1
        self.cards_played = []

    
    def shuffle_discard_into_drow(self) -> None:
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
            chosen_card = self.strategy.choose_action_card_to_play(self.hand)
            if chosen_card is not None:
                if chosen_card.name == CardName.REMODEL and len(self.hand) == 1: #sometimes "chosen_card" is remodel card and it the only card in the hand. for this case we finish the action cards play
                    break
                self.play_action_card(chosen_card) 
                self.play_action_cards()
                return
            else:
                break # if no card is found, the player lost his action cards

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

    

    def buy_cards(self):
        while self.cards_to_buy > 0:
            new_card_name = self.strategy.choose_name_of_card_to_buy(self.coins)
            if new_card_name is not None:
                self.buy_card_by_name(new_card_name)
            else:
                break # if no card is found, the player lost his cards to buy

    def buy_card_by_name(self, card_name: CardName): 
        new_card = Card.create(card_name)
        self.discard_p.append(new_card)
        remove_card_from_shop(card_name) 
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

    def enter_victory_points_to_your_dack(self, victory_points: int):
        self.victory_points += victory_points
        return

    def take_out_victory_points_from_your_dack(self, victory_points: int):
        self.victory_points -= victory_points
        return


    def play_remodel(self): 
            remodeled_card = None 
            new_card = None 
            money_to_buy_new_card = 0
            remodeled_card = self.strategy.choose_remodeled_card(self.hand)
            if remodeled_card is None:
                raise Exception(f"The player {self.player_name} try to play a Remodel card but he has no cards to remodel in his hand")
            money_to_buy_new_card = remodeled_card.cost + 2 # coins to buy the new card 
            if (remodeled_card.type == CardType.VICTORY):
                self.take_out_victory_points_from_your_dack(remodeled_card.victory_points)
            self.hand.remove(remodeled_card)
            push_card_to_trash(remodeled_card)
            new_card = self.strategy.choose_remodel_card(money_to_buy_new_card)
            self.discard_p.append(new_card)
            if (new_card.type == CardType.VICTORY):
                self.enter_victory_points_to_your_dack(new_card.victory_points)
            remove_card_from_shop(new_card.name)
            print(f"The player {self.player_name} remodeled a {remodeled_card.name} and bought a {new_card.name}")
            
            
            
            
            """ #TODO: add the card to the trash? or just leave it in the hand? add a feacher of minimum card or block the player from playing remodel card?
            if new_card is None:
                return None
            else:
                remove_card_from_shop(new_card.name)
                return new_card"""