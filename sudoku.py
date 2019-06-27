from z3 import Int, Solver, sat, Or, And, Not, simplify
import time

dimension = 3

input_matrix = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
input_matrix = "."*dimension*dimension


def get_matrix():
    if len(input_matrix) != dimension**2:
        return False
    matrix = []
    iterator = iter(input_matrix)
    row_n = 1
    while True:
        try:
            row = []
            for i in range(dimension):
                n = next(iterator)
                try:
                    num = int(n)
                    row.append(num)
                except ValueError:
                    row.append(Int("{}_{}".format(str(row_n), str(i + 1))))
            matrix.append(row)
        except StopIteration:
            break
        row_n += 1

    return matrix


def get_row_ints(matrix, n):
    return [i for i in matrix[n] if type(i) == int]


def get_column_ints(matrix, n):
    return [i[n] for i in matrix if type(i[n]) == int]


def get_all_INT_but(matrix, row, col):
    ints = []
    for i in range(dimension):
        for j in range(dimension):
            if type(matrix[i][j]) != int:
                if i != row and j != col:
                    ints.append([i, j])
    return ints


def get_solver(matrix):
    s = Solver()
    for i in range(dimension):
        for j in range(dimension):
            if type(matrix[i][j]) != int:
                s.add(matrix[i][j] >= 1, matrix[i][j] <= dimension)
                for k in range(dimension):
                    if i != k:
                        s.add(matrix[k][j] != matrix[i][j])
                    if j != k:
                        s.add(matrix[i][k] != matrix[i][j])
    return s


# def get_n_possible_models(s, n_models = 1):
#     m = s.model()
#     d = m.decls()
#     for i in range(len(m)):
#         s.add(m[i] != int(d[m[i].as_long()]))
#         while s.check() == sat:
#             n_models += 1
#             s.add


def get_or_conditions(matrix, m):
    or_condition = []
    for i in range(dimension):
        for j in range(dimension):
            if type(matrix[i][j]) != int:
                or_condition.append(m[matrix[i][j]] == matrix[i][j])
    return or_condition


if __name__ == "__main__":
    matrix = get_matrix()
    if not matrix:
        print("Input matrix not valid.")
    else:
        print("Input matrix:")
        for row in matrix:
            new_row = []
            for i in row:
                if type(i) == int:
                    new_row.append(i)
                else:
                    new_row.append("x")
            print(new_row)
        print()
        print("Dimensions: {0}x{0}".format(dimension))
        print()
        s = get_solver(matrix)
        n_models = 0
        while True:
            start_time = time.time()
            if s.check() == sat:
                n_models += 1
                m = s.model()
                or_condition = get_or_conditions(matrix, m)
                s.add(Or(or_condition))
                # print("Time taken: {}".format(time.time()-start_time))
                # for d in m.decls():
                #     print(d, int(m[d].as_long()))
                # print()
            else:
                break
        if n_models > 0:
            print("The Sudoku is solvable. Number of possible solutions: {}".format(n_models))
        else:
            print("The Sudoku is impossible to solve.")

        # if s.check() == sat:
        #     print("Your Sudoku has been solved.")
        #     print()
        #     m = s.model()
        #     for d in m.decls():
        #         splitted_name = str(d).split("_")
        #         row, col = int(splitted_name[0]), int(splitted_name[1])
        #         matrix[row-1][col-1] = int(m[d].as_long())
        #     for i in matrix:
        #         print(i)
