from representation.individual import Individual
from representation.problem import Problem

from functools import lru_cache


class FitnessFunction:
    """Funkcja przystosowania dla problemu komiwojażera."""

    @staticmethod
    @lru_cache(maxsize=None)
    def evaluate(individual: Individual, problem: Problem) -> int:
        """Zwraca wartość fitness osobnika."""
        value = 0
        for id in range(0, len(individual)):
            if id == len(individual) - 1:
                value += problem.problem[individual.genome[id] - 1][
                    individual.genome[0] - 1
                ]
                continue
            value += problem.problem[individual.genome[id] - 1][
                individual.genome[id + 1] - 1
            ]

        return value
