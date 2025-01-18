class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

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
        # 9x9 grid for player positions
        self.player_positions = [
            [Field() for _ in range(9)]
            for _ in range(9)
        ]

        # 8x9 grid for horizontal walls
        self.horizontal_walls = [
            [WallSlot() for _ in range(9)]
            for _ in range(8)
        ]

        # 9x8 grid for vertical walls
        self.vertical_walls = [
            [WallSlot() for _ in range(8)]
            for _ in range(9)
        ]

    def _validate_position(self, row, col, max_rows, max_cols):
        if not (0 <= row < max_rows and 0 <= col < max_cols):
            raise ValueError(f"Invalid position: ({row}, {col})")

    def update_player_position(self, row, col, occupied, player=None):
        self._validate_position(row, col, 9, 9)
        self.player_positions[row][col].occupied = occupied
        self.player_positions[row][col].can_be_occupied = not occupied
        self.player_positions[row][col].player = player if occupied else None

    def place_horizontal_wall(self, row, col, occupied):
        """Update the occupation status of a horizontal wall position."""
        if 0 <= row < 8 and 0 <= col < 9:
            if occupied:
                self.horizontal_walls[row][col].occupied = True
                self.horizontal_walls[row][col].can_be_occupied = False

                # Update adjacent horizontal wall
                if col > 0:
                    self.horizontal_walls[row][col - 1].can_be_occupied = False
                if col < 8:
                    self.horizontal_walls[row][col + 1].can_be_occupied = False

                # Update overlapping vertical walls
                if row < 9:
                    self.vertical_walls[row][col].can_be_occupied = False
                if col < 8 and row < 9:
                    self.vertical_walls[row][col + 1].can_be_occupied = False
            else:
                self.horizontal_walls[row][col].occupied = False

    def place_vertical_wall(self, row, col, occupied):
        """Update the occupation status of a vertical wall position."""
        if 0 <= row < 9 and 0 <= col < 8:
            if occupied:
                self.vertical_walls[row][col].occupied = True
                self.vertical_walls[row][col].can_be_occupied = False

                # Update adjacent vertical wall
                if row > 0:
                    self.vertical_walls[row - 1][col].can_be_occupied = False
                if row < 8:
                    self.vertical_walls[row + 1][col].can_be_occupied = False

                # Update overlapping horizontal walls
                if col < 9:
                    self.horizontal_walls[row][col].can_be_occupied = False
                if row < 8 and col < 9:
                    self.horizontal_walls[row + 1][col].can_be_occupied = False
            else:
                self.vertical_walls[row][col].occupied = False

    def print_board(self):
        """Print the current state of the board (for debugging)."""
        print("Player Positions:")
        for row in self.player_positions:
            print([["P" + str(cell.player) if cell.occupied else "-" for cell in row]])

        print("\nHorizontal Walls:")
        for row in self.horizontal_walls:
            print([["H" if cell.occupied else "-" for cell in row]])

        print("\nVertical Walls:")
        for row in self.vertical_walls:
            print([["V" if cell.occupied else "-" for cell in row]])

# Example usage:
if __name__ == "__main__":
    board = Board()
    board.update_player_position(0, 0, True, player=1)
    board.place_horizontal_wall(1, 1, True)
    board.place_vertical_wall(1, 1, True)
    board.print_board()
