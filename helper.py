def cnf_extract_clauses(cnf_clauses):
    clauses = cnf_clauses.split(")^(")
    clauses[0] = clauses[0][1:]
    clauses[len(clauses) - 1] = clauses[len(clauses) - 1][:-1]
    return clauses


def get_number_of_variables(clauses):
    variable_list = []
    counter = 0
    for clause in clauses:
        literals = clause.split("V")
        for literal in literals:
            if literal[0] != "~":
                if int(literal) not in variable_list:
                    variable_list.append(int(literal))
                    counter += 1
            else:
                if int(literal[1:]) not in variable_list:
                    variable_list.append(int(literal[1:]))
                    counter += 1
    return counter, variable_list
