from typing import List


class Problem:
    filename: str
    problem: List[List[float]]

    def __init__(self, filename: str):
        self.filename = filename
        self.problem = []
        self.read_file()

    def read_file(self):
        with open(f"problem/{self.filename}", "r") as file:
            for row in file:
                row = row.strip().split(",")
                tmp = []
                for cell in row:
                    tmp.append(int(cell))
                self.problem.append(tmp)
