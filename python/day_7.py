import itertools
import operator
from copy import deepcopy
from itertools import accumulate

from utils.utils import get_input

def parse_today_input():
    c_input = get_input(day=7).splitlines()
    input_parsed = {}
    for line in c_input:
        e_index = line.find(":")
        e_key = line[:e_index]
        e_value = line[e_index + 2:].split(" ")
        e_value = list(map(int, e_value))
        input_parsed[e_key] = e_value
    return input_parsed

def multiply(num1, num2):
    return num1 * num2


def add(num1, num2):
    return num1 + num2

def concat(num1, num2):
    new_num =  int(str(num1) + str(num2))
    return new_num

def check_value_list(val_set, possible_total):
    totals = []
    val_set_copy = deepcopy(val_set)
    first_num = val_set_copy.pop(0)
    for num in val_set_copy:
        if len(totals) == 0:
            totals.append(add(first_num, num))
            totals.append(multiply(first_num, num))
            totals.append(concat(first_num, num))
        else:
            new_totals = []
            for total in totals:
                new_totals.append(add(total, num))
                new_totals.append(multiply(total, num))
                new_totals.append(concat(total, num))
            totals = deepcopy(new_totals)
    if possible_total in totals:
        return possible_total
    else:
        return False


def calibration_finder(input_parsed):
    found_totals = []
    for key, value in input_parsed.items():
        possible_total = int(key)
        values = deepcopy(value)
        result = check_value_list(values, possible_total)
        if result:
            found_totals.append(possible_total)
    num_sum = sum(found_totals)
    return num_sum

if __name__ == '__main__':
    configured_input = parse_today_input()
    calculated_totals = calibration_finder(configured_input)
    print(calculated_totals)
