from typing import List


def print_dimacs(title: str, clauses: List[List[int]]):
    variables = set([variable for clause in clauses for variable in clause])
    print(f'c {title}')
    print(f'p cnf {len(variables)} {len(clauses)}')
    for clause in clauses:
        print(f'{" ".join(map(str, clause))} 0')
