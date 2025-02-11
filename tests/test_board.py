import pytest
from quoridor.src.board import Board
from quoridor.src.utils.types import Position, WallOrientation

@pytest.fixture
def board():
    """Create a new board instance for each test."""
    board = Board()
    # Ensure pawns are properly initialized
    assert board.fields[board.pawn1.position].pawn == board.pawn1
    assert board.fields[board.pawn2.position].pawn == board.pawn2
    return board

def test_initial_pawn_positions(board):
    """Test initial pawn positions and field occupation."""
    assert board.pawn1.position == Position(0, 4)
    assert board.pawn2.position == Position(8, 4)
    assert board.fields[Position(0, 4)].pawn == board.pawn1
    assert board.fields[Position(8, 4)].pawn == board.pawn2

def test_valid_pawn_move(board):
    """Test valid pawn movement and field updates."""
    old_position = board.pawn1.position
    new_position = Position(1, 4)
    board.move_pawn(board.pawn1, new_position)
    
    # Check pawn position is updated
    assert board.pawn1.position == new_position
    # Check fields are properly updated
    assert board.fields[old_position].pawn is None
    assert board.fields[new_position].pawn == board.pawn1

@pytest.mark.parametrize("position", [
    Position(-1, 4),  # Negative row
    Position(9, 4),   # Row out of bounds
    Position(4, -1),  # Negative column
    Position(4, 9)    # Column out of bounds
])
def test_invalid_pawn_move_out_of_bounds(board, position):
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, position)

def test_invalid_pawn_move_occupied(board):
    """Test that a pawn cannot move to an occupied position."""
    new_position = Position(8, 4)  # Position occupied by pawn2
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, new_position)

@pytest.mark.parametrize("orientation, position", [
    (WallOrientation.HORIZONTAL, Position(-1, 0)),    # Invalid row for horizontal
    (WallOrientation.HORIZONTAL, Position(8, 0)),     # Invalid row for horizontal (max is 7)
    (WallOrientation.VERTICAL, Position(0, -1)),      # Invalid column for vertical
    (WallOrientation.VERTICAL, Position(0, 8)),       # Invalid column for vertical (max is 7)
])
def test_invalid_wall_placement_out_of_bounds(board, orientation, position):
    """Test that placing walls out of bounds raises IndexError."""
    with pytest.raises(IndexError):
        board.place_wall(orientation, position)

def test_invalid_wall_placement_overlap(board):
    """Test that walls cannot overlap."""
    position = Position(4, 4)
    board.place_wall(WallOrientation.HORIZONTAL, position)
    with pytest.raises(ValueError):
        board.place_wall(WallOrientation.HORIZONTAL, position)

def test_pawn_jump_over_adjacent_pawn(board):
    """Test pawn jumping mechanics."""
    # Move pawn2 up to create a jumping scenario
    intermediate_positions = [Position(7, 4), Position(6, 4), Position(5, 4),
                            Position(4, 4), Position(3, 4), Position(2, 4)]
    
    for pos in intermediate_positions:
        board.move_pawn(board.pawn2, pos)
    
    # Move pawn1 down to be adjacent to pawn2
    board.move_pawn(board.pawn1, Position(1, 4))
    
    # Test jumping over
    jump_position = Position(3, 4)
    board.move_pawn(board.pawn1, jump_position)
    assert board.pawn1.position == jump_position
    assert board.fields[jump_position].pawn == board.pawn1

def test_blocked_jump_movement(board):
    """Test movement options when jump is blocked by wall."""
    # Setup pawns - first move pawn2 up from (8,4) to (2,4)
    intermediate_positions = [
        Position(7, 4),
        Position(6, 4),
        Position(5, 4),
        Position(4, 4),
        Position(3, 4),
        Position(2, 4)
    ]
    
    for pos in intermediate_positions:
        board.move_pawn(board.pawn2, pos)
    
    # Move pawn1 down from (0,4) to (1,4)
    board.move_pawn(board.pawn1, Position(1, 4))
    
    # Place blocking wall
    board.place_wall(WallOrientation.HORIZONTAL, Position(2, 4))
    
    # Test blocked forward jump
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, Position(3, 4))
    
    # Test valid sideways movements
    board.move_pawn(board.pawn1, Position(1, 3))  # Move left
    assert board.pawn1.position == Position(1, 3)
    
    board.move_pawn(board.pawn1, Position(1, 4))  # Move back
    board.move_pawn(board.pawn1, Position(1, 5))  # Move right
    assert board.pawn1.position == Position(1, 5)

def test_diagonal_moves_prohibited(board):
    """Test that diagonal moves are not allowed."""
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, Position(1, 5))  # Diagonal move

