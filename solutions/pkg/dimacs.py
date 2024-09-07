from pkg.terms import Formula


def parse_dimacs(formula: Formula, title: str = None, mapping: bool = True):
    symbols = set()
    for clause in formula.clauses:
        for literal in clause.literals:
            symbols.add(literal.symbol)

    symbol_mapping = dict((symbol, index + 1) for index, symbol in enumerate(sorted(symbols)))

    results = []

    if title:
        results.append(f'c {title}')

    if mapping:
        results.append(f'c mapping: {symbol_mapping}')

    results.append(f'p cnf {len(symbols)} {len(formula.clauses)}')
    for clause in formula.clauses:
        clause_results = []
        for literal in clause.literals:
            if literal.is_complement():
                clause_results.append(-symbol_mapping[literal.symbol])
            else:
                clause_results.append(symbol_mapping[literal.symbol])
        clause_results.append(0)
        results.append(f'{' '.join(str(result) for result in clause_results)}')

    return '\n'.join(str(result) for result in results)
