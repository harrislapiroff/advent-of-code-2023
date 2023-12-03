#!/usr/bin/env python3

f = open('1.txt', 'r')
lines = f.readlines()

def line_to_number(line: str) -> int:
    ns = list(filter(lambda c: c in '0123456789', line))
    return int(ns[0] + ns[-1])

answer = sum(map(line_to_number, lines))

print(answer)
