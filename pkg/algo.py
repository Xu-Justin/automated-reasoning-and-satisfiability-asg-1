from typing import Dict, List

from pkg.type import Formula, Clause, Literal


def at_most_two_a(n: int, k: int) -> Formula:
    formula = []

    def rec(start: int, depth: int, clause: Clause):
        if depth == k + 1:
            return formula.append([*clause])
        for i in range(start, n + 1):
            clause.append(-i)
            rec(i + 1, depth + 1, clause)
            clause.pop()

    rec(1, 0, [])
    return formula


def at_most_two_b(n: int, k: int) -> Formula:
    formula = []

    def s(i: int, j: int) -> Literal:
        """At least j variables x_1, x_2, ..., x_i are assigned 1"""
        return i * n + j + n

    for i in range(1, min(n + 1, n + 1 - k)):
        formula.append([-i, s(i, 1)])

    for i in range(1, n):
        for j in range(max(1, i - k), min(i + 1, k + 1)):
            formula.append([-s(i, j), s(i + 1, j)])
            formula.append([-s(i, j), -(i + 1), s(i + 1, j + 1)])

    for i in range(max(1, k + 1), n + 1):
        formula.append([-s(i, k + 1)])

    return formula


def tseitin(formula: Formula, y: Literal, t: Literal) -> Formula:
    variables = set(abs(literal) for clause in formula for literal in clause)
    assert y not in variables
    for i in range(len(formula)):
        assert t + i not in variables
        assert t + i != y

    transformed_formula = [[y]]

    for i in range(len(formula)):
        transformed_formula.append([-y, t + i])

    transformed_formula.append([*[-(t + i) for i in range(len(formula))], y])

    for i, clause in enumerate(formula):
        transformed_formula.append([-(t + i), *clause])
        for var in clause:
            transformed_formula.append([-var, t + i])

    return transformed_formula


def dpll(formula: Formula) -> bool:
    unassigned_variable = set(abs(literal) for clause in formula for literal in clause)
    assigned_variable = dict()

    def assign_variable(mapping: Dict[int, bool]):
        for var, value in mapping.items():
            assert var in unassigned_variable
            assert var not in assigned_variable.keys()
            assigned_variable[var] = value
            unassigned_variable.remove(var)

    def unassign_variable(variables: List[int]):
        for var in variables:
            assert var not in unassigned_variable
            assert var in assigned_variable.keys()
            assigned_variable.pop(var)
            unassigned_variable.add(var)

    def assign_formula(formula: Formula, mapping: Dict[int, bool]) -> bool:
        if not mapping:
            return iterate(formula)

        assign_variable(mapping)

        next_mapping = dict()
        next_formula = []
        for clause in formula:
            next_clause = []
            is_false_clause = False
            for literal in clause:
                var = abs(literal)
                if var in unassigned_variable:
                    next_clause.append(literal)
                    continue
                value = assigned_variable[var]
                if (literal > 0) == value:
                    next_clause.clear()
                    is_false_clause = False
                    break
                is_false_clause = True
            if len(next_clause) == 0:
                if is_false_clause:
                    unassign_variable(list(mapping.keys()))
                    return False
                continue
            if len(next_clause) == 1:
                next_var = abs(next_clause[0])
                next_value = next_clause[0] > 0
                if next_var in next_mapping.keys() and next_value != next_mapping[next_var]:
                    unassign_variable(list(mapping.keys()))
                    return False
                next_mapping[next_var] = next_value
            next_formula.append(next_clause)

        verdict = assign_formula(next_formula, next_mapping)
        if not verdict:
            unassign_variable(list(mapping.keys()))
        return verdict

    def iterate(formula: Formula) -> bool:
        if not unassigned_variable:
            assert not formula
            return True

        var = next(iter(unassigned_variable))
        if assign_formula(formula, {var: False}) or assign_formula(formula, {var: True}):
            return True
        return False

    return iterate(formula)
