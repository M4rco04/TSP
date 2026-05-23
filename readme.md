# TSP Solver - Algorytmy Ewolucyjne i Przeszukiwanie Lokalne

Projekt ten stanowi platformę do rozwiązywania problemu komiwojażera (Traveling Salesman Problem - TSP) przy użyciu trzech zaawansowanych metaheurystyk: **Algorytmu Ewolucyjnego**, **Symulowanego Wyżarzania** oraz **Wspinaczki Górskiej z Perturbacjami (Iterated Local Search)**. Program znajduje optymalną lub bliską optymalnej ścieżkę odwiedzającą wszystkie miasta w oparciu o macierz odległości.

## 📂 Struktura projektu

Kod jest zorganizowany w sposób modułowy, co pozwala na łatwą wymianę operatorów i dodawanie nowych algorytmów:

`main.py` – Główny skrypt sterujący procesem wczytywania danych i uruchamiania wszystkich trzech algorytmów.

`algorithm/` – Rdzeń obliczeniowy:
* `evolutionary_algorithm.py` – Klasa zarządzająca cyklem ewolucyjnym.
* `local_search.py` – Abstrakcyjna klasa bazowa dostarczająca wspólny interfejs i operatory (2-opt, 3-opt) dla metod przeszukiwania lokalnego.
* `hill_climbing.py` – Zaawansowana implementacja wspinaczki górskiej (Iterated Local Search).
* `annealing.py` – Implementacja symulowanego wyżarzania z mechanizmem ponownego podgrzewania.

`representation/` – Modele danych:
* `individual.py` – Reprezentacja trasy (genomu).
* `population.py` – Zarządzanie zbiorem osobników.
* `problem.py` – Obsługa wczytywania macierzy odległości z plików CSV.

`genetic_operators/` – Logika modyfikacji rozwiązań (dla EA):
* `selection.py` – Metody wyboru rodziców (turniejowa, ruletkowa).
* `crossover.py` – Operatory krzyżowania (PMX, Order).
* `mutation.py` – Operatory mutacji (Swap, Inversion).

`fitness/` – Moduł oceny:
* `fitness_function.py` – Obliczanie jakości rozwiązania (całkowitej długości trasy).

---

## 🛠️ Użyte technologie i wzorce

* **Python 3.10+** – Wykorzystanie nowoczesnych mechanizmów języka, takich jak `Type Hints`, `Enums` oraz struktury `match/case` do zarządzania strategiami.
* **LRU Cache** – Wykorzystany w klasie `FitnessFunction` w celu drastycznego przyspieszenia obliczeń poprzez zapamiętywanie wyników dla już sprawdzonych tras.
* **Architektura zorientowana obiektowo (OOP)** – Wykorzystanie klas abstrakcyjnych (`ABC`) i dziedziczenia w celu unikania duplikacji kodu (DRY).
* **Argparse** – Do profesjonalnej obsługi argumentów linii komend.
* **JSON** – Standard przechowywania parametrów konfiguracyjnych wszystkich algorytmów.

---

## 🧠 Działanie algorytmów

### 1. Algorytm Ewolucyjny (EA)
Algorytm symuluje proces doboru naturalnego:
* **Inicjalizacja**: Tworzona jest losowa populacja osobników (tras).
* **Selekcja**: Wybór najlepszych tras do reprodukcji, przy użyciu metody turniejowej lub ruletki.
* **Krzyżowanie (Crossover)**: Łączenie cech dwóch tras (PMX, OX), aby stworzyć potomstwo dziedziczące dobre pod-trasy.
* **Mutacja**: Losowe zmiany w trasie (Inwersja/Swap), zapobiegające utknięciu w optimach lokalnych.
* **Elitaryzm**: Zachowanie 2 najlepszych znalezionych dotąd rozwiązań przy przejściu do nowej generacji.

### 2. Wspinaczka Górska z Perturbacjami (Iterated Local Search)
Zaawansowany algorytm stochastyczny badający sąsiedztwo rozwiązania:
* **Sąsiedztwo 3-opt**: Algorytm ocenia 7 różnych kombinacji przepięcia krawędzi (w tym warianty redukujące się do 2-opt) dla wylosowanego cięcia trasy.
* **Strategie Wyboru Sąsiada**: Zaimplementowano trzy podejścia wyboru:
  * *FirstBest* – wybiera pierwszego lepszego sąsiada.
  * *TheBest* – sprawdza wszystkich i wybiera obiektywnie najkrótszą trasę.
  * *TheWorstBest* – wybiera trasę poprawiającą wynik, ale w najmniejszym możliwym stopniu.
* **Perturbacje**: Jeśli algorytm utknie w optimum lokalnym (stagnacja), wykonuje serię silnych losowych ruchów (random walks), aby uciec z minimum lokalnego i wznowić wspinaczkę.

### 3. Symulowane Wyżarzanie (SA)
Metaheurystyka inspirowana procesem stygnięcia układów termodynamicznych:
* **Operator 2-opt**: Szybki mechanizm odwracania losowego fragmentu trasy w celu usuwania skrzyżowań.
* **Akceptacja Gorszych Rozwiązań**: Algorytm może przyjąć dłuższą trasę, by wyjść z minimum lokalnego. Szansa na to zależy od rozkładu Boltzmanna i aktualnej temperatury.
* **Chłodzenie i Reheating**: Temperatura spada geometrycznie (współczynnik `alpha`). W przypadku długotrwałej stagnacji, algorytm używa mechanizmu "ponownego podgrzania" (`reheats`), aby na nowo zwiększyć eksplorację przestrzeni.

---

## ⚙️ Konfiguracja (settings.json)

Wszystkie parametry sterujące znajdują się w pliku `settings.json`. Powinien on zawierać trzy główne sekcje:

| Parametr | Algorytm | Opis |
| --- | --- | --- |
| `population` | EA | Rozmiar populacji w algorytmie ewolucyjnym |
| `mutation_rate` | EA | Prawdopodobieństwo wystąpienia mutacji (np. 0.05) |
| `timeout` | EA | Maksymalny czas trwania ewolucji w sekundach |
| `generations` | EA | Limit pokoleń (jeśli czas nie zostanie przekroczony) |
| `max_stagnation` | HC / SA | Liczba iteracji bez poprawy wyzwalająca perturbację (HC) lub podgrzanie (SA) |
| `n_iterations` | HC | Główna liczba iteracji wspinaczki |
| `perturbation_walks` | HC | Siła "kopnięcia" (liczba losowych ruchów 2-opt po stagnacji) |
| `neighbor_type` | HC | Strategia wyboru (0 = FirstBest, 1 = TheBest, 2 = TheWorstBest) |
| `temperature` | SA | Startowa temperatura dla wyżarzania |
| `alpha` | SA | Współczynnik chłodzenia (zazwyczaj od 0.9 do 0.999) |
| `reheats` | SA | Liczba dozwolonych "podgrzań" układu po osiągnięciu stagnacji |

---

## 🚀 Instrukcja uruchomienia

1. Upewnij się, że Twoje pliki z danymi (macierze odległości w formacie CSV) znajdują się w folderze `problem/`.
2. Skonfiguruj parametry w pliku `settings.json` w głównym katalogu projektu.
3. Uruchom program z wiersza poleceń, podając nazwę pliku z danymi (wraz z rozszerzeniem):

```bash
python main.py -f nazwa_pliku.csv
```

Program po zakończeniu wyświetli najlepszą znalezioną trasę oraz jej koszt (Fitness) sekwencyjnie dla każdego z trzech algorytmów, co pozwala na bezpośrednie porównanie ich skuteczności.