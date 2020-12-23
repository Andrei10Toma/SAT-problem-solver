# Toma Andrei 321CB
from create_fnc import *
from evaluate_fnc import *
from evaluate_bdd import *
from create_bdd import *


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
