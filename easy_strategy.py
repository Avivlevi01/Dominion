import random
from cards import Card
from strategy import Strategy
class EasyStrategy(Strategy):
    
    def __init__(self):
        self.name = "EasyStrategy"

    def choose_remodeled_card(self, hand: list[Card]) -> Card:
        if len(hand) == 0:
            raise Exception("The player try to remodel a card but he has no cards to remodel in his hand")
        return random.choice(hand)