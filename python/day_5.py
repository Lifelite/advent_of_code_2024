import os
from pathlib import Path


# Get input from saved text file in $CWD/input
input_path = Path(__file__).parent.parent / "input" / "day5.txt"
challenge_input = open(input_path).read()

challenge_input = challenge_input.split("\n\n")
order_markers = challenge_input[0].split("\n")
page_pairs = []

for order_marker in order_markers:
    page_pairs.append(order_marker.split("|"))

produce_page_list = []
for line in challenge_input[1].split("\n"):
    line = line.split(",")
    len(line) > 1 and produce_page_list.append(list(line))


def check_order_pairs(page_pair, page_list):
    found_pairs = []
    for pair in page_pair:
        if pair[0] in page_list and pair[1] in page_list:
            found_pairs.append(pair)
        else:
            continue
    return found_pairs

def check_pair_against_page_list(page_pair, page_list):
    first_page_index = page_list.index(page_pair[0])
    second_page_index = page_list.index(page_pair[1])
    if first_page_index < second_page_index:
        return True
    else:
        return False

def fix_page_list_with_pair(page_pair, bad_page_list):
    modified_page_list = bad_page_list.copy()
    first_value = modified_page_list.pop(bad_page_list.index(page_pair[0]))
    second_page_index = modified_page_list.index(page_pair[1])
    modified_page_list.insert(second_page_index, first_value)
    return modified_page_list

def check_page_list(page_pair, page_list):

    for pair in page_pair:
        if not check_pair_against_page_list(pair, page_list):
            return False
        else:
            continue
    return True

def page_order_processor(page_order_pairs:list[list[str]], page_list:list[list[str]]):
    correct_lists = []
    incorrect_lists = []
    for current_list in page_list:
        found_pairs = check_order_pairs(page_order_pairs, current_list)

        if check_page_list(found_pairs, current_list):
            correct_lists.append(current_list)

        else:
            incorrect_lists.append(current_list)

    return correct_lists, incorrect_lists

def count_middle_value(valid_lists:list[list[str]]) -> int:
    count = 0
    for current_list in valid_lists:
        list_length = len(current_list)
        if list_length % 2 == 0:
            raise Exception("Well I guess we need to add handling for this")
        else:
            middle_index = list_length // 2
            count += int(current_list[middle_index])
    return count

def fix_bad_lists(order_markers, bad_lists):
    fixed_lists = []
    for bad_list in bad_lists:
        found_markers = check_order_pairs(order_markers, bad_list)
        new_list = bad_list.copy()
        for marker in found_markers:
            if not check_pair_against_page_list(marker, new_list):
                new_list = fix_page_list_with_pair(marker, new_list)
            else:
                continue
        fixed_lists.append(new_list)
    # Run check again just in case, recursively
    properly_fixed_lists, incorrect_lists = page_order_processor(order_markers, fixed_lists)
    if len(incorrect_lists) > 0:
        refixed =  fix_bad_lists(order_markers, incorrect_lists)
        properly_fixed_lists += refixed

    return properly_fixed_lists

good_lists, bad_lists = page_order_processor(page_pairs, produce_page_list)
print(count_middle_value(good_lists))

fixed_lists = fix_bad_lists(page_pairs, bad_lists)
print(count_middle_value(fixed_lists))
