from itertools import product
from pathlib import Path

input_path = Path(__file__).parent.parent / "input" /"day1.txt"
challenge_input = open(input_path).read()

def input_parser(data):
    list_1 = []
    list_2 = []
    data = data.split("\n")

    # Added to remove new line IDE automatically adds to the bottom of files
    data.pop(-1)

    for line in data:
        new_line = line.split("   ")

        list_1.append(new_line[0])
        list_2.append(new_line[1])
    return list_1, list_2

def find_distance(input_thing):
    list_1, list_2 = input_parser(input_thing)
    list_1.sort()
    list_2.sort()
    i = 0
    distance = 0
    while i < len(list_1):
        distance_between = int(list_1[i]) - int(list_2[i])
        distance += abs(distance_between)
        i += 1
    return distance


answer = find_distance(challenge_input)
print(answer)


def find_similarity(input_thing):
    list_1, list_2 = input_parser(input_thing)
    score = 0
    for value_1, value_2 in product(list_1, list_2):
        if value_1 == value_2:
            score += int(value_1)
    return score

answer_2 = find_similarity(challenge_input)
print(answer_2)
