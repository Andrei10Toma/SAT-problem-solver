# Toma Andrei 321CB
# given input: (0V~1)^(~0V1)
# SAT solver

def cnf_extract_clauses(cnf_clauses):
    clauses = cnf_clauses.split(")^(")
    clauses[0] = clauses[0][1:]
    clauses[len(clauses) - 1] = clauses[len(clauses) - 1][:-1]
    return clauses


def generate_fnc(clauses_fnc, variable_dictionary):
    fnc_mat = {}
    for i in range(len(clauses_fnc)):
        fnc_mat[i] = [0] * len(variable_dictionary.keys())
        literals = clauses_fnc[i].split("V")
        for literal in literals:
            if literal[0] != "~":
                fnc_mat[i][variable_dictionary.get(int(literal))] = 1
            else:
                fnc_mat[i][variable_dictionary.get(int(literal[1:]))] = -1
    return fnc_mat


def fnc_input(cnf_modified):
    index_columns = 0
    variable_dictionary = {}
    clauses = cnf_extract_clauses(cnf_modified)
    for clause in clauses:
        literals = clause.split("V")
        for literal in literals:
            if literal[0] != "~":
                if int(literal) not in variable_dictionary.keys():
                    variable_dictionary[int(literal)] = index_columns
                    index_columns += 1
            else:
                if int(literal[1:]) not in variable_dictionary.keys():
                    variable_dictionary[int(literal[1:])] = index_columns
                    index_columns += 1
    return generate_fnc(clauses, variable_dictionary)


def check_clause(clause, interpret):
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
        print(interpretation)
        for clause in fnc.values():
            if check_clause(clause, interpretation) is False:
                return False
        return True
    interpretation[index] = 0
    if test_fnc(fnc, n, index + 1, interpretation) is True:
        return True
    interpretation[index] = 1
    if test_fnc(fnc, n, index + 1, interpretation) is True:
        return True
    return False


def create_bdd(bdd_cnf):
    pass


if __name__ == '__main__':
    cnf = input()
    fnc_matrix = fnc_input(cnf)
    for rows in fnc_matrix.values():
        print(rows)
    counter_variables = len(fnc_matrix[0])
    bin_arr = [0] * counter_variables
    if test_fnc(fnc_matrix, counter_variables, 0, bin_arr) is True:
        print("YES")
    else:
        print("NO")
