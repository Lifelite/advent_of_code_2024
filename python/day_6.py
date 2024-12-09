import concurrent
import copy
import itertools
from concurrent import futures
from concurrent.futures import wait

from utils.utils import get_input

challenge_input = get_input(6)

input_rows = challenge_input.split("\n")
map_matrix = []

for row in input_rows:
    if len(row) > 0:
        map_matrix.append(list(row))


class Guard:
    # Coordinates look odd because formatted it will be list[y-axis][x-axis]

    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]

    def __init__(self, current_position, current_direction):
        self._current_position = current_position
        self.current_direction = Guard._check_direction(current_direction)

    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, value):
        if (
                not value
                or not 0 <= value[0] < 130
                or not 0 <= value[1] < 130
        ):
            self._current_position = None
        else:
            self._current_position = value

    @staticmethod
    def _check_direction(direction):
        match direction:
            case "^":
                return Guard.UP
            case "v":
                return Guard.DOWN
            case "<":
                return Guard.LEFT
            case ">":
                return Guard.RIGHT

    @staticmethod
    def _add_values(val_1, val_2):
        new_value = [val_1[0] + val_2[0], val_1[1] + val_2[1]]
        return new_value

    def move_up(self):
        self.current_position = self._add_values(self.UP, self.current_position)

    def move_down(self):
        self.current_position = self._add_values(self.DOWN, self.current_position)

    def move_left(self):
        self.current_position = self._add_values(self.LEFT, self.current_position)

    def move_right(self):
        self.current_position = self._add_values(self.RIGHT, self.current_position)

    def turn_right(self):
        match self.current_direction:
            case Guard.UP:
                self.current_direction = Guard.RIGHT
            case Guard.DOWN:
                self.current_direction = Guard.LEFT
            case Guard.LEFT:
                self.current_direction = Guard.UP
            case Guard.RIGHT:
                self.current_direction = Guard.DOWN

    def move(self):
        match self.current_direction:
            case Guard.UP:
                self.move_up()
            case Guard.DOWN:
                self.move_down()
            case Guard.LEFT:
                self.move_left()
            case Guard.RIGHT:
                self.move_right()

    def stepback(self):
        match self.current_direction:
            case Guard.UP:
                self.move_down()
            case Guard.DOWN:
                self.move_up()
            case Guard.LEFT:
                self.move_right()
            case Guard.RIGHT:
                self.move_left()


def map_guard_patrol(area_map):
    new_area_map = copy.deepcopy(area_map)
    # This is looping through to seek out the Guard
    current_position = list(
        [(ix, iy)
         for ix, x_row in enumerate(new_area_map)
         for iy, i in enumerate(x_row)
         if i == "^"][0]
    )
    guard = Guard(current_position, "^")
    count = 0
    latest_count = 0
    identical_count = 0
    while guard.current_position is not None:
        new_area_map[guard.current_position[0]][guard.current_position[1]] = "X"
        guard.move()
        if guard.current_position and new_area_map[guard.current_position[0]][guard.current_position[1]] == "O":
            count +=1
            if count > 4:
                guard.current_position = None
                return count_patrolled_spaces(new_area_map)

        if (
                guard.current_position
                and
                (
                        new_area_map[guard.current_position[0]][guard.current_position[1]] == "#"
                        or new_area_map[guard.current_position[0]][guard.current_position[1]] == "O"
                )
        ):
            guard.stepback()
            guard.turn_right()

            # Logging turns for loop protection
            if count > 0:
                new_count = count_patrolled_spaces(new_area_map)
                if new_count == latest_count:
                    identical_count += 1
                else:
                    latest_count = new_count
                    identical_count = 0

                if identical_count > 5:
                    guard.current_position = False
                    return new_count
            continue

    return new_area_map

def count_patrolled_spaces(area_map):
    count = 0
    for item in itertools.chain.from_iterable(area_map):
        if item == "X":
            count += 1
    return count

def get_mapped_coordinates(area_map):
    return [
        [ix, iy]
        for ix, x_row in enumerate(area_map)
        for iy, i in enumerate(area_map[ix])
        if i == "X"
    ]
def check_loops(cor_x, cor_y, area_map):
    new_map = copy.deepcopy(area_map)
    new_map[cor_x][cor_y] = "O" if new_map[cor_x][cor_y] != "^" else "^"
    check = map_guard_patrol(new_map)

    # returning steps for debugging purposes
    if isinstance(check, int):
        return check


def check_possible_loops(marked_area_map, area_map):
    results = []
    non_loops = 0
    possible_loop_obstacles_coordinates = get_mapped_coordinates(marked_area_map)
    with concurrent.futures.ProcessPoolExecutor(max_workers=25) as executor:
        for coords_x, coords_y in possible_loop_obstacles_coordinates:
            loop_possibility = executor.submit(check_loops, coords_x, coords_y, area_map)
            results.append(loop_possibility)
    wait(results)
    loop_possiblities = []
    for loop_possibility in results:
        if loop_possibility.result():
            loop_possiblities.append(loop_possibility.result())
        else:
            non_loops += 1

    return loop_possiblities



if __name__ == "__main__":
    guard_map = map_guard_patrol(map_matrix)
    new_m = copy.deepcopy(map_matrix)
    new_m[115][83] = "O"
    test = map_guard_patrol(new_m)
    count = count_patrolled_spaces(guard_map)
    print(count)
    loops = check_possible_loops(guard_map, map_matrix)
    print(len(loops))
