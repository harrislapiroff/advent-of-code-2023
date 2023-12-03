#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List
from pprint import pprint


CONSTRAINTS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


@dataclass
class DrawColor:
    "The number of a single color drawn in a draw"
    color: str
    number: int


@dataclass
class Draw:
    "All the different colors drawn in a single draw"
    draw_colors: List[DrawColor]


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

def game_meets_constraint(game: Game, constraint: dict) -> bool:
    """
    Check if a game is possible given a constraint on how many total cubes of
    each color are in the bag

    Constraints should take the form:

    {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    """

    for draw in game.draws:
        for draw_color in draw.draw_colors:
            if draw_color.number > constraint[draw_color.color]:
                return False

    return True


f = open('2.txt', 'r')
lines = f.readlines()
games = list(map(parse_game, lines))
passing_games = list(filter(lambda g: game_meets_constraint(g, CONSTRAINTS), games))
print(sum(map(lambda g: g.id, passing_games)))
