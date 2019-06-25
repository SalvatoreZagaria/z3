from z3 import *

input_matrix = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
allowed = [1,2,3,4,5,6,7,8,9]

def get_matrix():
    if len(input_matrix) != 81:
        return False
    matrix = []
    iterator = iter(input_matrix)
    while True:
        try:
            row = []

            for i in range(9):
                n = next(iterator)
                try:
                    num = int(n)
                    row.append(Int(num))
                except ValueError:
                    row.append(Int(0))
            matrix.append(row)
        except StopIteration:
            break

    return matrix


def get_row(matrix, n):
    return matrix[n][:]


def get_column(matrix, n):
    return [i[n] for i in matrix]


def sudoku_solver():
    s = Solver()
    matrix = get_matrix()
    if not matrix:
        print("Input matrix not valid.")

    for i in range(9):
        s.add(all(matrix[i][:]) == )
        s.add(x in allowed)