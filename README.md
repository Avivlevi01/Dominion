# Dominion

**Status: work in progress.** This is an ongoing learning project, not a finished game.

It is a small Dominion-like card game in Python. The point of the project is to practice the architecture of a game with several classes, shared state, and rules that get harder over time. The code runs a full game between two players. Some rules are still rough, and the known problems are listed below on purpose.

## What this project is for

A turn in this game changes several piles at once: the hand, the draw pile, the discard pile, the shop, and the trash. That is a useful place to practice:

- giving each class one job
- deciding which object owns each piece of state
- keeping the startup code free of game rules
- noticing when a new card no longer fits the current design

## Architecture

Three files run the game.

| File | Owns |
| --- | --- |
| `main.py` | Creating the two players and starting one game. |
| `game.py` | Card descriptions, the shop, the trash, and the turn loop. |
| `player.py` | One player's deck, hand, coins, actions, and the steps of a turn. |

`main.py` does not contain the rules. It builds two `Player` objects and passes them to `start_game`.

Imports go in one direction. `player.py` uses the cards and the shop functions from `game.py`. `game.py` does not import `player.py`. That avoids a circular import. `from __future__ import annotations` lets `game.py` mention `Player` in type notes without loading `player.py`.

The card data lives in one dictionary, `cards`. Each entry is one description: name, cost, type, coins, and victory points. `Card.create` copies that description into a new object for a deck. The shared description does not change when a player gains a card.

`shop` is a second dictionary. Its keys are card names, and its values are how many copies are still available. The player does not own the shop. The game module does, and the player calls functions such as `get_amount_of_card_in_shop` and `buy_from_shop`.

A turn is a fixed sequence in `play_turn`: draw, play actions, play treasures, buy, then clean up.

## Run a game

From the project folder:

```powershell
python main.py
```

The program plays Aviv against Moshe and prints each turn. It stops when three piles in the shop are empty, then it prints who has more victory points.

## Known issues

These are real gaps in the current code.

- **A buy can remove two copies from the shop.** `find_card_to_buy` and `find_expensive_card_to_buy` already lower the shop count. `buy_card` then calls `buy_from_shop`, which lowers it again.
- **"Most expensive" is not really calculated.** `find_expensive_card_to_buy` stops at the first card the player can afford. The result depends on the order of the `shop` dictionary, not on a comparison of costs.
- **The ending knows two player names.** `check_game_over` prints "Aviv" and "Moshe" directly. The function already receives the two player objects, so the names should come from those objects.
- **Buying choices are inside `Player`.** Rules such as "with 3 coins, choose Silver or Village" live in `buy_cards`. The player class currently both stores the deck and decides the strategy.
- **Action cards are a chain of name checks.** `play_action_cards` looks for Village, then Remodel, then Smithy. A new action card means another branch in that method.
- **Names are still draft names.** Examples: `drow_p`, `print_dack`, and `count_empty_paket_in_shop`.
- **There are no tests yet.** The game is checked by running it and reading the printed turn log.
- **`src/game00.py` is an old copy.** It is not part of the program that `main.py` runs.

## Roadmap

1. Make one purchase change the shop once.
2. Pick the card with the highest cost the player can afford, instead of trusting dictionary order.
3. Print the winner from the player objects, for any player names.
4. Move the buying choices out of `Player`, so a new strategy does not require editing the deck class.
5. Let a new action card add its own behavior, instead of growing the `if card.name` chain.
6. Rename the draft names, then add a few tests around buying and the end of the game.
