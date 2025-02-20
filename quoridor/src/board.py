from enum import Enum
from quoridor.src.utils.types import Direction, Position, Matrix, WallOrientation, WallSlotPosition
from abc import ABC, abstractmethod
from collections import deque

# Types

class Pawn:
    def __init__(self, id, position):
        self.id = id
        self.position = position
    
    def desired_direction(self):
        return Direction.UP if self.id == 1 else Direction.DOWN

class Wall:
    def __init__(self, orientation, position):
        self.orientation = orientation
        self.position = position

class Field:
    def __init__(self, pawn=None):
        self.pawn = pawn
    
    def is_occupied(self):
        return self.pawn is not None

class WallSlot:
    def __init__(self, occupied=False, can_be_occupied=True):
        self.occupied = occupied
        self.can_be_occupied = can_be_occupied
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

        self.fields = Matrix(self.board_width, self.board_width, lambda: Field())
        self.horizontal_wall_slots = Matrix(self.board_width - 1, self.board_width, lambda: WallSlot())
        self.vertical_wall_slots = Matrix(self.board_width, self.board_width - 1, lambda: WallSlot())

        # Initialize the fields with the initial pawn positions
        self.fields[self.pawn1.position].pawn = self.pawn1
        self.fields[self.pawn2.position].pawn = self.pawn2


    def move_pawn(self, pawn, new_position):
        """Move a pawn to a new position."""
        valid_moves = self.get_all_valid_pawn_moves(pawn)
        if new_position not in valid_moves:
            raise ValueError("Invalid move")
        
        # Clear the old position
        self.fields[pawn.position].pawn = None
        
        # Move the pawn to the new position
        self.fields[new_position].pawn = pawn
        pawn.position = new_position
        
    def can_pass_between_adjacent_positions(self, start_position: Position, end_position: Position) -> bool:
        """Check if there are walls between two adjacent positions - Must be adjacent positions, otherwise will raise an error."""
        direction = Direction.from_positions(start_position, end_position)
        wall_orientation = WallOrientation.from_direction(direction)
        wall_slot_positions = direction.wall_slot_positions()
        wall_slots = self.get_surrounding_wall_slots(start_position, wall_orientation, wall_slot_positions)
        return not any([wall_slot.occupied for wall_slot in wall_slots if wall_slot is not None])

        
    def get_all_valid_pawn_moves(self, pawn):
        """Get all valid moves for a pawn."""
        valid_moves = []

        for direction in Direction.all_directions():
            new_position = pawn.position + direction.value
            if self.fields.is_in_bounds(new_position):
                if self.can_pass_between_adjacent_positions(pawn.position, new_position):
                    if not self.fields[new_position].is_occupied():
                        valid_moves.append(new_position)
                    else:
                        jump_over_position = new_position + direction.value
                        if self.fields.is_in_bounds(jump_over_position):
                            if self.can_pass_between_adjacent_positions(new_position, jump_over_position):
                                # Jump over it there isn't a wall behind and the position is in bounds
                                valid_moves.append(jump_over_position)
                            else:
                                # Check if the pawn can move to perpendicular directions
                                for perpendicular_direction in direction.perpendicular_directions():
                                    perpendicular_position = new_position + perpendicular_direction.value
                                    if self.fields.is_in_bounds(perpendicular_position) and self.can_pass_between_adjacent_positions(new_position, perpendicular_position):
                                        valid_moves.append(perpendicular_position)

                        elif pawn.desired_direction() == direction and not self.fields.is_in_bounds(jump_over_position):
                            # Jumping over the pawn wins the game
                            valid_moves.append(jump_over_position)
                            print("Victory, pawn jumps over the oponent pawn over the edge of the board")
                            # TODO: Handle it any way you want within the game logic!
        
        # If valid moves are empty, the pawn is blocked, this is an edge case that needs to be solved by the game logic
        # In some cases raise an error, in other cases allow for a diagonal or any other kind of jump that needs to be checked properly and handled as a custom edge case.
        # But he should either win the game or be able to move forward, there are no other options.
        if not valid_moves:
            # TODO: Handle the jump over for a specific edge case that happens here, or declare a win game!
            print("Pawn is blocked, handle it as a custom edge case or declare victory")
            raise ValueError("Pawn is blocked")
    
        return valid_moves

        

    def place_wall(self, orientation, position):
        """Place a wall at a given position."""
        if not self.can_place_wall_at_position(orientation, position):
            raise ValueError("Cannot place wall at this position")
        if orientation == WallOrientation.HORIZONTAL:
            self.horizontal_wall_slots[position].occupied = True
            next_adjacent_position = Position(position.row, position.col + 1)
            if self.horizontal_wall_slots.is_in_bounds(next_adjacent_position):
                self.horizontal_wall_slots[next_adjacent_position].can_be_occupied = False
            self.vertical_wall_slots[position].can_be_occupied = False

        elif orientation == WallOrientation.VERTICAL:
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
                and not self.horizontal_wall_slots[adjacent_horizontal_slot_position].occupied
                and not self.vertical_wall_slots[position].occupied
            )
        
        elif orientation == WallOrientation.VERTICAL:
            adjacent_vertical_slot_position = Position(position.row + 1, position.col)
            return (
                not self.vertical_wall_slots[position].occupied
                and self.vertical_wall_slots[position].can_be_occupied
                and not self.vertical_wall_slots[adjacent_vertical_slot_position].occupied
                and not self.horizontal_wall_slots[position].occupied
            )

    def is_path_blocked(self, start_position, target_row):
        """
        Check if a path exists from start_position to the target row.
        
        Args:
            start_position (Position): Starting position
            target_row (int): Target row to reach
            
        Returns:
            bool: True if path is blocked, False if path exists
        """
        directions = [
            (0, 1),   # right
            (1, 0),   # down
            (0, -1),  # left
            (-1, 0)   # up
        ]

        visited = set()
        queue = deque([start_position])
        visited.add(start_position)

        while queue:
            current_position = queue.popleft()
            
            # Check if we've reached the target row
            if current_position.row == target_row:
                return False  # Path exists

            for direction in directions:
                new_row = current_position.row + direction[0]
                new_col = current_position.col + direction[1]
                new_position = Position(new_row, new_col)

                if (not self.fields.is_in_bounds(new_position) or 
                    new_position in visited or 
                    not self.can_pass_between_adjacent_positions(current_position, new_position)):
                    continue

                visited.add(new_position)
                queue.append(new_position)

        return True  # No path exists
    
    def get_surrounding_wall_slots(self, position, orientation, wall_slot_positions: list[WallSlotPosition]):
        wall_slots = []
        for wall_slot_position in wall_slot_positions:
            wall_slots.append(self.get_surrounding_wall_slot(position, orientation, wall_slot_position))
        return wall_slots
    
    def get_surrounding_wall_slot(self, position, orientation, wall_slot_position: WallSlotPosition):
        if wall_slot_position == WallSlotPosition.UP_LEFT:
            wsp = Position(row=position.row - 1, col=position.col - 1)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            elif orientation == WallOrientation.VERTICAL and self.vertical_wall_slots.is_in_bounds(wsp):
                return self.vertical_wall_slots[wsp]
            else:
                return None
        
        if wall_slot_position == WallSlotPosition.UP_RIGHT:
            wsp = Position(row=position.row - 1, col=position.col)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            elif orientation == WallOrientation.VERTICAL and self.vertical_wall_slots.is_in_bounds(wsp):
                return self.vertical_wall_slots[wsp]
            else:
                return None
        
        if wall_slot_position == WallSlotPosition.DOWN_LEFT:
            wsp = Position(row=position.row, col=position.col - 1)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            elif orientation == WallOrientation.VERTICAL and self.vertical_wall_slots.is_in_bounds(wsp):
                return self.vertical_wall_slots[wsp]
            else:
                return None
        
        if wall_slot_position == WallSlotPosition.DOWN_RIGHT:
            wsp = Position(row=position.row, col=position.col)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            elif orientation == WallOrientation.VERTICAL and self.vertical_wall_slots.is_in_bounds(wsp):
                return self.vertical_wall_slots[wsp]
            else:
                return None
            
    def get_occupied_fields(self) -> list[Position]:
        """Return a list of positions occupied by pawns."""
        occupied_fields = []
        for row in range(self.board_width):
            for col in range(self.board_width):
                position = Position(row, col)
                field = self.fields[position]
                if field is not None and field.pawn is not None:
                    occupied_fields.append(position)
        return occupied_fields
            

# Example usage:

if __name__ == "__main__":
    from quoridor.src.utils.board_visualizer import BoardVisualizer
    
    board = Board()
    visualizer = BoardVisualizer(board)

    # Place a horizontal wall
    wall_position_horizontal = Position(5, 4)
    board.place_wall(WallOrientation.HORIZONTAL, wall_position_horizontal)
    print(f"Horizontal wall placed at {wall_position_horizontal}")
    visualizer.print_walls()

    # Place a vertical wall
    wall_position_vertical = Position(4, 4)
    board.place_wall(WallOrientation.VERTICAL, wall_position_vertical)
    print(f"Vertical wall placed at {wall_position_vertical}")
    visualizer.print_walls()