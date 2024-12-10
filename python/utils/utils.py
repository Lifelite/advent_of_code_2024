from pathlib import Path


def get_input(day:int):
    input_path = Path(__file__).parent.parent.parent / "input" / f"day{day}.txt"
    return open(input_path).read()


