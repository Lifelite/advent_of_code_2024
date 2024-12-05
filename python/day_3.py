from pathlib import Path
import re

input_path = Path(__file__).parent.parent / "input" / "day3.txt"
challenge_input = open(input_path).readlines()

def find_mul_function_results(file_input):
    full_value = 0
    for line in file_input:
        returns = re.findall("mul\([0-9]*,[0-9]*\)", line)

        for item in returns:
            item = item[4:-1:1]
            numbers = item.split(",")
            full_value += int(numbers[0]) * int(numbers[1])

    return full_value


answer = find_mul_function_results(challenge_input)
print(answer)


def find_mul_function_results_2(file_input):
    full_value = 0
    current_flag = True

    for line in file_input:
        returns = re.findall("mul\([0-9]*,[0-9]*\)|do\(\)|don't\(\)", line)

        for item in returns:
            if item == "do()":
                current_flag = True
                continue
            if item == "don't()":
                current_flag = False
                continue
            if current_flag:
                item = item[4:-1:1]
                numbers = item.split(",")
                full_value += int(numbers[0]) * int(numbers[1])


    return full_value

answer2 = find_mul_function_results_2(challenge_input)
print(answer2)
