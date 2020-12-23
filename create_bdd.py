from node_class import Node
from copy import deepcopy
from helper import *


def create_bdd_tree(current_node, variable_list, index):
    if index == len(variable_list) or current_node.data == 1 or current_node.data == 0:
        return
    variable = str(variable_list[index])
    non_variable = "~" + str(variable_list[index])
    current_clauses = deepcopy(current_node.data)
    update_clauses(current_clauses, current_node, index, variable_list, non_variable, variable, "left")
    create_bdd_tree(current_node.left, variable_list, index + 1)
    current_clauses = deepcopy(current_node.data)
    update_clauses(current_clauses, current_node, index, variable_list, variable, non_variable, "right")
    create_bdd_tree(current_node.right, variable_list, index + 1)


def update_clauses(current_clauses, current_node, index, variable_list, variable, non_variable, case):
    ok_break = -1
    leaf_value = 0
    counter_pops = 0
    for i in range(len(current_clauses)):
        ok_break = -1
        i = i - counter_pops
        new_clause = ""
        if i < len(current_clauses):
            literals = current_clauses[i].split("V")
            if variable in literals:
                if index == len(variable_list) - 1:
                    leaf_value = 1
                else:
                    current_clauses.pop(i)
                    if len(current_clauses) == 0:
                        leaf_value = 1
                        ok_break = 1
                        break
                    counter_pops += 1
            elif non_variable in literals:
                if len(literals) == 1:
                    leaf_value = 0
                    ok_break = 1
                    break
                else:
                    for j in range(len(literals)):
                        if non_variable != literals[j]:
                            new_clause += literals[j] + "V"
                    new_clause = new_clause[:-1]
                    current_clauses[i] = new_clause
    if index < len(variable_list) - 1 and ok_break == -1:
        added_node = Node(current_clauses)
    else:
        added_node = Node(leaf_value)
    if case == "right":
        current_node.set_right(added_node)
    elif case == "left":
        current_node.set_left(added_node)


def initialise_bdd(cnf_bdd):
    clauses = cnf_extract_clauses(cnf_bdd)
    root = Node(clauses)
    number_of_variables, variables_list = get_number_of_variables(clauses)
    create_bdd_tree(root, variables_list, 0)
    return root
