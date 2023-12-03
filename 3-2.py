#!/usr/bin/env python3

import re

from dataclasses import dataclass, field
from itertools import product, chain
from typing import List, Tuple, Any


@dataclass
class Number:
    """
    Representation of a number in a grid

    Attributes:
        row: The row of the number in the grid
        col: The *start* column of the number. It may span multiple columns
    """
    row: int
    col: int
    value: int
    grid: List[str] = field(repr=False)

    def __len__(self):
        return len(str(self.value))

    def cells(self) -> List[Tuple[int, int]]:
        "List the cell coordinates (x, y) that the number occupies"
        return [(self.row, x) for x in range(self.col, self.col + len(self))]

    def adjacent_cells(self) -> List[Tuple[int, int]]:
        "List the cell coordinates (x, y) that are adjacent to the number"
        row_range = range(
            max(self.row - 1, 0),
            min(self.row + 2, len(self.grid))
        )
        col_range = range(
            max(self.col - 1, 0),
            min(self.col + len(self) + 1, len(self.grid[0]))
        )
        return [(x, y) for x, y in product(row_range, col_range) if (x, y) not in self.cells()]


def find_numbers_on_row(line: str, row_idx: int, grid: List[str]) -> List[Number]:
    matches = re.finditer(r'\d+', line)
    return [Number(row_idx, match.start(), int(match[0]), grid) for match in matches]


def find_asterisks_on_row(line: str) -> List[int]:
    "Return a list of indexes where asterisks are found on a row"
    return [idx for idx, char in enumerate(line) if char == '*']


def gear_ratio_for_asterisk(asterisk: Tuple[int, int], numbers: List[Number]) -> int:
    "Return the gear ratio for a given asterisk or none if it is not adjacent to two numbers"
    # Find the numbers that are adjacent to the asterisk
    adjacent_numbers = [n for n in numbers if asterisk in n.adjacent_cells()]
    if (len(adjacent_numbers) == 2):
        return adjacent_numbers[0].value * adjacent_numbers[1].value
    return None


f = open('3.txt', 'r')
lines = [l.strip() for l in f.readlines()]
# Create Number objects for every number we find
numbers = list(chain(*[find_numbers_on_row(line, idx, lines) for idx, line in enumerate(lines)]))
# Find (x, y) coordinates of all asterisks
asterisks = list(chain(*[[(row, col) for col in find_asterisks_on_row(line)] for row, line in enumerate(lines)]))

print(sum([gr for asterisk in asterisks if (gr := gear_ratio_for_asterisk(asterisk, numbers)) is not None]))
