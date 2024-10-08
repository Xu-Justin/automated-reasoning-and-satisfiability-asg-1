from pkg.algo import at_most_two_a, at_most_two_b, tseitin, dpll
from pkg.dimacs import convert_formula_as_dimacs


def main():
    formula_a = at_most_two_a(n=5, k=2)
    print(convert_formula_as_dimacs(formula_a, title='(1a) AtMostTwoA'))
    formula_a = tseitin(formula_a, 1000, 100)
    print(convert_formula_as_dimacs(formula_a, title='(1b) AtMostTwoA - Tseitin Transformation'))

    formula_b = at_most_two_b(n=5, k=2)
    print(convert_formula_as_dimacs(formula_b, title='(1a) AtMostTwoB'))
    formula_b = tseitin(formula_b, 2000, 200)
    print(convert_formula_as_dimacs(formula_b, title='(1b) AtMostTwoB - Tseitin Transformation'))

    formula = formula_a + formula_b + [[-1000], [2000]]
    print(convert_formula_as_dimacs(formula, title='(1c)'))
    print(f'(1d) Verdict: {'SAT' if dpll(formula) else 'UNSAT'}')


if __name__ == '__main__':
    main()
