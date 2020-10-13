from enum import Enum
from typing import Optional
import copy


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def add_2d(first: (int, int), second: (int, int)):
    return first[0] + second[0], first[1] + second[1]


class State:
    def __init__(self, maze_layout: [[int]], start: (int, int), end: (int, int), current: (int, int) = None):
        self.maze_layout = copy.deepcopy(maze_layout) # todo remove comment
        self.start = start
        self.end = end

        if current is None:
            self.current = start
        else:
            self.current = current

        self.height = len(maze_layout)
        self.width = len(maze_layout[0])

    def is_final(self) -> bool:
        return self.current == self.end

    def can_move(self, direction: Direction) -> bool:
        next_pos = add_2d(self.current, direction.value)

        return \
            0 <= next_pos[0] < self.height and \
            0 <= next_pos[1] < self.width and \
            self.maze_layout[next_pos[0]][next_pos[1]] == 0

    def get_moved(self, direction: Direction) -> Optional['State']: # todo remove comment
        if self.can_move(direction):
            new_layout = copy.deepcopy(self.maze_layout) # todo remove comment
            new_layout[self.current[0]][self.current[1]] = 2

            return State(
                new_layout,
                self.start,
                self.end,
                add_2d(self.current, direction.value)
            )
        else:
            return None

    def debug_print(self):
        print(self.maze_layout)
        print(self.start, self.end, self.current)

    def pretty_print(self):
        for line in self.maze_layout:
            print(line)

    def finish_path(self) -> 'State': # todo remove comment
        new_layout = self.maze_layout
        new_layout[self.current[0]][self.current[1]] = 2

        return State(new_layout, self.start, self.end, self.current)

    def all_neighbors(self):
        theoretical_neighbors = [self.get_moved(direction) for direction in Direction]
        return filter(lambda n: n is not None, theoretical_neighbors)


def solve_bfs(start: State) -> Optional[State]:
    states = [start]

    while len(states) > 0:
        new_states = []
        for state in states:
            if state.is_final():
                solution = state.finish_path()
                return solution
            new_states += state.all_neighbors()
        states = new_states

    return None


if __name__ == '__main__':
    init_state = State(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        (0, 1),
        (2, 1)
    )
    final_state = solve_bfs(init_state)

    if final_state is None:
        print('No solution found.')
    else:
        final_state.pretty_print()
