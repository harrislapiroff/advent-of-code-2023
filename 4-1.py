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

    def matches(self):
        return set(self.winning_numbers) & set(self.player_numbers)


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
points = sum(
    2 ** (len(matches) - 1)
    for card in cards
    if (matches := card.matches())
)
print(points)
