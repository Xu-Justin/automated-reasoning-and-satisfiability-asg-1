import solution
from pkg.dimacs import parse_dimacs
from pkg.terms import Aux


def solve():
    formulaA = solution.atMostTwoA(['x1', 'x2', 'x3', 'x4', 'x5'])
    # print(formulaA)
    dimacsA = parse_dimacs(formulaA, title='AtMostTwoA', mapping=False)
    print(dimacsA)

    formulaB = solution.atMostTwoB(['x1', 'x2', 'x3', 'x5', 'x5'], Aux('z'))
    # print(formulaB)
    dimacsB = parse_dimacs(formulaB, title='AtMostTwoB', mapping=False)
    print(dimacsB)


if __name__ == '__main__':
    solve()
