import random
import math

from algorithm.local_search import LocalSearch
from representation.individual import Individual
from representation.problem import Problem
from fitness.fitness_function import FitnessFunction


class Annealing(LocalSearch):
    temp: float
    temp_initial: float
    alfa: float
    max_stagnation: int
    reheats: int

    def __init__(
        self,
        problem: Problem,
        board_size: int,
        temp: float,
        alfa: float,
        max_stagnation: int,
        reheats: int,
    ):
        super().__init__(problem, board_size)
        self.temp_initial = temp
        self.temp = temp
        self.alfa = alfa
        self.max_stagnation = max_stagnation
        self.reheats = reheats

    def _reheat(self) -> None:
        self.temp = self.temp_initial * 0.4
        self.reheats -= 1

    def _run(self) -> Individual:
        best_nodes = self.nodes.copy()
        best_evo = self.evo

        inner_iterations = int(0.5 * (self.board_size**2))
        stagnation_counter = 0

        while self.temp > 1e-4:
            improved_in_this_temp = False

            for _ in range(inner_iterations):
                potential_solution = self.swap2opt(self.nodes)

                potential_evo = FitnessFunction.evaluate(
                    potential_solution, self.problem
                )
                evo_diff = potential_evo - self.evo

                if evo_diff < 0 or random.random() < math.exp(-evo_diff / self.temp):
                    self.nodes = potential_solution
                    self.evo = potential_evo

                    if self.evo < best_evo:
                        best_evo = self.evo
                        best_nodes = self.nodes.copy()
                        improved_in_this_temp = True
                        stagnation_counter = 0

            self.temp *= self.alfa

            if not improved_in_this_temp:
                stagnation_counter += 1

            if stagnation_counter >= self.max_stagnation and self.reheats > 0:
                self._reheat()
                stagnation_counter = 0

        return best_nodes
