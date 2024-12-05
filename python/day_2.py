from pathlib import Path



input_path = Path(__file__).parent.parent / "input" /"day2.txt"
challenge_input = open(input_path).read()

def check_report(line_array):
    previous = None
    upward = None

    for number in line_array:
        value = int(number)
        if not previous:
            previous = value
            continue

        if previous == value:
            return False

        if upward is None and value > previous:
            upward = True

        if upward is None and value < previous:
            upward = False

        result = value - previous
        if upward:
            if 0 < result < 4:
                previous = value
                continue
            else:
                return False
        else:
            result = previous - value
            if 0 < result < 4:
                previous = value
                continue
            else:
                return False
    return "Safe"

def process_reports(raw_input:str):
    safe_reports = []
    for line in raw_input.splitlines():
        line_array = line.split(" ")
        check = check_report(line_array)
        if check:
            safe_reports.append(line_array)
            continue
        else:

            i = 0
            while i < len(line_array):
                mod_line_array = line_array.copy()
                mod_line_array.pop(i)
                check = check_report(mod_line_array)
                if check:
                    safe_reports.append(mod_line_array)
                    i+=1
                    break
                else:
                    i+=1
                    continue

    return safe_reports






array = process_reports(challenge_input)


print(array)
print(len(array))
