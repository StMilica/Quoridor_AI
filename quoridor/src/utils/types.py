from enum import Enum
    
class Position:
    
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __iter__(self):
        return iter((self.row, self.col))
    
    def __eq__(self, other):
        if isinstance(other, Position):
            return self.row == other.row and self.col == other.col
        return False

    def __repr__(self):
        return f"Position(row={self.row}, col={self.col})"
    
    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.row + other.row, self.col + other.col)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.row - other.row, self.col - other.col)
        return NotImplemented

class WallOrientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

    @staticmethod
    def from_direction(direction):
        if direction in [Direction.UP, Direction.DOWN]:
            return WallOrientation.HORIZONTAL
        return WallOrientation.VERTICAL
    
class WallSlotPosition(Enum):
    UP_LEFT = Position(-1, -1)
    UP_RIGHT = Position(-1, 1)
    DOWN_LEFT = Position(1, -1)
    DOWN_RIGHT = Position(1, 1)
    
class Direction(Enum):
    UP = Position(-1, 0)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)
    RIGHT = Position(0, 1)

    @staticmethod
    def from_positions(start: Position, end: Position):
        delta = end - start
        if abs(delta.row) + abs(delta.col) != 1:
            raise ValueError("Positions are not directly adjacent")
        
        for direction in Direction:
            if direction.value == Position(delta.row, delta.col):
                return direction
        raise ValueError("Invalid direction")
    
    def rotate_left(self):
        return {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP
        }[self]
    
    def rotate_right(self):
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP
        }[self]
        
    def perpendicular_directions(self):
        return {
            Direction.UP: (Direction.LEFT, Direction.RIGHT),
            Direction.RIGHT: (Direction.UP, Direction.DOWN),
            Direction.DOWN: (Direction.LEFT, Direction.RIGHT),
            Direction.LEFT: (Direction.UP, Direction.DOWN)
        }[self]
    
    def wall_slot_positions(self):
        return {
            Direction.UP: (WallSlotPosition.UP_LEFT, WallSlotPosition.UP_RIGHT),
            Direction.RIGHT: (WallSlotPosition.UP_RIGHT, WallSlotPosition.DOWN_RIGHT),
            Direction.DOWN: (WallSlotPosition.DOWN_LEFT, WallSlotPosition.DOWN_RIGHT),
            Direction.LEFT: (WallSlotPosition.UP_LEFT, WallSlotPosition.DOWN_LEFT)
        }[self]
    
    @staticmethod
    def all_directions() -> list['Direction']:
        return list(Direction)
    
    

class Matrix:
    def __init__(self, rows, cols, default_value=None):
        self.rows = rows
        self.cols = cols
        self.data = [[default_value for _ in range(cols)] for _ in range(rows)]

    def is_in_bounds(self, position):
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __getitem__(self, position):
        row, col = position
        if not self.is_in_bounds(position):
            raise IndexError("Position out of bounds")
        return self.data[row][col]

    def __setitem__(self, position, value):
        row, col = position
        if not self.is_in_bounds(position):
            raise IndexError("Position out of bounds")
        self.data[row][col] = value

    def move_item(self, current_position, new_position):
        current_row, current_col = current_position
        new_row, new_col = new_position
        if not self.is_in_bounds(current_position) or not self.is_in_bounds(new_position):
            raise IndexError("Position out of bounds")
        self.data[new_row][new_col] = self.data[current_row][current_col]
        self.data[current_row][current_col] = None

