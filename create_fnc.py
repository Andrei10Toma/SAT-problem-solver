from helper import *


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
    variable_counter = 0
    variable_dictionary = {}
    clauses = cnf_extract_clauses(cnf_modified)
    for clause in clauses:
        literals = clause.split("V")
        for literal in literals:
            if literal[0] != "~":
                if int(literal) not in variable_dictionary.keys():
                    variable_dictionary[int(literal)] = variable_counter
                    variable_counter += 1
            else:
                if int(literal[1:]) not in variable_dictionary.keys():
                    variable_dictionary[int(literal[1:])] = variable_counter
                    variable_counter += 1
    return generate_fnc(clauses, variable_dictionary)
