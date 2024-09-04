from typing import List

from dimacs import print_dimacs


def at_most_two(variables: List[int], aux: int = None):
    if len(variables) <= 3:
        clauses = []
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                for k in range(j + 1, len(variables)):
                    clauses.append([-variables[i], -variables[j], -variables[k]])
        return clauses
    return at_most_two(variables[0:2] + [aux]) + at_most_two([aux] + variables[2:], aux + 1)


def solve(n: int):
    return at_most_two([i + 1 for i in range(n)], n + 1)


if __name__ == '__main__':
    print_dimacs('at most two (with aux)', solve(n=5))
