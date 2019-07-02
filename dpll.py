from z3 import *
'''
The formula has to be written as a list of lists.
Allowed operators: AND, OR, NOT, IMPLIES, BI-IMPLIES
'''

formula_list = ["AND", "x = y", ["OR", ["AND", "y = z", ["NOT", "x = z"]], "x = z"]]


def get_operator(operator):
    if operator == "NOT":
        return Not
    elif operator == "AND":
        return And
    elif operator == "OR":
        return Or
    elif operator == "IMPLIES":
        return Implies
    elif operator == "BI-IMPLIES":
        return operator
    else:
        return False


def get_inner_most(f_list, to_avoid=None):  # Todo: this works
    last_one = None
    while True:
        if to_avoid == f_list:
            return last_one
        if all(type(i) == str for i in f_list):
            return f_list
        for i in f_list:
            if type(i) == list:
                last_one = f_list
                f_list = i
                break


def get_sat_formula(sat_formula, operator_str, variables):
    if sat_formula is None:
        if operator_str == "BI-IMPLIES":
            return variables[0] == variables[1]
        elif operator_str == "NOT":
            return Not(variables[0])
        else:
            operator = get_operator(operator_str)
            if operator:
                return operator(variables)
            else:
                print("{}: operator not valid.".format(operator_str))
                return False
    else:
        if operator_str == "BI-IMPLIES":
            return variables[0] == sat_formula
        elif operator_str == "NOT":
            return Not(sat_formula)
        else:
            operator = get_operator(operator_str)
            if operator:
                variables.append(sat_formula)
                return operator(variables)
            else:
                print("{}: operator not valid.".format(operator_str))
                return False


def sat_solver(f_list):
    sat_formula = None
    inner_most = get_inner_most(f_list)
    while True:
        variables = []
        if inner_most is None:
            break
        else:
            for i in inner_most[1:]:
                if type(i) == str:
                    variables.append(Bool(i))
            sat_formula = get_sat_formula(sat_formula, inner_most[0], variables)
        inner_most = get_inner_most(f_list, to_avoid=inner_most)

    return sat_formula


if __name__ == "__main__":
    sat_formula = sat_solver(formula_list)
    s = Solver()
    s.add(sat_formula)
    s.check()
    m = s.model()
    variables_for_dtp = []
    for d in m.decls():
        if m[d]:
            variables_for_dtp.append(d)
        else:
            variables_for_dtp.append(Not(d))
    dtp = And(variables_for_dtp)
    solve(dtp)


#
# dpt = And(x == y, y == z, Not(x == z))
# solve(dpt)
