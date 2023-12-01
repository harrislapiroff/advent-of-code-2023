#!/usr/bin/env python3
import re
import itertools

DIGITS = list(itertools.chain(
    enumerate([
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
    ]),
    enumerate([
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ])
))

DIGIT_RE = '|'.join([label for idx, label in DIGITS])

f = open('1.txt', 'r')
lines = f.readlines()

def line_to_number(line: str) -> int:
    # Find the first number that matches any of the written out digits or numerals in our
    # DIGITS regex and then convert it to an int
    first_number = re.search(DIGIT_RE, line)
    first_int = (int_ for int_, str_ in DIGITS if str_ == first_number[0]).__next__()
    # To find the last number let's reverse both the string and the regex since regexes
    # don't support right-to-left matching and we can't guarantee the last match won't
    # overlap with a different match (and therefore be excluded)
    last_number = re.search(DIGIT_RE[::-1], line[::-1])
    last_int = (int_ for int_, str_ in DIGITS if str_ == last_number[0][::-1]).__next__()
    # Return an int of the two digits concatenated
    return int(str(first_int) + str(last_int))

# Sum the corresponding numbers for all lines
answer = sum(map(line_to_number, lines))

print(answer)