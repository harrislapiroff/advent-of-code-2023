#!/usr/bin/env python3

import re

from dataclasses import dataclass
from typing import List

CARD_RE = r'Card\s+(\d+): ([\d ]+) \| ([\d ]+)'

@dataclass
class Card:
    id: int
    winning_numbers: List[int]
    player_numbers: List[int]
    multiplier: int = 1

    def matches(self):
        return set(self.winning_numbers) & set(self.player_numbers)

    def increment(self, amt = 1):
        self.multiplier += amt


def parse_card(line: str) -> Card:
    """
    Parse a string that looks like:

    Card 1: 1 2 3 4 5 | 1 2 3 4 5

    into a Card object.
    """
    id_str, winning_numbers_str, player_numbers_str = re.match(CARD_RE, line).groups()
    winning_numbers = [int(x) for x in winning_numbers_str.split(' ') if x != '']
    player_numbers = [int(x) for x in player_numbers_str.split(' ') if x != '']
    return Card(int(id_str), winning_numbers, player_numbers)


f = open('4.txt', 'r')
cards = [parse_card(line.strip()) for line in f.readlines()]
for card in cards:
    matches = card.matches()
    copy_start = card.id  # Card IDs are 1-indexed
    copy_end = min(card.id + len(matches), len(cards))
    cards_to_copy = cards[copy_start:copy_end]
    for card_to_copy in cards_to_copy:
        card_to_copy.increment(card.multiplier)


print(sum(card.multiplier for card in cards))
