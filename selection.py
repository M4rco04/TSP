from representation.population import Population
from representation.individual import Individual
import random


class Selection:
    """Metody selekcji."""

    @staticmethod
    def tournament(population: Population, k: int) -> Individual:
        chosen = random.sample(population.population, k=k)
        return min(
            chosen, key=lambda x: population.fitness[population.population.index(x)]
        )

    @staticmethod
    def roulette(population: Population) -> Individual:
        max_fitness = max(population.fitness)
        return random.choices(
            population.population, weights=max_fitness - population.fitness
        )[0]
