from typing import List
from representation.individual import Individual
from fitness.fitness_function import FitnessFunction
from representation.problem import Problem


class Population:
    """Reprezentuje populację osobników."""

    def __init__(self, size: int, problem: Problem, board: int):
        self.size = size
        self.population: List[Individual] = []
        self.initialize(board)
        self.evaluate(problem)

    def initialize(self, board: int) -> None:
        """Tworzy początkową populację."""
        self.population = []
        for _ in range(self.size):
            individual = Individual(length=board)
            self.population.append(individual)

    def evaluate(self, problem) -> None:
        """Oblicza fitness dla wszystkich osobników."""
        self.fitness: List[int] = [
            FitnessFunction.evaluate(ind, problem) for ind in self.population
        ]

    def get_best(self) -> Individual:
        """Zwraca najlepszego osobnika."""
        return min(
            self.population, key=lambda x: self.fitness[self.population.index(x)]
        )
