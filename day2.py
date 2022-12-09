from util.harness import run_day
import logging

from enum import Enum, auto
from abc import ABC

class Shape(Enum):
    ROCK     = auto()
    PAPER    = auto()
    SCISSORS = auto()

beats = { 
    Shape.ROCK: Shape.SCISSORS, 
    Shape.PAPER: Shape.ROCK,
    Shape.SCISSORS: Shape.PAPER
}

loses = {
    Shape.SCISSORS: Shape.ROCK, 
    Shape.ROCK: Shape.PAPER, 
    Shape.PAPER: Shape.SCISSORS
}


def compare_shapes(s1, s2):
    if s1 == s2:
        return 0
    if beats[s2] == s1:
        return 1
    else:
        return -1

shape_scores = {
    Shape.ROCK: 1,
    Shape.PAPER: 2,
    Shape.SCISSORS: 3
}

them_to_shape = { 
    "A": Shape.ROCK, 
    "B": Shape.PAPER, 
    "C": Shape.SCISSORS, 
}

us_to_shape = { 
    "X": Shape.ROCK, 
    "Y": Shape.PAPER, 
    "Z": Shape.SCISSORS, 
}

def score_round(them, us):
    round_score = 0
    result = compare_shapes(them, us) 
    if result == 0: # draw
        round_score += 3
    elif result > 0: # win
        round_score += 6
    round_score += shape_scores[us]
    return round_score


def part1(ls):
    score = 0
    for l in ls:
        shapes = l.split()
        them = them_to_shape[shapes[0]]
        us = us_to_shape[shapes[1]]

        round_score = score_round(them, us)
        
        # print("them: {}, us: {}, result: {}, score: {}".format(them, us, result, round_score))
        score += round_score

    return score


def part2(ls):
    score = 0
    for l in ls:
        shapes = l.split()
        them = them_to_shape[shapes[0]]

        desired_result = shapes[1]

        us = None
        if desired_result == "X":
            us = loses[them]
        elif desired_result == "Y":
            us = them
        elif desired_result == "Z":
            us = beats[them]


        round_score = score_round(them, us)
        
        print("them: {}, us: {}, result: {}, score: {}".format(them, us, result, round_score))
        score += round_score

    return score


if __name__ == "__main__":
    run_day(2, part1, part2)
