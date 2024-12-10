import dataclasses
from copy import deepcopy
from itertools import combinations
from typing import NamedTuple, List

from utils.utils import get_input

challenge_input = get_input(8)


class Coordinate(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class Antenna:
    MAP_Y_MIN = 0
    MAP_Y_MAX = 49
    MAP_X_MIN = 0
    MAP_X_MAX = 49
    _locations: List[Coordinate] = dataclasses.field(default_factory=list)
    _antinodes: List[Coordinate] = dataclasses.field(default_factory=list)

    def _off_the_map_checker(self, coordinate: Coordinate) -> bool:
        return not (
                (coordinate.y < self.MAP_Y_MIN or coordinate.y > self.MAP_Y_MAX)
                or
                (coordinate.x < self.MAP_X_MIN or coordinate.x > self.MAP_X_MAX)
        )

    @property
    def antinodes(self):
        return self._antinodes

    @antinodes.setter
    def antinodes(self, value):
        self._antinodes = value

    def add_antinode(self, antinode: Coordinate):
        antinodes_copy = self._antinodes.copy()
        antinodes_copy.append(antinode)
        self.antinodes = antinodes_copy

    @property
    def locations(self):
        return self._locations

    def antionide_calc(self, antinode, diff):
        new_node = Coordinate(
            antinode.x + diff.x,
            antinode.y + diff.y,
        )
        if self._off_the_map_checker(new_node):

            self.add_antinode(new_node)
            # Remove this line to do part 1
            self.antionide_calc(new_node, diff)

    @locations.setter
    def locations(self, value: List[Coordinate]):
        self._locations = value
        if len(self.locations) > 1:
            for point_1, point_2 in combinations(self._locations, 2):
                diff_x = point_1.x - point_2.x
                diff_y = point_1.y - point_2.y
                add_x = point_2.x - point_1.x
                add_y = point_2.y - point_1.y

                # redo this line to do part 1.  We don't want to add antenna points by default for that.

                self.antionide_calc(point_1, Coordinate(diff_x, diff_y))
                self.antionide_calc(point_1, Coordinate(add_x, add_y))
                self.antionide_calc(point_2, Coordinate(add_x, add_y))
                self.antionide_calc(point_2, Coordinate(diff_x, diff_y))

    def add_antenna(self, coordinate: Coordinate):
        new_location_list = deepcopy(self._locations)
        new_location_list.append(coordinate)
        self.locations = new_location_list
        return self


def parse_input(c_input):
    i_list = c_input.splitlines()
    antenna_map: {Antenna} = {}
    new_map = []
    for index, line in enumerate(i_list):

        new_line = []
        for c_index, ch in enumerate(line):
            coordinate = Coordinate(c_index, index)
            new_line.append(ch)
            if ch == ".":
                continue
            if antenna_map.get(ch, False):
                antenna_map[ch].add_antenna(coordinate)
            else:
                antenna_map[ch] = Antenna().add_antenna(Coordinate(c_index, index))

        new_map.append(new_line)

    unique_coordinates = []
    all_coordinates = set()
    counter = 0
    maps = {}
    for key, antenna in antenna_map.items():
        maps[key] = deepcopy(new_map)
        for antinode in antenna.antinodes:
            maps[key][antinode.y][antinode.x] = "q"
            if antinode not in unique_coordinates:
                unique_coordinates.append(antinode)
            all_coordinates.add(antinode)

    return unique_coordinates


if __name__ == "__main__":
    a_map = parse_input(challenge_input)
    print(len(a_map))
