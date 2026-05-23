from typing import Tuple
from representation.individual import Individual
import random


class Crossover:
    """Operatory krzyżowania."""

    @staticmethod
    def pmx(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Partially Mapped Crossover (PMX) dla permutacji"""
        size = len(parent1)
        child1, child2 = parent1.copy(), parent2.copy()
        i, j = sorted(random.sample(range(size), 2))

        child1.genome[i : j + 1] = parent2.genome[i : j + 1]
        child2.genome[i : j + 1] = parent1.genome[i : j + 1]

        def fill_child(
            child: Individual, parent_src: Individual, parent_target: Individual
        ):
            for idx in range(size):
                if idx >= i and idx <= j:
                    continue
                gene = parent_src.genome[idx]
                while gene in child.genome[i : j + 1]:
                    gene = parent_src.genome[parent_target.genome.index(gene)]
                child.genome[idx] = gene

        fill_child(child1, parent1, parent2)
        fill_child(child2, parent2, parent1)

        return child1, child2

    @staticmethod
    def order(
        parent1: Individual, parent2: Individual
    ) -> Tuple[Individual, Individual]:
        """Order Crossover (OX) dla permutacji"""
        size = len(parent1)
        child1, child2 = parent1.copy(), parent2.copy()
        i, j = sorted(random.sample(range(size), 2))

        # kopiujemy fragment i do j
        child1.genome[i : j + 1] = parent1.genome[i : j + 1]
        child2.genome[i : j + 1] = parent2.genome[i : j + 1]

        def fill_order(child: Individual, parent_src: Individual):
            pos = (j + 1) % size
            for gene in parent_src.genome:
                if gene not in child.genome:
                    child.genome[pos] = gene
                    pos = (pos + 1) % size

        fill_order(child1, parent2)
        fill_order(child2, parent1)

        return child1, child2
