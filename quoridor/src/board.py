from enum import Enum
from .utils.types import Direction, Position, Matrix, WallSlotPosition
from abc import ABC, abstractmethod
from collections import deque

# Types

class WallOrientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

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

        self.fields = Matrix(self.board_width, self.board_width, Field())
        self.horizontal_wall_slots = Matrix(self.board_width - 1, self.board_width, WallSlot())
        self.vertical_wall_slots = Matrix(self.board_width, self.board_width - 1, WallSlot())

    def move_pawn(self, pawn, new_position):
        """Move a pawn to a new position."""
        if not self.is_valid_pawn_move(pawn.position, new_position):
            raise ValueError("Invalid move")
        self.fields.move_item(pawn.position, new_position)
        pawn.position = new_position
        
    def can_pass_between_adjacent_positions(self, start_position: Position, end_position: Position) -> bool:
        """Check if there are walls between two adjacent positions - Must be adjacent positions, otherwise will raise an error."""
        direction = Direction.from_positions(start_position, end_position)
        # UP
        if direction == Direction.UP:
            wall_slots = self.get_surrounding_wall_slots(start_position, WallOrientation.HORIZONTAL, [WallSlotPosition.UP_LEFT, WallSlotPosition.UP_RIGHT])
            return any([wall_slot.occupied for wall_slot in wall_slots])
        # DOWN
        if direction == Direction.DOWN:
            wall_slots = self.get_surrounding_wall_slots(start_position, WallOrientation.HORIZONTAL, [WallSlotPosition.DOWN_LEFT, WallSlotPosition.DOWN_RIGHT])
            return any([wall_slot.occupied for wall_slot in wall_slots])
        # LEFT
        if direction == Direction.LEFT:
            wall_slots = self.get_surrounding_wall_slots(start_position, WallOrientation.VERTICAL, [WallSlotPosition.UP_LEFT, WallSlotPosition.DOWN_LEFT])
            return any([wall_slot.occupied for wall_slot in wall_slots])
        # RIGHT
        if direction == Direction.RIGHT:
            wall_slots = self.get_surrounding_wall_slots(start_position, WallOrientation.VERTICAL, [WallSlotPosition.UP_RIGHT, WallSlotPosition.DOWN_RIGHT])
            return any([wall_slot.occupied for wall_slot in wall_slots])
        
    def get_all_valid_pawn_moves(self, pawn):
        """Get all valid moves for a pawn."""
        valid_moves = []        
        # UP
        up_position = pawn.position + Direction.UP
        if self.fields.is_in_bounds(up_position) and self.can_pass_between_adjacent_positions(pawn.position, up_position):
            if not self.fields[up_position].is_occupied():
                valid_moves.append(up_position)
            else: 
                # Jump over the pawn
                # IF there is a wall behind the pawn, the jump is not possible
                jump_over_position = up_position + Direction.UP
                if self.fields.is_in_bounds(jump_over_position) and self.can_pass_between_adjacent_positions(up_position, jump_over_position):
                    valid_moves.append(jump_over_position)
                elif self.fields.is_in_bounds(jump_over_position):
                    # If there is a wall behind the pawn, check if the pawn can move to the left or right
                    # LEFT
                    left_position = up_position + Direction.LEFT
                    if self.fields.is_in_bounds(left_position) and self.can_pass_between_adjacent_positions(up_position, left_position):
                        valid_moves.append(left_position)
                    # RIGHT
                    right_position = up_position + Direction.RIGHT
                    if self.fields.is_in_bounds(right_position) and self.can_pass_between_adjacent_positions(up_position, right_position):
                        valid_moves.append(right_position)
                else:
                    if pawn.desired_direction() == Direction.UP:
                        valid_moves.append(jump_over_position)
                        print("Victory, pawn jumped over the other pawn")
                        # TODO: Handle it any way you want within the game logic!
        
        # DOWN
        down_position = pawn.position + Direction.DOWN
        if self.fields.is_in_bounds(down_position) and self.can_pass_between_adjacent_positions(pawn.position, down_position):
            if not self.fields[down_position].is_occupied():
                valid_moves.append(down_position)
            else: 
                # Jump over the pawn
                # IF there is a wall behind the pawn, the jump is not possible
                jump_over_position = down_position + Direction.DOWN
                if self.fields.is_in_bounds(jump_over_position) and self.can_pass_between_adjacent_positions(down_position, jump_over_position):
                    valid_moves.append(jump_over_position)
                elif self.fields.is_in_bounds(jump_over_position):
                    # If there is a wall behind the pawn, check if the pawn can move to the left or right
                    # LEFT
                    left_position = down_position + Direction.LEFT
                    if self.fields.is_in_bounds(left_position) and self.can_pass_between_adjacent_positions(down_position, left_position):
                        valid_moves.append(left_position)
                    # RIGHT
                    right_position = down_position + Direction.RIGHT
                    if self.fields.is_in_bounds(right_position) and self.can_pass_between_adjacent_positions(down_position, right_position):
                        valid_moves.append(right_position)
                else:
                    if pawn.desired_direction() == Direction.DOWN:
                        valid_moves.append(jump_over_position)
                        print("Victory, pawn jumped over the other pawn")
                        # TODO: Handle it any way you want within the game logic!
                        
        # LEFT
        left_position = pawn.position + Direction.LEFT
        if self.fields.is_in_bounds(left_position) and self.can_pass_between_adjacent_positions(pawn.position, left_position):
            if not self.fields[left_position].is_occupied():
                valid_moves.append(left_position)
            else: 
                # Jump over the pawn
                # IF there is a wall behind the pawn, the jump is not possible
                jump_over_position = left_position + Direction.LEFT
                if self.fields.is_in_bounds(jump_over_position) and self.can_pass_between_adjacent_positions(left_position, jump_over_position):
                    valid_moves.append(jump_over_position)
                else:
                    # If there is a wall behind the pawn, check if the pawn can move to the left or right
                    # UP
                    up_position = left_position + Direction.UP
                    if self.fields.is_in_bounds(up_position) and self.can_pass_between_adjacent_positions(left_position, up_position):
                        valid_moves.append(up_position)
                    # DOWN
                    down_position = left_position + Direction.DOWN
                    if self.fields.is_in_bounds(down_position) and self.can_pass_between_adjacent_positions(left_position, down_position):
                        valid_moves.append(down_position)
                        
        # RIGHT
        right_position = pawn.position + Direction.RIGHT
        if self.fields.is_in_bounds(right_position) and self.can_pass_between_adjacent_positions(pawn.position, right_position):
            if not self.fields[right_position].is_occupied():
                valid_moves.append(right_position)
            else: 
                # Jump over the pawn
                # IF there is a wall behind the pawn, the jump is not possible
                jump_over_position = right_position + Direction.RIGHT
                if self.fields.is_in_bounds(jump_over_position) and self.can_pass_between_adjacent_positions(right_position, jump_over_position):
                    valid_moves.append(jump_over_position)
                else:
                    # If there is a wall behind the pawn, check if the pawn can move to the left or right
                    # UP
                    up_position = right_position + Direction.UP
                    if self.fields.is_in_bounds(up_position) and self.can_pass_between_adjacent_positions(right_position, up_position):
                        valid_moves.append(up_position)
                    # DOWN
                    down_position = right_position + Direction.DOWN
                    if self.fields.is_in_bounds(down_position) and self.can_pass_between_adjacent_positions(right_position, down_position):
                        valid_moves.append(down_position)
            

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
                and self.horizontal_wall_slots[adjacent_horizontal_slot_position].can_be_occupied
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

    def is_path_blocked(self, start_position, end_position):
        """Check if a path is blocked by walls using BFS."""
        directions = [
            (0, 1),  # right
            (1, 0),  # down
            (0, -1), # left
            (-1, 0)  # up
        ]

        visited = set()
        queue = deque([start_position])

        while queue:
            current_position = queue.popleft()
            if current_position == end_position:
                return False  # Path is not blocked

            for direction in directions:
                new_row = current_position.row + direction[0]
                new_col = current_position.col + direction[1]
                new_position = Position(new_row, new_col)

                if not self.fields.is_in_bounds(new_position):
                    continue

                if new_position in visited:
                    continue

                if not self.is_valid_move(current_position, new_position):
                    continue

                visited.add(new_position)
                queue.append(new_position)

        return True  # Path is blocked
    
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
            return self.vertical_wall_slots[wsp]
        
        if wall_slot_position == WallSlotPosition.UP_RIGHT:
            wsp = Position(row=position.row - 1, col=position.col)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            return self.vertical_wall_slots[wsp]
        
        if wall_slot_position == WallSlotPosition.DOWN_LEFT:
            wsp = Position(row=position.row, col=position.col - 1)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            return self.vertical_wall_slots[wsp]
        
        if wall_slot_position == WallSlotPosition.DOWN_RIGHT:
            wsp = Position(row=position.row, col=position.col)
            if orientation == WallOrientation.HORIZONTAL and self.horizontal_wall_slots.is_in_bounds(wsp):
                return self.horizontal_wall_slots[wsp]
            return self.vertical_wall_slots[wsp]
        
        

            

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