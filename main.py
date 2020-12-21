# Toma Andrei 321CB
# given input: (11V2V~30)^(2V30V11)^(11V30)^(~2V11)
# SAT solver
from bdd_tree import Node
from copy import deepcopy


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


def create_bdd_tree(current_node, variable_list, index):
    ok = 0
    ok_break = -1
    if index == len(variable_list) or current_node.data == 1 or current_node.data == 0:
        return
    current_clauses = deepcopy(current_node.data)
    non_variable = "~" + str(variable_list[index])
    variable = str(variable_list[index])
    counter_pops = 0
    for i in range(len(current_clauses)):
        i = i - counter_pops
        new_clause = ""
        if i < len(current_clauses):
            literals = current_clauses[i].split("V")
            if non_variable in literals:
                if index == len(variable_list) - 1:
                    ok = 1
                else:
                    current_clauses.pop(i)
                    if len(current_clauses) == 0:
                        ok = 1
                        ok_break = 1
                        break
                    counter_pops += 1
            elif variable in literals:
                if len(literals) == 1:
                    ok = 0
                    ok_break = 1
                    break
                else:
                    for j in range(len(literals)):
                        if variable == literals[j]:
                            continue
                        else:
                            new_clause += literals[j] + "V"
                    new_clause = new_clause[:-1]
                    current_clauses[i] = new_clause
    if index < len(variable_list) - 1 and ok_break == -1:
        added_node = Node(current_clauses)
    else:
        added_node = Node(ok)
    current_node.set_left(added_node)
    create_bdd_tree(current_node.left, variable_list, index + 1)
    ok = 0
    ok_break = -1
    current_clauses = deepcopy(current_node.data)
    non_variable = "~" + str(variable_list[index])
    variable = str(variable_list[index])
    counter_pops = 0
    for i in range(len(current_clauses)):
        ok_break = -1
        i = i - counter_pops
        new_clause = ""
        if i < len(current_clauses):
            literals = current_clauses[i].split("V")
            if variable in literals:
                if index == len(variable_list) - 1:
                    ok = 1
                else:
                    current_clauses.pop(i)
                    if len(current_clauses) == 0:
                        ok = 1
                        ok_break = 1
                        break
                    counter_pops += 1
            elif non_variable in literals:
                if index == len(variable_list) - 1 or len(literals) == 1:
                    ok = 0
                    ok_break = 1
                    break
                else:
                    for j in range(len(literals)):
                        if non_variable == literals[j]:
                            continue
                        else:
                            new_clause += literals[j] + "V"
                    new_clause = new_clause[:-1]
                    current_clauses[i] = new_clause
    if index < len(variable_list) - 1 and ok_break == -1:
        added_node = Node(current_clauses)
    else:
        added_node = Node(ok)
    current_node.set_right(added_node)
    create_bdd_tree(current_node.right, variable_list, index + 1)


def initialise_bdd(cnf_bdd):
    clauses = cnf_extract_clauses(cnf_bdd)
    root = Node(clauses)
    number_of_variables, variables_list = get_number_of_variables(clauses)
    create_bdd_tree(root, variables_list, 0)
    return root


def test_bdd(bdd_tree_node):
    if bdd_tree_node.left is None or bdd_tree_node.right is None:
        if bdd_tree_node.data == 1:
            return True
        return False
    if test_bdd(bdd_tree_node.left) is True:
        return True
    if test_bdd(bdd_tree_node.right) is True:
        return True
    return False


if __name__ == '__main__':
    cnf = input()
    bdd_root = initialise_bdd(cnf)
    fnc_matrix = fnc_input(cnf)
    counter_variables = len(fnc_matrix[0])
    bin_arr = [0] * counter_variables
    if test_fnc(fnc_matrix, counter_variables, 0, bin_arr) is True:
        print("YES")
    else:
        print("NO")
    if test_bdd(bdd_root) is True:
        print("YES")
    else:
        print("NO")
