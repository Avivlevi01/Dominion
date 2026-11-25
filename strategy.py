import random
from cards import Card, shop, cards, CardName

class Strategy:
    def __init__(self):
        self.name = "Strategy"

    def affordable_card_names(self, coins: int) -> list[CardName]:
        return [
            name for name, amount in shop.items()
            if amount > 0 and cards[name].cost <= coins
        ]

    def choose_name_of_card_to_buy(self, coins: int) -> CardName | None:
        affordable = self.affordable_card_names(coins)
        if not affordable:
            return None
        return random.choice(affordable)

    def choose_action_card_to_play (self, hand: list[Card]): 
        for card in hand:
            if card.name == CardName.VILLAGE:
                return card
        if len(hand) == 1 and hand[0].name == CardName.REMODEL:
            return None
        for card in hand:
            if card.name == CardName.REMODEL or card.name == CardName.SMITHY:
                return card
        return None


    def choose_remodeled_card(self, hand: list[Card]) -> Card:
        remodeled_card = None
        for card in hand:
            if remodeled_card is None or card.cost < remodeled_card.cost:
                remodeled_card = card
        if remodeled_card is None:
            raise Exception(f"The player try to remodel a card but he has no cards to remodel in his hand")
        return remodeled_card

    def choose_remodel_card(self, money_to_buy_new_card: int) -> Card:
        affordable = self.affordable_card_names(money_to_buy_new_card)
        if not affordable:
            raise Exception(f"The player try to buy a new card but he has no cards in the shop")
        return Card.create(random.choice(affordable))

    