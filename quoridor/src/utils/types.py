
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Matrix:
    def __init__(self, rows, cols, default_value=None):
        self.rows = rows
        self.cols = cols
        self.data = [[default_value for _ in range(cols)] for _ in range(rows)]

    def is_in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __getitem__(self, position):
        row, col = position
        if not self.is_in_bounds(row, col):
            raise IndexError("Position out of bounds")
        return self.data[row][col]

    def __setitem__(self, position, value):
        row, col = position
        if not self.is_in_bounds(row, col):
            raise IndexError("Position out of bounds")
        self.data[row][col] = value

    def move_item(self, row: int, col: int, new_row: int, new_col: int):
        if not self.is_in_bounds(row, col) or not self.is_in_bounds(new_row, new_col):
            raise IndexError("Position out of bounds")
        self.data[new_row][new_col] = self.data[row][col]
        self.data[row][col] = None

