import random
from cards import Card, CardName, cards, get_amount_of_card_in_shop
from strategy import Strategy
class HardStrategy(Strategy):
    
    def __init__(self):
        self.name = "HardStrategy"

    def choose_random_card_with_max_cost(self, coins: int) -> CardName | None:
        if coins != 3 and coins != 4:
            return None
        cards_at_max_cost = []
        for card_name in cards:
            if cards[card_name].cost == coins and get_amount_of_card_in_shop(card_name) > 0:
                cards_at_max_cost.append(card_name)
        if len(cards_at_max_cost) == 0:
            return None
        return random.choice(cards_at_max_cost)

    def choose_name_of_card_to_buy(self, coins: int) -> CardName | None:
        if coins <= 0:
            return None
        affordable = self.affordable_card_names(coins)
        if not affordable:
            return None
        best_cost = max(cards[name].cost for name in affordable)
        tied = [name for name in affordable if cards[name].cost == best_cost]
        return random.choice(tied)

    def choose_remodeled_card(self, hand: list[Card]) -> Card:
        for card_name in [CardName.ESTATE, CardName.COPPER]:
            for card in hand:
                if card.name == card_name:
                    return card
        return super().choose_remodeled_card(hand)

    def choose_remodel_card(self, money_to_buy_new_card: int) -> Card:
        random_max_card = self.choose_random_card_with_max_cost(money_to_buy_new_card)
        if random_max_card is not None:
            return Card.create(random_max_card)
        if get_amount_of_card_in_shop(CardName.PROVINCE) > 0 and cards[CardName.PROVINCE].cost <= money_to_buy_new_card:
            return Card.create(CardName.PROVINCE)
        if get_amount_of_card_in_shop(CardName.GOLD) > 0 and cards[CardName.GOLD].cost <= money_to_buy_new_card:
            return Card.create(CardName.GOLD)
        action_names = []
        if get_amount_of_card_in_shop(CardName.SMITHY) > 0 and cards[CardName.SMITHY].cost <= money_to_buy_new_card:
            action_names.append(CardName.SMITHY)
        if get_amount_of_card_in_shop(CardName.REMODEL) > 0 and cards[CardName.REMODEL].cost <= money_to_buy_new_card:
            action_names.append(CardName.REMODEL)
        if len(action_names) > 0:
            return Card.create(random.choice(action_names))
        return super().choose_remodel_card(money_to_buy_new_card)