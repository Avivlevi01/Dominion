# Dominion

**Status: work in progress.** This is an ongoing learning project, not a finished game.

It is a small Dominion-like card game in Python. The point of the project is to practice the architecture of a game with several classes, shared state, and rules that get harder over time. The code runs a full game between two players. Some rules are still rough, and the known problems are listed below on purpose.

## What this project is for

A turn in this game changes several piles at once: the hand, the draw pile, the discard pile, the shop, and the trash. That is a useful place to practice:

- giving each module one job
- deciding which object owns each piece of state
- keeping the startup code free of game rules
- noticing when a new card no longer fits the current design

## Architecture

Five files run the game.

| File | Owns |
| --- | --- |
| `main.py` | Creating the two players and starting one game. |
| `game.py` | The turn loop and the check for the end of the game. |
| `cards.py` | Card descriptions, the shop, and the trash. |
| `player.py` | One player's deck, hand, coins, actions, and the steps of a turn. |
| `strategy.py` | Which card to buy, which action to play, and how Remodel picks a replacement. |

`main.py` does not contain the rules. It builds two `Player` objects and passes them to `start_game`. The starting cards sit in the discard pile. The first draw shuffles that pile into the draw pile, so `main.py` does not shuffle.

Imports stay in one direction. `cards.py` does not import the other game files. `strategy.py` and `player.py` use `cards.py`. `game.py` uses the shop from `cards.py` and the `Player` class from `player.py`. `player.py` does not import `game.py`, so the modules do not import each other in a circle.

The card data lives in one dictionary, `cards`. Each entry is one description: name, cost, type, coins, and victory points. `Card.create` copies that description into a new object for a deck. The shared description does not change when a player gains a card.

`shop` is a second dictionary in `cards.py`. Its keys are card names, and its values are how many copies are still available. The player does not own the shop. A normal buy calls `remove_card_from_shop` once, inside `buy_card`. Remodel lowers the shop once when it gains the replacement card.

A turn is a fixed sequence in `play_turn`: draw, play actions, play treasures, buy, then clean up.

`buy_cards` asks `choose_card_to_buy` for a card name and then buys that name. With 3 coins the choice is Silver or Village. With 4 coins the choice is Smithy or Remodel. Any other coin total uses the first card in the shop that the player can afford.

The end of the game prints the winner from the two player objects. The printed names are `player_name` on those objects.

## Run a game

From the project folder:

```powershell
python main.py
```

The program plays Aviv against Moshe and prints each turn. It stops when three piles in the shop are empty, then it prints who has more victory points.

## What is working now

- Card data, the shop, and the trash live in `cards.py`, away from the turn loop.
- Buy and action choices live in `strategy.py`. `Player` still carries out the chosen step.
- One normal purchase removes one copy from the shop.
- The game prints the winner's name from the player objects.
- A full game can run from `python main.py` through draws, actions, buys, and the end check.

## Known issues

These are real gaps in the current code.

- **"Most expensive" is not really calculated.** `find_expensive_card_in_shop_by_coins` stops at the first card the player can afford. The result depends on the order of the `shop` dictionary, not on a comparison of costs.
- **A buy with no legal card can crash.** `choose_card_to_buy` reads `.name` on the result of that search. When the result is `None`, Python raises `AttributeError`.
- **A failed Remodel puts `None` in the discard pile.** Remodel trashes the cheapest card in hand, then looks for a replacement. If none exists, the function returns `None`, and `play_action_card` appends that `None`.
- **Action effects are still a chain of name checks.** `choose_action_card_to_play` picks Village before Remodel or Smithy. `play_action_card` then branches on the card name. A new action card means another branch.
- **The end check is written for exactly two players.** The printed names come from the objects, and the parameters are still named for Aviv and Moshe.
- **Names are still draft names.** Examples: `drow_p`, `print_dack`, and `count_empty_paket_in_shop`.
- **There are no tests yet.** The game is checked by running it and reading the printed turn log.

## Roadmap

1. When no card can be bought, end the buy phase instead of reading `.name` on `None`.
2. Pick the card with the highest cost the player can afford, instead of trusting dictionary order.
3. On a failed Remodel, leave a real card outcome: trash the chosen card only when a replacement is gained, and never store `None` in a pile.
4. Let a new action card add its own behavior, instead of growing the `if card.name` chain.
5. Rename the draft names, then add a few tests around buying and the end of the game.
