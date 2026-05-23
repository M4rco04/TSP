from algorithm.evolutionary_algorithm import EvolutionaryAlgorithm
from algorithm.annealing import Annealing
from algorithm.hill_climbing import HillClimbing, Neighbor
from fitness.fitness_function import FitnessFunction
from representation.problem import Problem

import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="Rozwiązywanie problemu komiwojażera")
    parser.add_argument("-f", "--file", help="Plik, z którego wczytywane są dane")
    args = parser.parse_args()

    # Parametry algorytmu
    with open("settings.json", "r") as file:
        data = json.load(file)

    EVOLUTIONARY = data["evolutionary"]
    HILLCLIMBING = data["hill_climbing"]
    ANNEALING = data["annealing"]

    POP_SIZE = EVOLUTIONARY["population"]  # liczba osobników w populacji
    MUTATION_RATE = EVOLUTIONARY["mutation_rate"]  # prawdopodobieństwo mutacji
    TIMEOUT = EVOLUTIONARY["timeout"]  # czas działania algorytmu w sekundach
    GENERATIONS = EVOLUTIONARY["generations"]  # maksymalna liczba iteracji

    HILLCLIMBING_MAX_STAGNATION = HILLCLIMBING["max_stagnation"]
    N_ITERATIONS = HILLCLIMBING["n_iterations"]
    PERTURBATION_WALKS = HILLCLIMBING["perturbation_walks"]
    NEIGHBOR_TYPE = Neighbor(HILLCLIMBING["neighbor_type"])

    TEMPERATURE = ANNEALING["temperature"]  # temperatura początkowa dla algorytmu wyżarzania
    ALPHA = ANNEALING["alpha"]  # współczynnik zmniejszania temperatury
    MAX_STAGNATION = ANNEALING["max_stagnation"] # maksymalna stagnacja
    REHEATS = ANNEALING["reheats"] #liczba możliwych podgrzań

    # Wybór pliku z danymi
    if not args.file:
        raise ValueError("Nie podano pliku")

    problem = Problem(args.file)

    # Utworzenie instancji algorytmu
    ea = EvolutionaryAlgorithm(
        population_size=POP_SIZE,
        mutation_rate=MUTATION_RATE,
        problem=problem,
        board_size=len(problem.problem),
        move_timeout=TIMEOUT,
        generations=GENERATIONS,
    )

    # Inicjalizacja populacji
    ea.initialize()

    # Uruchomienie ewolucji
    best = ea.solve()

    # Wynik
    print("Najlepszy osobnik znaleziony przez algorytm:")
    print(best.genome)
    print("Fitness:", FitnessFunction.evaluate(best, ea.problem))

    # Utworzenie instancji algorytmu
    hill_climbing = HillClimbing(
        problem=problem,
        board_size=len(problem.problem),
        max_stagnation=HILLCLIMBING_MAX_STAGNATION,
        n_iterations=N_ITERATIONS,
        perturbation_walks=PERTURBATION_WALKS,
        neighbor_type=NEIGHBOR_TYPE
    )

    # Uruchomienie wspinaczki górskiej
    hill_best = hill_climbing.solve()

    # Wynik
    print("Najlepszy wynik korzystając ze wspinaczki górskiej:")
    print(hill_best.genome)
    print("Fitness:", FitnessFunction.evaluate(hill_best, hill_climbing.problem))

    # Utworzenie instancji algorytmu
    annealing = Annealing(
        problem=problem,
        board_size=len(problem.problem),
        temp=TEMPERATURE,
        alfa=ALPHA,
        max_stagnation=MAX_STAGNATION,
        reheats=REHEATS,
    )

    # Uruchomienie wyżarzania
    ann_best = annealing.solve()

    # Wynik
    print("Najlepszy wynik korzystając z wyżarzania:")
    print(ann_best.genome)
    print("Fitness:", FitnessFunction.evaluate(ann_best, annealing.problem))


if __name__ == "__main__":
    main()
