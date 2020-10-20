from enum import Enum
from typing import Optional
import random

import copy


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def add_2d(first: (int, int), second: (int, int)):
    return first[0] + second[0], first[1] + second[1]


def manhattan_distance(first: (int, int), second: (int, int)):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


class State:
    def __init__(self, maze_layout: [[int]], start: (int, int), end: (int, int), current: (int, int) = None):
        self.maze_layout = copy.deepcopy(maze_layout)
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

    def can_move(self, direction: Direction, no_return: bool = True) -> bool:
        next_pos = add_2d(self.current, direction.value)

        return \
            0 <= next_pos[0] < self.height and \
            0 <= next_pos[1] < self.width and \
            (
                self.maze_layout[next_pos[0]][next_pos[1]] == 0
                if no_return
                else self.maze_layout[next_pos[0]][next_pos[1]] != 1
            )

    def get_moved(self, direction: Direction, no_return: bool = True) -> Optional['State']:
        if self.can_move(direction, no_return):
            new_layout = copy.deepcopy(self.maze_layout)
            next_position = add_2d(self.current, direction.value)

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

    def finish_path(self) -> 'State':
        new_layout = self.maze_layout
        new_layout[self.current[0]][self.current[1]] = 2

        return State(new_layout, self.start, self.end, self.current)

    def all_neighbors(self):
        theoretical_neighbors = [self.get_moved(direction) for direction in Direction]
        return list(filter(lambda n: n is not None, theoretical_neighbors))

    def get_score(self) -> int:
        return manhattan_distance(self.current, self.end)

    def first_better_neighbor(self) -> Optional['State']:
        current_score = self.get_score()
        theoretical_neighbors = [self.get_moved(direction) for direction in Direction]

        for neighbor in theoretical_neighbors:
            if neighbor is not None and neighbor.get_score() <= current_score:
                return neighbor

        return None

    def random_neighbor(self) -> Optional['State']:
        current_score = self.get_score()

        theoretical_neighbors = [self.get_moved(direction, no_return=False) for direction in Direction]
        actual_neighbors = list(filter(lambda n: n is not None, theoretical_neighbors))

        neighbor = random.choice(actual_neighbors)

        neighbor_score = neighbor.get_score()
        if neighbor_score < current_score:
            return neighbor
        else:
            heat = neighbor_score / manhattan_distance(self.start, self.end)
            if random.random() < heat:
                return neighbor
            else:
                return None


def solve_backtracking(start: State) -> Optional[State]:
    if start.is_final():
        return start.finish_path()

    for direction in Direction:
        if start.can_move(direction):
            solution = solve_backtracking(start.get_moved(direction))
            if solution is not None:
                return solution
    return None


# very poor memory efficiency and speed, due to representation; alternative would require representations tailored to
# each algorithm
def solve_bfs(start: State) -> Optional[State]:
    states = [start]

    while len(states) > 0:
        new_states = []
        for state in states:
            neighbors = state.all_neighbors()
            for neighbor in neighbors:
                if neighbor.is_final():
                    solution = neighbor.finish_path()
                    return solution
            new_states += neighbors
        states = new_states

    return None


def solve_hill_climber(start: State) -> Optional[State]:
    state = start

    while state is not None:
        if state.is_final():
            state = state.finish_path()
            break
        better_neighbor = state.first_better_neighbor()
        state = better_neighbor

    return state


def solve_annealing(start: State) -> Optional[State]:
    state = start

    step = 1
    step_limit = 1000
    while not state.is_final() and step < step_limit:
        neighbor = state.random_neighbor()
        if neighbor is not None:
            state = neighbor

    if state.is_final():
        return state.finish_path()
    else:
        return None


if __name__ == '__main__':
    init_state = State(
        [
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        ],
        (0, 0),
        (6, 21)
    )
    init_easy = State(
        [
            [0, 0, 0, 1, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0],
        ],
        (0, 0),
        (4, 4)
    )

    'uncomment one to run test:'
    'backtracking:'
    final_state = solve_backtracking(init_state)
    'bfs:'
    # final_state = solve_bfs(init_state)
    'hill climber gets stuck in local minima, needs easier example:'
    # final_state = solve_hill_climber(init_easy)
    'annealing:'
    # final_state = solve_annealing(init_state)

    if final_state is None:
        print('No solution found.')
    else:
        final_state.pretty_print()
