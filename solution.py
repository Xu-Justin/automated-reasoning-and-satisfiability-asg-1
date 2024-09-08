def atMostTwoA(n, k):
    formula = []
    clause = []

    def _atMostTwoA(start, depth):
        if depth == k + 1:
            formula.append([*clause])
            return
        for i in range(start, n + 1):
            clause.append(-i)
            _atMostTwoA(i + 1, depth + 1)
            clause.pop()

    _atMostTwoA(1, 0)
    return formula


def S(i, j):
    """At least j variables x1, x2, ..., xi are assigned 1"""
    assert i < 10 and j < 10
    return i * 10 + j


def atMostTwoB(n, k):
    formula = []
    for i in range(1, min(n + 1, n + 1 - k)):
        formula.append([-i, S(i, 1)])

    for i in range(1, n):
        for j in range(1, min(i + 1, k + 1)):
            formula.append([-S(i, j), S(i + 1, j)])
            formula.append([-S(i, j), -(i + 1), S(i + 1, j + 1)])

    for i in range(max(1, k + 1), n + 1):
        formula.append([-S(i, k + 1)])

    return formula


def tseitin(formula, y, t):
    assert t >= 100 and y >= 1000
    transformed_formula = [[y]]

    for i in range(len(formula)):
        transformed_formula.append([-y, t + i])

    transformed_formula.append([*[-(t + i) for i in range(len(formula))], y])

    for i, clause in enumerate(formula):
        transformed_formula.append([-(t + i), *clause])
        for var in clause:
            transformed_formula.append([-var, t + i])

    return transformed_formula


def print_dimacs(formula):
    for clause in formula:
        print(f'{' '.join(str(var) for var in clause)} 0')
    print()


def main():
    # print_dimacs(atMostTwoA(5, 2))
    print_dimacs(tseitin(atMostTwoA(5, 2), 1000, 100))

    # print_dimacs(atMostTwoB(5, 2))
    print_dimacs(tseitin(atMostTwoB(5, 2), 2000, 200))


if __name__ == '__main__':
    main()
