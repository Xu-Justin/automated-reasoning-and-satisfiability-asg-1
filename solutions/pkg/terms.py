from __future__ import annotations

from types import UnionType
from typing import Tuple


class Var:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def __repr__(self):
        return f'{self.symbol}'


class Not:
    def __new__(cls, expression: Expression):
        if type(expression) is Not:
            return expression.expression
        return super().__new__(cls)

    def __init__(self, expression: Expression):
        self.expression = parse_expression(expression)

    def __repr__(self):
        return f'¬{str(self.expression)}'


class Or:
    def __init__(self, *expressions: Expression):
        self.expressions = parse_expressions(expressions)

    def __repr__(self):
        return f'({' ∨ '.join(str(expression) for expression in self.expressions)})'


class And:
    def __init__(self, *expressions: Expression):
        self.expressions = parse_expressions(expressions)

    def __repr__(self):
        return f'({' ∧ '.join(str(expression) for expression in self.expressions)})'


class Implication:
    def __init__(self, premise: Expression, conclusion: Expression):
        self.premise = parse_expression(premise)
        self.conclusion = parse_expression(conclusion)

    def __repr__(self):
        return f'({str(self.premise)} → {str(self.conclusion)})'

    def transform(self):
        return Or(Not(self.premise), self.conclusion)


class Biconditional:
    def __init__(self, antecedent: Expression, consequent: Expression):
        self.antecedent = parse_expression(antecedent)
        self.consequent = parse_expression(consequent)

    def __repr__(self):
        return f'({str(self.antecedent)} ↔ {str(self.consequent)})'

    def transform(self):
        return And(Implication(self.antecedent, self.consequent), Implication(self.consequent, self.antecedent))


Expression: UnionType = str | Var | Not | Or | And | Implication | Biconditional


def parse_expression(expression: Expression):
    if type(expression) is str:
        return Var(expression)
    if type(expression) is Not and type(expression.expression) is Not:
        return expression.expression.expression
    else:
        return expression


def parse_expressions(expressions: Tuple[Expression, ...]):
    return tuple(parse_expression(expression) for expression in expressions)


class Literal:
    def __init__(self, var: str | Var | Not):
        if type(var) is str:
            self.symbol = var
            self.var = Var(var)
        elif type(var) is Var:
            self.symbol = var.symbol
            self.var = var
        elif type(var) is Not:
            self.symbol = var.expression.symbol
            self.var = var
        else:
            raise TypeError(f'Invalid literal ({type(var)}, {type(var.expression)})')

    def __repr__(self):
        return f'{self.var}'

    def is_complement(self):
        return type(self.var) is Not


def parse_literal(literal: Literal | str | Var | Not):
    if type(literal) is literal:
        return literal
    else:
        return Literal(literal)


def parse_literals(literals: Tuple[Literal | str | Var | Not, ...]):
    return tuple(parse_literal(literal) for literal in literals)


class Clause:
    def __init__(self, *literals: Literal | str | Var | Not):
        self.literals = parse_literals(literals)

    def __repr__(self):
        return f'{' ∨ '.join(str(literal) for literal in self.literals)}'


class Formula:
    def __init__(self, *clauses: Clause):
        self.clauses = clauses

    def __repr__(self):
        return f'{'\n'.join(str(clause) for clause in self.clauses)}'

    def __add__(self, formula: Formula):
        self.add(*formula.clauses)
        return self

    def add(self, *clauses: Clause):
        self.clauses += clauses


class Aux:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.counter = 0

    def next(self):
        self.counter += 1
        return Var(f'{self.symbol}{self.counter}')
