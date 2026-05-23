from typing import List
from enum import Enum

from algorithm.local_search import LocalSearch
from representation.individual import Individual
from representation.problem import Problem
from fitness.fitness_function import FitnessFunction


class Neighbor(Enum):
    FirstBest = 0
    TheBest = 1
    TheWorstBest = 2


class HillClimbing(LocalSearch):
    max_stagnation: int
    perturbation_walks: int
    neighbor_type: Neighbor

    def __init__(
        self,
        problem: Problem,
        board_size: int,
        max_stagnation: int,
        n_iterations: int,
        perturbation_walks: int,
        neighbor_type: Neighbor
    ):
        super().__init__(problem, board_size)
        self.max_stagnation = max_stagnation
        self.n_iterations = n_iterations
        self.perturbation_walks = perturbation_walks
        self.neighbor_type = neighbor_type

    def _run(self) -> Individual:
        best_nodes = self.nodes.copy()
        best_evo = self.evo

        stagnation_counter = 0

        for _ in range(self.n_iterations):
            if stagnation_counter > self.max_stagnation:
                self.perturbations()
                stagnation_counter = 0

            neighbors = self.swap3opt(self.nodes)
            neighbor = self.choose_neighbor(neighbors)

            if neighbor is None:
                stagnation_counter += 1
                continue

            stagnation_counter = 0

            self.nodes = neighbor
            self.evo = FitnessFunction.evaluate(neighbor, self.problem)

            if self.evo < best_evo:
                best_nodes = self.nodes.copy()
                best_evo = self.evo

        return best_nodes

    def perturbations(self) -> None:
        for _ in range(self.perturbation_walks):
            self.nodes = self.swap2opt(self.nodes)

        self.evo = FitnessFunction.evaluate(self.nodes, self.problem)

    def choose_neighbor(self, neighbors: List[Individual]) -> Individual | None:
        match self.neighbor_type:
            case Neighbor.FirstBest:
                return self.first_best_neighbor(neighbors)
            case Neighbor.TheBest:
                return self.the_best_neighbor(neighbors)
            case Neighbor.TheWorstBest:
                return self.the_worst_best_neighbor(neighbors)
            case _:
                raise ValueError("No such neighbor type")

    def first_best_neighbor(self, neighbors: List[Individual]) -> Individual | None:
        for neighbor in neighbors:
            evo = FitnessFunction.evaluate(neighbor, self.problem)
            if evo < self.evo:
                return neighbor
        return None

    def the_best_neighbor(self, neighbors: List[Individual]) -> Individual | None:
        evaluated_neighbors = [
            (n, FitnessFunction.evaluate(n, self.problem)) for n in neighbors
        ]

        best_neighbor, best_evo = min(evaluated_neighbors, key=lambda x: x[1])

        if best_evo < self.evo:
            return best_neighbor
        return None

    def the_worst_best_neighbor(self, neighbors: List[Individual]) -> Individual | None:
        improving_neighbors = [
            (n, FitnessFunction.evaluate(n, self.problem))
            for n in neighbors
            if FitnessFunction.evaluate(n, self.problem) < self.evo
        ]

        if not improving_neighbors:
            return None

        worst_best_neighbor, _ = max(improving_neighbors, key=lambda x: x[1])
        return worst_best_neighbor
