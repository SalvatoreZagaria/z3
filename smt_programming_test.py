from z3 import *


def sum_to_five():
    x = Int("x")
    y = Int("y")
    s = Solver()
    s.add(x >= -10, x <= 10)
    s.add(y >= -10, y <= 10)
    s.add(x + y == 5)
    while True:
        if s.check() == sat:
            m = s.model()
            print("x: {}; y: {}".format(m[x], m[y]))
            s.add(Or(x != m[x], y != m[y]))
        else:
            print("Done.")
            break


def ex1():
    init = 1
    trans = [(1, 2), (2, 3)]
    final = 3
    return init, trans, final


def ex2():
    init = 1
    trans = [(1, 2), (3, 4), (4, 5)]
    final = 5
    return init, trans, final


def is_n_reachable(problem, n):
    def transition(i, variables, trans):
        enc = []
        for tr in trans:
            src, dst = tr
            enc.append(And(variables[i] == src, variables[i + 1] == dst))
        return Or(enc)
        # enc = False
        # for tr in trans:
        #     src, dst = tr
        #     enc = Or(enc, And(variables[i] == src, variables[i+1] == dst))
        # return enc

    init, trans, final = problem
    s = Solver()
    variables = [Int(str(i)) for i in range(n + 1)]
    conditions = [variables[0] == init]
    for i in range(n):
        conditions.append(transition(i, variables, trans))
    conditions.append(variables[n] == final)
    s.add(And(conditions))
    if s.check() == sat:
        print("Sat!")
        print(s.model())
        return True
    else:
        print(s.check())
        return False


def is_reachable(problem, n):
    for i in range(n+1):
        print("Checking {}-reachability...".format(i))
        if is_n_reachable(problem, i):
            break


if __name__ == "__main__":
    sum_to_five()
    is_reachable(ex1(), 3)
    is_reachable(ex2(), 4)
