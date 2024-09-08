from pkg.type import Formula


def convert_formula_as_dimacs(formula: Formula, title: str = None, compress: bool = True) -> str:
    variables = set(abs(literal) for clause in formula for literal in clause)

    compress_mapping = dict()
    for i, var in enumerate(sorted(variables)):
        compress_mapping[var] = i + 1

    results = []
    if title:
        results.append(f'c {title}')

    results.append(f'p cnf {len(formula)} {len(variables)}')
    for clause in formula:
        _clause = []
        for literal in clause:
            if not compress:
                _clause.append(literal)
                continue
            var = abs(literal)
            if literal > 0:
                _clause.append(compress_mapping[var])
            else:
                _clause.append(-compress_mapping[var])

        results.append(f'{' '.join(map(str, _clause))} 0')

    return '\n'.join(results)
