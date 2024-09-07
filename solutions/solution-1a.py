from typing import List

from pkg.dimacs import parse_dimacs
from pkg.terms import Formula, Var, Not, Clause, Aux


def at_most_two_a(variables: List[str | Var | Not]) -> Formula:
    formula = Formula()
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            for k in range(j + 1, len(variables)):
                formula.add(Clause(
                    Not(variables[i]),
                    Not(variables[j]),
                    Not(variables[k])
                ))
    return formula


def at_most_two_b(variables: List[str | Var | Not], aux: Aux) -> Formula:
    if len(variables) <= 3:
        return at_most_two_a(variables)
    aux_var = aux.next()
    return at_most_two_a(variables[:2] + [aux_var]) + at_most_two_b([Not(aux_var)] + variables[2:], aux)


def solve():
    formula_a = at_most_two_a(['x1', 'x2', 'x3', 'x4', 'x5'])
    # print(formula_a)
    dimacs_a = parse_dimacs(formula_a, title='AtMostTwoA', mapping=False)
    print(dimacs_a)

    formula_b = at_most_two_b(['x1', 'x2', 'x3', 'x5', 'x5'], Aux('z'))
    # print(formula_b)
    dimacs_b = parse_dimacs(formula_b, title='AtMostTwoB', mapping=False)
    print(dimacs_b)


if __name__ == '__main__':
    solve()
