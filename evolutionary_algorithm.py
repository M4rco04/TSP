from datetime import datetime
from typing import List
from representation.population import Population
from representation.individual import Individual
from representation.problem import Problem
from genetic_operators.selection import Selection
from genetic_operators.crossover import Crossover
from genetic_operators.mutation import Mutation


class EvolutionaryAlgorithm:
    """Główny algorytm ewolucyjny."""

    selection_method = "tournament"
    tournament_k = 3

    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
        board_size: int,
        problem: Problem,
        move_timeout: float = 2,
        generations: int | None = None,
    ):
        self.population_size: int = population_size
        self.mutation_rate: float = mutation_rate
        self.problem: Problem = problem
        self.board_size: int = board_size
        self.timeout: float = move_timeout
        self.generations: int | None = generations

    def initialize(self) -> None:
        self.population: Population = Population(
            self.population_size, self.problem, self.board_size
        )

    def _evolve(self) -> Individual:
        """Uruchamia algorytm i zwraca najlepsze znalezione rozwiązanie."""
        while self._any_time_left() and self._have_generations():

            self._replacement(self._mutation(self._crossover(self._selection())))

            if self.generations:
                self.generations -= 1

        return self.population.get_best()

    def _selection(self) -> List[Individual]:
        parents: List[Individual] = []
        for _ in range(self.population_size):
            if self.selection_method == "tournament":
                parent = Selection.tournament(self.population, self.tournament_k)
            elif self.selection_method == "roulette":
                parent = Selection.roulette(self.population)
            parents.append(parent)

        return parents

    def _crossover(self, parents: List[Individual]) -> List[Individual]:
        childs: List[Individual] = []
        for i in range(0, len(parents), 2):
            childs.extend(Crossover.pmx(parents[i], parents[i + 1]))

        return childs

    def _mutation(self, childs: List[Individual]) -> List[Individual]:
        for child in childs:
            Mutation.inversion(child, self.mutation_rate)
            Mutation.swap_2(child, self.mutation_rate)

        return childs

    def _replacement(self, childs: List[Individual]) -> None:
        elite_size = 2
        sorted_population = sorted(
            self.population.population,
            key=lambda ind: self.population.fitness[
                self.population.population.index(ind)
            ],
        )
        elite = sorted_population[:elite_size]

        self.population.population = elite + childs[:-elite_size]
        self.population.evaluate(self.problem)

    def solve(self) -> Individual:
        self.start = datetime.now()
        return self._evolve()

    def _any_time_left(self) -> bool:
        return (datetime.now() - self.start).total_seconds() < self.timeout

    def _have_generations(self) -> bool:
        if self.generations is None:
            return True
        return self.generations
