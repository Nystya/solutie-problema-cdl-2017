
def _expand(current, pattern, index, expanded):
    if index >= len(pattern):
        expanded.append(current)
        return


    if pattern[index].lower() == 'x':
        for i in range(10):
            _expand(current + str(i), pattern, index + 1, expanded)

        return

    _expand(current + pattern[index], pattern, index + 1, expanded)


def expand(pattern):
    expanded = []

    _expand('', pattern, 0, expanded)

    return set(expanded)
