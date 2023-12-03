#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List
from pprint import pprint

COLORS = ['red', 'green', 'blue']


@dataclass
class DrawColor:
    "The number of a single color drawn in a draw"
    color: str
    number: int


@dataclass
class Draw:
    "All the different colors drawn in a single draw"
    draw_colors: List[DrawColor]

    def color(self, color: str) -> int:
        matching_colors = list(filter(lambda d, color=color: d.color == color, self.draw_colors))
        if len(matching_colors) == 0:
            return DrawColor(color=color, number=0)
        return matching_colors[0]


@dataclass
class Game:
    "Multiple draws from a bag of colored cubes"
    id: int
    draws: List[Draw]


def parse_draw_color(draw_color_str: str) -> DrawColor:
    """
    Parse a string that looks like:

    3 blue

    into a DrawColor object.
    """

    number, color = draw_color_str.split(' ')
    return DrawColor(color=color.strip(), number=int(number))


def parse_draw(draw_str: str) -> Draw:
    """
    Parse a string that looks like:

    3 blue, 4 red

    into a Draw object.
    """

    return Draw(draw_colors=list(map(parse_draw_color, draw_str.split(', '))))


def parse_game(game_str: str) -> Game:
    """
    Parse a string that looks like:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    into a Game object.
    """
    game_id_str, draws_str = game_str.split(': ')
    game_id = int(game_id_str.split(' ')[1])

    return Game(
        id=game_id,
        draws=list(map(parse_draw, draws_str.split('; ')))
    )


def minimum_cubes(game_: Game) -> int:
    """
    Find the minimum number of cubes that could have been in the bag
    for a given game.
    """

    minimums = {}
    for color in COLORS:
        minimums[color] = max(list(map(lambda g: g.color(color).number, game_.draws)))

    return minimums


def game_power(game: Game) -> int:
    """
    Find the power of a game, which is the product of the minimum number of
    cubes of each color that could have been in the bag
    """

    minimums = minimum_cubes(game)
    return minimums['red'] * minimums['green'] * minimums['blue']


f = open('2.txt', 'r')
lines = f.readlines()
games = list(map(parse_game, lines))
print(
    sum(
        map(
            game_power,
            games
        )
    )
)
