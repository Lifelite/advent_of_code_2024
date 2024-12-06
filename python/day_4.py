import dataclasses
from pathlib import Path

input_path = Path(__file__).parent.parent / "input" / "day4.txt"
challenge_input = open(input_path).read()

@dataclasses.dataclass
class Directions:
    UP = [0, -1]
    DOWN = [0, 1]
    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UPLEFT = [-1, -1]
    DOWNRIGHT = [1, 1]
    DOWNLEFT = [-1, 1]
    UPRIGHT = [1, -1]

def add_values(val_1, val_2):
    new_value =  [val_1[0] + val_2[0], val_1[1] + val_2[1]]
    return new_value

def check_word(word, string):
    if word.find(string) != -1:
        return True
    return False

def letter_searcher(target, position, matrix, direction):
    current_check = matrix[position[0]][position[1]]
    new_coordinates = position.copy()

    while True:
        new_coordinates = add_values(new_coordinates, direction)
        if not 0 <= new_coordinates[0] < len(matrix) or not 0 <= new_coordinates[1] < len(matrix[position[0]]) :
            return False
        current_check += matrix[new_coordinates[0]][new_coordinates[1]]
        if current_check == target:
            return True
        elif check_word(target, current_check):
            continue
        else:
            return False


def find_words(c_input, target):
    lines = c_input.split("\n")
    input_list = []
    directions = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [1,-1]]
    counter = 0
    for line in lines:
        input_list.append(list(line))

    # exists to remove new line automatically inserted by IDE
    input_list.pop(-1)
    for index, row in enumerate(input_list):
        for c_index, column in enumerate(row):
            if column == target[0]:
                for direction in directions:
                    if letter_searcher(target, [index, c_index], input_list, direction):
                        counter += 1
                    else:
                        continue
    return counter





value = find_words(challenge_input, "SAM")
print(value)


#part 2

def x_finder(target, position, matrix):
    cross_1 = [[1,1],[-1,-1]]
    cross_2 = [[-1,1],[1,-1]]
    coor_1 = add_values(cross_1[0], position)
    coor_2 = add_values(cross_1[1], position)
    coor_3 = add_values(cross_2[0], position)
    coor_4 = add_values(cross_2[1], position)

    # I just thought this was a hilariously ugly way to avoid IndexErrors
    if (
            not 0 <= coor_1[0] < len(matrix)
            or not 0 <= coor_1[1] < len(matrix[position[0]])
            or not 0 <= coor_2[0] < len(matrix[position[0]])
            or not 0 <= coor_2[1] < len(matrix[position[0]])
            or not 0 <= coor_3[0] < len(matrix[position[0]])
            or not 0 <= coor_3[1] < len(matrix[position[0]])
            or not 0 <= coor_4[0] < len(matrix[position[0]])
            or not 0 <= coor_4[1] < len(matrix[position[0]])
    ) :
        return False

    word1 = matrix[coor_1[0]][coor_1[1]] + matrix[position[0]][position[1]] + matrix[coor_2[0]][coor_2[1]]
    word2 = matrix[coor_3[0]][coor_3[1]] + matrix[position[0]][position[1]] + matrix[coor_4[0]][coor_4[1]]

    if (
        (target == word1 or target[::-1] == word1)
        and
        (target == word2 or target[::-1] == word2)
    ):
        return True
    else:
        return False


def find_words(c_input, target):
    lines = c_input.split("\n")
    input_list = []
    counter = 0
    for line in lines:
        input_list.append(list(line))

    # exists to remove new line automatically inserted by IDE
    input_list.pop(-1)
    for index, row in enumerate(input_list):
        for c_index, column in enumerate(row):
            if column == target[1] and x_finder(target, [index, c_index], input_list):
                counter += 1
    return counter

value = find_words(challenge_input, "SAM")
print(value)
