from typing import List

from dimacs import print_dimacs


def at_most_two(variables: List[int]):
    clauses = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            for k in range(j + 1, len(variables)):
                clauses.append([-variables[i], -variables[j], -variables[k]])
    return clauses


def solve(n: int):
    return at_most_two([i + 1 for i in range(n)])


if __name__ == '__main__':
    print_dimacs('at most two', solve(n=5))
