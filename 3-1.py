#!/usr/bin/env python3

import re

from dataclasses import dataclass
from itertools import product, chain
from typing import List, Tuple, Any


SYMBOL_RE = re.compile(r'[^0-9^\.]')


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


def is_part_number(number: Number) -> bool:
    adjacent_cells = number.adjacent_cells()
    return any(SYMBOL_RE.match(number.grid[x][y]) is not None for x, y in adjacent_cells)


f = open('3.txt', 'r')
lines = [l.strip() for l in f.readlines()]
numbers = chain(*[find_numbers_on_row(line, idx, lines) for idx, line in enumerate(lines)])
part_numbers = [n for n in numbers if is_part_number(n)]
print(sum([pn.value for pn in part_numbers]))
