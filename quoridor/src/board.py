from utils.types import Position, Matrix
    


class Pawn:
    def __init__(self, id, position):
        self.id = id
        self.position = position

class Field:
    def __init__(self, pawn=None):
        self.pawn = pawn

class WallSlot:
    def __init__(self, occupied=False):
        self.occupied = occupied


class Board:
    def __init__(self):
        self.board_width = 9

        self.pawn1 = Pawn(1, Position(0, 4))
        self.pawn2 = Pawn(2, Position(8, 4))

        self.fields = Matrix(self.board_width, self.board_width, Field())
        self.horizontal_wall_slots = Matrix(self.board_width - 1, self.board_width, WallSlot())
        self.vertical_wall_slots = Matrix(self.board_width, self.board_width - 1, WallSlot())

    def _validate_position(self, row, col, max_rows, max_cols):
        if not (0 <= row < max_rows and 0 <= col < max_cols):
            raise ValueError(f"Invalid position: ({row}, {col})")

    def update_player_position(self, row, col, occupied, player=None):
        self._validate_position(row, col, 9, 9)
        self.fields[row, col].occupied = occupied
        self.fields[row, col].can_be_occupied = not occupied
        self.fields[row, col].player = player if occupied else None

    def place_horizontal_wall(self, row, col, occupied):
        """Update the occupation status of a horizontal wall position."""
        if self.horizontal_wall_slots.is_in_bounds(row, col):
            if occupied:
                self.horizontal_wall_slots[row, col].occupied = True
                self.horizontal_wall_slots[row, col].can_be_occupied = False

                # Update adjacent horizontal wall
                if col > 0:
                    self.horizontal_wall_slots[row, col - 1].can_be_occupied = False
                if col < 8:
                    self.horizontal_wall_slots[row, col + 1].can_be_occupied = False

                # Update overlapping vertical walls
                if row < 9:
                    self.vertical_wall_slots[row, col].can_be_occupied = False
                if col < 8 and row < 9:
                    self.vertical_wall_slots[row, col + 1].can_be_occupied = False
            else:
                self.horizontal_wall_slots[row, col].occupied = False

    def place_vertical_wall(self, row, col, occupied):
        """Update the occupation status of a vertical wall position."""
        if self.vertical_wall_slots.is_in_bounds(row, col):
            if occupied:
                self.vertical_wall_slots[row, col].occupied = True
                self.vertical_wall_slots[row, col].can_be_occupied = False

                # Update adjacent vertical wall
                if row > 0:
                    self.vertical_wall_slots[row - 1, col].can_be_occupied = False
                if row < 8:
                    self.vertical_wall_slots[row + 1, col].can_be_occupied = False

                # Update overlapping horizontal walls
                if col < 9:
                    self.horizontal_wall_slots[row, col].can_be_occupied = False
                if row < 8 and col < 9:
                    self.horizontal_wall_slots[row + 1, col].can_be_occupied = False
            else:
                self.vertical_wall_slots[row, col].occupied = False

    def print_board(self):
        """Print the current state of the board (for debugging)."""
        print("Player Positions:")
        for row in self.fields.data:
            print([["P" + str(cell.player) if cell.occupied else "-" for cell in row]])

        print("\nHorizontal Walls:")
        for row in self.horizontal_wall_slots.data:
            print([["H" if cell.occupied else "-" for cell in row]])

        print("\nVertical Walls:")
        for row in self.vertical_wall_slots.data:
            print([["V" if cell.occupied else "-" for cell in row]])

# Example usage:
if __name__ == "__main__":
    board = Board()
    board.update_player_position(0, 0, True, player=1)
    board.place_horizontal_wall(1, 1, True)
    board.place_vertical_wall(1, 1, True)
    board.print_board()
