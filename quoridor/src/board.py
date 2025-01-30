from enum import Enum
from utils.types import Position, Matrix
from abc import ABC, abstractmethod

# Types

class WallOrientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Pawn:
    def __init__(self, id, position):
        self.id = id
        self.position = position

class Wall:
    def __init__(self, orientation, position):
        self.orientation = orientation
        self.position = position

class Field:
    def __init__(self, pawn=None):
        self.pawn = pawn

class WallSlot:
    def __init__(self, occupied=False, can_be_occupied=True):
        self.occupied = occupied
        self.can_be_occupied = True
        self.wall = None


# Board class

class BoardBase(ABC):
    @abstractmethod
    def move_pawn(self, pawn_id: int, new_position: Position):
        pass

    @abstractmethod
    def place_wall(self, orientation, position: Position):
        pass

class Board(BoardBase):
    def __init__(self):
        self.board_width = 9

        self.pawn1 = Pawn(1, Position(0, 4))
        self.pawn2 = Pawn(2, Position(8, 4))

        self.fields = Matrix(self.board_width, self.board_width, Field())
        self.horizontal_wall_slots = Matrix(self.board_width - 1, self.board_width, WallSlot())
        self.vertical_wall_slots = Matrix(self.board_width, self.board_width - 1, WallSlot())

    def move_pawn(self, pawn, new_position):
        """Move a pawn to a new position."""
        self.fields.move_item(pawn.position, new_position)

    def place_wall(self, orientation, position):
        """Place a wall at a given position."""
        if orientation == WallOrientation.HORIZONTAL:
            if not self.can_place_wall_at_position(orientation, position):
                raise ValueError("Horizontal wall slot already occupied")
            self.horizontal_wall_slots[position].occupied = True
            next_adjacent_position = Position(position.row, position.col + 1)
            if self.horizontal_wall_slots.is_in_bounds(next_adjacent_position):
                self.horizontal_wall_slots[next_adjacent_position].can_be_occupied = False
            self.vertical_wall_slots[position].can_be_occupied = False

        elif orientation == WallOrientation.VERTICAL:
            if not self.can_place_wall_at_position(orientation, position):
                raise ValueError("Vertical wall slot already occupied")
            self.vertical_wall_slots[position].occupied = True
            next_adjacent_position = Position(position.row + 1, position.col)
            if self.vertical_wall_slots.is_in_bounds(next_adjacent_position):
                self.vertical_wall_slots[next_adjacent_position].can_be_occupied = False
            self.horizontal_wall_slots[position].can_be_occupied = False

    def can_place_wall_at_position(self, orientation, position):
        """Check if a wall can be placed at a given position."""
        if orientation == WallOrientation.HORIZONTAL:
            adjacent_horizontal_slot_position = Position(position.row, position.col + 1)
            return (
                not self.horizontal_wall_slots[position].occupied
                and self.horizontal_wall_slots[position].can_be_occupied
                and self.horizontal_wall_slots[adjacent_horizontal_slot_position].can_be_occupied
                and not self.horizontal_wall_slots[adjacent_horizontal_slot_position].occupied
                and not self.vertical_wall_slots[position].occupied
            )
        
        elif orientation == WallOrientation.VERTICAL:
            adjacent_vertical_slot_position = Position(position.row + 1, position.col)
            return (
                not self.vertical_wall_slots[position].occupied
                and self.vertical_wall_slots[position].can_be_occupied
                and self.vertical_wall_slots[adjacent_vertical_slot_position].can_be_occupied
                and not self.vertical_wall_slots[adjacent_vertical_slot_position].occupied
                and not self.horizontal_wall_slots[position].occupied
            )


# Example usage:

if __name__ == "__main__":
    board = Board()

    # Move pawn 1 to a new position
    new_position_pawn1 = Position(1, 4)
    board.move_pawn(board.pawn1, new_position_pawn1)
    print(f"Pawn 1 moved to {new_position_pawn1}")

    # Move pawn 2 to a new position
    new_position_pawn2 = Position(7, 4)
    board.move_pawn(board.pawn2, new_position_pawn2)
    print(f"Pawn 2 moved to {new_position_pawn2}")

    # Place a horizontal wall
    wall_position_horizontal = Position(4, 4)
    board.place_wall(WallOrientation.HORIZONTAL, wall_position_horizontal)
    print(f"Horizontal wall placed at {wall_position_horizontal}")

    # Place a vertical wall
    wall_position_vertical = Position(5, 5)
    board.place_wall(WallOrientation.VERTICAL, wall_position_vertical)
    print(f"Vertical wall placed at {wall_position_vertical}")