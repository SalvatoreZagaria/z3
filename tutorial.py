from z3 import *

input_matrix = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"


def get_matrix():
    if len(input_matrix) != 81:
        return False
    matrix = []
    iterator = iter(input_matrix)
    row_n = 1
    while True:
        try:
            row = []
            for i in range(9):
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
    for i in range(9):
        for j in range(9):
            if type(matrix[i][j]) != int:
                if i != row and j != col:
                    ints.append([i, j])
    return ints


def get_solver(matrix):
    s = Solver()
    for i in range(9):
        for j in range(9):
            if type(matrix[i][j]) != int:
                s.add(matrix[i][j] >= 1, matrix[i][j] <= 9)
                for k in get_row_ints(matrix, i):
                    s.add(matrix[i][j] != k)
                for k in get_column_ints(matrix, j):
                    s.add(matrix[i][j] != k)
                # for k in range(9):
                #     if j != k and type(matrix[i][k]) != int:
                #         s.add(matrix[i][j] != matrix[i][k])
                #     if i != k and type(matrix[k][j]) != int:
                #         s.add(matrix[i][j] != matrix[k][j])
    return s


if __name__ == "__main__":
    matrix = get_matrix()
    if not matrix:
        print("Input matrix not valid.")
    else:
        s = get_solver(matrix)
        if s.check() == sat:
            print("Your Sudoku has been solved.")
            print()
            m = s.model()
            for d in m.decls():
                splitted_name = str(d).split("_")
                row, col = int(splitted_name[0]), int(splitted_name[1])
                matrix[row-1][col-1] = int(m[d].as_long())
            for i in matrix:
                print(i)
        else:
            print("Impossible to solve the Sudoku.")
