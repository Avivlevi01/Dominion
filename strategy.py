from cards import Card, shop, cards, CardName, CardType, push_to_trash, get_amount_of_card_in_shop, remove_card_from_shop
import random

def find_expensive_card_in_shop_by_coins(coins: int): # have a problem with this function, it returns the first card found and I order it to return the most expensive card becosuse the order is top to bottom
    expensive_card = None
    for card_name, amount in shop.items():
        if coins >= cards[card_name].cost and amount > 0:
            expensive_card = Card.create(card_name)
            break
    return expensive_card # if no card is found, return None


def choose_card_to_buy(coins: int):
    while coins > 0:
        if coins == 3 and get_amount_of_card_in_shop(CardName.VILLAGE) > 0 and get_amount_of_card_in_shop(CardName.SILVER) > 0: # if the player has enough coins, he can buy an estate
            name_of_random_card = random.choice([CardName.SILVER, CardName.VILLAGE])
            return name_of_random_card
        if coins == 4 and get_amount_of_card_in_shop(CardName.SMITHY) > 0 and get_amount_of_card_in_shop(CardName.REMODEL) > 0: # if the player has enough coins, he can buy an estate
            name_of_random_card = random.choice([CardName.SMITHY, CardName.REMODEL])
            return name_of_random_card
        expensive_card = find_expensive_card_in_shop_by_coins(coins)
        return expensive_card.name
    return None

def choose_action_card_to_play (discard_p: list[Card]): 
    for card in discard_p:
        if card.name == CardName.VILLAGE:
            return card
    for card in discard_p:
        if card.name == CardName.REMODEL or card.name == CardName.SMITHY:
            return card
    return None

def play_remodel_and_return_remodel_card(hand: list[Card]):
    remodeled_card = None # the card to remodel
    new_card = None # the card to buy
    money_to_buy_new_card = 0

    for card in hand:
        if remodeled_card is None or card.cost < remodeled_card.cost:
            remodeled_card = card

    money_to_buy_new_card = remodeled_card.cost + 2 # 2 coins to buy the new card 
    hand.remove(remodeled_card)
    push_to_trash(remodeled_card)
    new_card = find_expensive_card_in_shop_by_coins(money_to_buy_new_card)
    if new_card is None:
        return None # TODO: add the card to the trash? or just leave it in the hand?
    else:
        remove_card_from_shop(new_card.name)
        return new_card


    