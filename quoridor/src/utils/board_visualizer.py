from quoridor.src.board import Board
from quoridor.src.utils.types import Position

class BoardVisualizer:
    def __init__(self, board: Board):
        self.board = board

    def print_occupied_fields(self):
        """Print the positions of all occupied fields in a formatted grid."""
        print("\nBoard State:")
        print("  " + " ".join(f"{i}" for i in range(self.board.board_width)))
        print("  " + "-" * (self.board.board_width * 2 - 1))
        
        for row in range(self.board.board_width):
            row_str = f"{row}|"
            for col in range(self.board.board_width):
                position = Position(row, col)
                field = self.board.fields[position]
                if field is not None and field.pawn is not None:
                    row_str += f"{field.pawn.id} "
                else:
                    row_str += ". "
            print(row_str.rstrip())
        print()

    def print_walls(self):
        """Print the positions of all placed walls in a single formatted grid."""
        print("\nWall Positions:")
        print("  " + " ".join(f"{i}" for i in range(self.board.board_width)))
        print("  " + "-" * (self.board.board_width * 2 - 1))
        
        for row in range(self.board.board_width):
            row_str = f"{row}|"
            for col in range(self.board.board_width):
                position = Position(row, col)
                # Check for horizontal wall
                has_horizontal = (row < self.board.board_width - 1 and 
                                self.board.horizontal_wall_slots.is_in_bounds(position) and 
                                self.board.horizontal_wall_slots[position].occupied)
                # Check for vertical wall
                has_vertical = (col < self.board.board_width - 1 and 
                            self.board.vertical_wall_slots.is_in_bounds(position) and 
                            self.board.vertical_wall_slots[position].occupied)
                
                if has_horizontal and has_vertical:
                    row_str += "╬ "  # Intersection of horizontal and vertical walls
                elif has_horizontal:
                    row_str += "═ "  # Horizontal wall
                elif has_vertical:
                    row_str += "║ "  # Vertical wall
                else:
                    row_str += ". "
            print(row_str.rstrip())
        print()