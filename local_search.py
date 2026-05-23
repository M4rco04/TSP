from abc import ABC, abstractmethod
import random
from datetime import datetime
from typing import List

from representation.individual import Individual
from representation.problem import Problem
from fitness.fitness_function import FitnessFunction


class LocalSearch(ABC):
    problem: Problem
    nodes: Individual
    board_size: int
    evo: int
    time: float

    def __init__(self, problem: Problem, board_size: int):
        self.problem = problem
        self.nodes = Individual(board_size)
        self.evo = FitnessFunction.evaluate(self.nodes, self.problem)
        self.board_size = board_size

    def solve(self) -> Individual:
        start = datetime.now()
        result = self._run()
        self.time = (datetime.now() - start).total_seconds()
        return result

    @abstractmethod
    def _run(self) -> Individual:
        pass

    def swap2opt(self, current_nodes: Individual) -> Individual:
        a, b = sorted(random.sample(range(self.board_size), 2))

        solution = current_nodes.copy()
        solution.genome[a + 1 : b + 1] = reversed(solution.genome[a + 1 : b + 1])
        return solution

    def swap3opt(self, current_nodes: Individual) -> List[Individual]:
        i, j, k = sorted(random.sample(range(1, self.board_size), 3))

        genome: List[int] = current_nodes.genome

        A = genome[:i]
        B = genome[i:j]
        C = genome[j:k]
        D = genome[k:]

        B_rev = B[::-1]
        C_rev = C[::-1]

        combinations = [
            A + B_rev + C + D,
            A + B + C_rev + D,
            A + C_rev + B_rev + D,
            A + B_rev + C_rev + D,
            A + C + B + D,
            A + C + B_rev + D,
            A + C_rev + B + D
        ]

        results = []
        for combo in combinations:
            new_solution = current_nodes.copy()
            new_solution.genome = combo
            results.append(new_solution)

        return results
