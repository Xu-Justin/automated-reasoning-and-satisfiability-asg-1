from typing import List

from pkg.terms import Formula, Var, Not, Clause, Aux


def atMostTwoA(variables: List[str | Var | Not]) -> Formula:
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


def atMostTwoB(variables: List[str | Var | Not], aux: Aux) -> Formula:
    if len(variables) <= 3:
        return atMostTwoA(variables)
    aux_var = aux.next()
    return atMostTwoA(variables[:2] + [aux_var]) + atMostTwoB([Not(aux_var)] + variables[2:], aux)
