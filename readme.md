# TSP Solver - Evolutionary Algorithms and Local Search

This project provides a platform for solving the Traveling Salesman Problem (TSP) using three advanced metaheuristics: **Evolutionary Algorithm**, **Simulated Annealing**, and **Hill Climbing with Perturbations (Iterated Local Search)**. The program finds the optimal or near-optimal path visiting all cities based on a distance matrix.

## 📂 Project Structure

The code is organized in a modular way, allowing for easy swapping of operators and the addition of new algorithms:

`main.py` – The main script controlling the process of loading data and running all three algorithms.

`algorithm/` – Computational core:

* `evolutionary_algorithm.py` – Class managing the evolutionary cycle.
* `local_search.py` – Abstract base class providing a common interface and operators (2-opt, 3-opt) for local search methods.
* `hill_climbing.py` – Advanced implementation of hill climbing (Iterated Local Search).
* `annealing.py` – Implementation of simulated annealing with a reheating mechanism.

`representation/` – Data models:

* `individual.py` – Representation of the route (genome).
* `population.py` – Management of the population of individuals.
* `problem.py` – Handling distance matrix loading from CSV files.

`genetic_operators/` – Logic for modifying solutions (for EA):

* `selection.py` – Parent selection methods (tournament, roulette wheel).
* `crossover.py` – Crossover operators (PMX, Order).
* `mutation.py` – Mutation operators (Swap, Inversion).

`fitness/` – Evaluation module:

* `fitness_function.py` – Calculating solution quality (total route length).

---

## 🛠️ Technologies and Patterns Used

* **Python 3.10+** – Utilizing modern language features such as `Type Hints`, `Enums`, and `match/case` structures for strategy management.
* **LRU Cache** – Used in the `FitnessFunction` class to drastically speed up calculations by memorizing results for previously evaluated routes.
* **Object-Oriented Programming (OOP)** – Using abstract classes (`ABC`) and inheritance to avoid code duplication (DRY principle).
* **Argparse** – For professional command-line argument handling.
* **JSON** – Standard for storing configuration parameters for all algorithms.

---

## 🧠 How the Algorithms Work

### 1. Evolutionary Algorithm (EA)

The algorithm simulates the process of natural selection:

* **Initialization**: A random population of individuals (routes) is created.
* **Selection**: Choosing the best routes for reproduction using tournament or roulette wheel selection.
* **Crossover**: Combining traits of two routes (PMX, OX) to create offspring that inherit good sub-routes.
* **Mutation**: Random changes in the route (Inversion/Swap) to prevent getting stuck in local optima.
* **Elitism**: Preserving the 2 best solutions found so far when transitioning to a new generation.

### 2. Hill Climbing with Perturbations (Iterated Local Search)

An advanced stochastic algorithm that explores the neighborhood of a solution:

* **3-opt Neighborhood**: The algorithm evaluates 7 different combinations of edge reconnections (including variants that reduce to 2-opt) for a randomly selected route cut.
* **Neighbor Selection Strategies**: Three selection approaches are implemented:
* *FirstBest* – chooses the first improving neighbor.
* *TheBest* – checks all neighbors and selects the objectively shortest route.
* *TheWorstBest* – chooses a route that improves the result, but by the smallest possible margin.


* **Perturbations**: If the algorithm gets stuck in a local optimum (stagnation), it executes a series of strong random moves (random walks) to escape the local minimum and resume climbing.

### 3. Simulated Annealing (SA)

A metaheuristic inspired by the cooling process of thermodynamic systems:

* **2-opt Operator**: A fast mechanism for reversing a random segment of the route to remove intersections.
* **Acceptance of Worse Solutions**: The algorithm can accept a longer route to escape a local minimum. The probability of this depends on the Boltzmann distribution and the current temperature.
* **Cooling and Reheating**: The temperature drops geometrically (the `alpha` coefficient). In case of prolonged stagnation, the algorithm uses a "reheating" mechanism (`reheats`) to increase space exploration anew.

---

## ⚙️ Configuration (settings.json)

All control parameters are located in the `settings.json` file. It should contain three main sections:

| Parameter | Algorithm | Description |
| --- | --- | --- |
| `population` | EA | Population size in the evolutionary algorithm |
| `mutation_rate` | EA | Probability of mutation occurrence (e.g., 0.05) |
| `timeout` | EA | Maximum evolution time in seconds |
| `generations` | EA | Generation limit (if time is not exceeded) |
| `max_stagnation` | HC / SA | Number of iterations without improvement triggering perturbation (HC) or reheating (SA) |
| `n_iterations` | HC | Main number of climbing iterations |
| `perturbation_walks` | HC | "Kick" strength (number of random 2-opt moves after stagnation) |
| `neighbor_type` | HC | Selection strategy (0 = FirstBest, 1 = TheBest, 2 = TheWorstBest) |
| `temperature` | SA | Starting temperature for annealing |
| `alpha` | SA | Cooling coefficient (typically between 0.9 and 0.999) |
| `reheats` | SA | Number of allowed system "reheats" after reaching stagnation |

---

## 🚀 Running Instructions

1. Ensure your data files (distance matrices in CSV format) are located in the `problem/` folder.
2. Configure the parameters in the `settings.json` file in the main project directory.
3. Run the program from the command line, providing the data file name (including the extension):

```bash
python main.py -f file_name.csv

```

Upon completion, the program will display the best route found and its cost (Fitness) sequentially for each of the three algorithms, allowing for a direct comparison of their effectiveness.
