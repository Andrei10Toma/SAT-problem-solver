def check_clause_fnc(clause, interpret):
    for i in range(len(clause)):
        if clause[i] == -1 and interpret[i] == 0:
            return True
        elif clause[i] == 1 and interpret[i] == 1:
            return True
        elif clause[i] == 0:
            continue
    return False


def test_fnc(fnc, n, index, interpretation):
    if index == n:
        for clause in fnc.values():
            if check_clause_fnc(clause, interpretation) is False:
                return False
        return True
    interpretation[index] = 0
    if test_fnc(fnc, n, index + 1, interpretation) is True:
        return True
    interpretation[index] = 1
    if test_fnc(fnc, n, index + 1, interpretation) is True:
        return True
    return False
