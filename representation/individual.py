from typing import List
import random


class Individual:
    """
    Reprezentuje pojedyncze rozwiązanie problemu komiwojażera.
    Genotyp: lista długości n, gdzie n to liczba wierzchołków, indeks = kolejność odwiedzenia, wartość = numer wierzchołka.
    """

    genome: List[int]

    def __init__(self, length: int, genome: List[int] | None = None):
        self.length = length
        if genome is None:
            self.genome = []
            self.random_initialize()
        else:
            self.genome = genome

    def random_initialize(self) -> None:
        """Losowa inicjalizacja osobnika."""
        rand = list(range(1, self.length + 1))
        random.shuffle(rand)
        self.genome = rand

    def copy(self) -> "Individual":
        """Zwraca kopię osobnika."""
        return Individual(self.length, self.genome.copy())

    def __len__(self) -> int:
        return self.length
