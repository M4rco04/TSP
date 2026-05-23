from representation.individual import Individual
import random


class Mutation:
    """Operatory mutacji."""

    @staticmethod
    def swap_2(individual: Individual, probability: float) -> None:
        if random.random() > probability:
            return
        i, j = random.sample(range(len(individual)), k=2)
        individual.genome[i], individual.genome[j] = (
            individual.genome[j],
            individual.genome[i],
        )

    @staticmethod
    def inversion(individual: Individual, probability: float) -> None:
        if random.random() > probability:
            return
        i = random.randint(0, len(individual) - 2)
        j = random.randint(i + 1, len(individual) - 1)
        individual.genome[i : j + 1] = list(reversed(individual.genome[i : j + 1]))
