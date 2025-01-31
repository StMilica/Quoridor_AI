import pytest
from quoridor.src.board import Board, Position, WallOrientation

@pytest.fixture
def board():
    return Board()

def test_initial_pawn_positions(board):
    assert board.pawn1.position == Position(0, 4)
    assert board.pawn2.position == Position(8, 4)

def test_valid_pawn_move(board):
    new_position = Position(1, 4)
    board.move_pawn(board.pawn1, new_position)
    assert board.pawn1.position == new_position

def test_invalid_pawn_move_out_of_bounds(board):
    new_position = Position(-1, 4)
    with pytest.raises(IndexError):
        board.move_pawn(board.pawn1, new_position)

def test_invalid_pawn_move_occupied(board):
    new_position = Position(8, 4)
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, new_position)

def test_valid_wall_placement_horizontal(board):
    position = Position(4, 4)
    board.place_wall(WallOrientation.HORIZONTAL, position)
    assert board.horizontal_wall_slots[position].occupied

def test_valid_wall_placement_vertical(board):
    position = Position(5, 5)
    board.place_wall(WallOrientation.VERTICAL, position)
    assert board.vertical_wall_slots[position].occupied

def test_invalid_wall_placement_overlap(board):
    position = Position(4, 4)
    board.place_wall(WallOrientation.HORIZONTAL, position)
    with pytest.raises(ValueError):
        board.place_wall(WallOrientation.HORIZONTAL, position)

def test_invalid_wall_placement_block_path(board):
    # Assuming is_path_blocked is implemented
    position = Position(4, 4)
    board.place_wall(WallOrientation.HORIZONTAL, position)
    with pytest.raises(ValueError):
        board.place_wall(WallOrientation.VERTICAL, Position(4, 5))

def test_pawn_jump_over_adjacent_pawn(board):
    # Move pawn2 to the position where it will be adjacent to pawn1
    board.move_pawn(board.pawn2, Position(7, 4))
    board.move_pawn(board.pawn2, Position(6, 4))
    board.move_pawn(board.pawn2, Position(5, 4))
    board.move_pawn(board.pawn2, Position(4, 4))
    board.move_pawn(board.pawn2, Position(3, 4))
    board.move_pawn(board.pawn2, Position(2, 4))

    # Move pawn1 to the position where it will be adjacent to pawn2
    board.move_pawn(board.pawn1, Position(1, 4))

    # Test jump over pawn2
    board.move_pawn(board.pawn1, Position(3, 4))
    assert board.pawn1.position == Position(3, 4)

    # Test blocked jump
    board.place_wall(WallOrientation.HORIZONTAL, Position(2, 4))
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, Position(4, 4))

    # Test left move when jump is blocked
    board.move_pawn(board.pawn1, Position(2, 3))
    assert board.pawn1.position == Position(2, 3)

    # Test right move when jump is blocked
    board.move_pawn(board.pawn1, Position(2, 4))
    board.move_pawn(board.pawn1, Position(2, 5))
    assert board.pawn1.position == Position(2, 5)

    # Test that diagonal move is prohibited in all other cases
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, Position(3, 5))
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, Position(1, 5))

def test_pawn_jump_blocked_by_wall(board):
    board.move_pawn(board.pawn1, Position(1, 4))
    board.move_pawn(board.pawn2, Position(2, 4))
    board.place_wall(WallOrientation.HORIZONTAL, Position(2, 4))
    with pytest.raises(ValueError):
        board.move_pawn(board.pawn1, Position(3, 4))

def test_pawn_move_left_right_when_jump_blocked(board):
    board.move_pawn(board.pawn1, Position(1, 4))
    board.move_pawn(board.pawn2, Position(2, 4))
    board.place_wall(WallOrientation.HORIZONTAL, Position(2, 4))
    board.move_pawn(board.pawn1, Position(2, 3))
    assert board.pawn1.position == Position(2, 3)

def test_wall_placement_on_board_edges(board):
    position = Position(0, 0)
    board.place_wall(WallOrientation.HORIZONTAL, position)
    assert board.horizontal_wall_slots[position].occupied

    position = Position(0, 0)
    board.place_wall(WallOrientation.VERTICAL, position)
    assert board.vertical_wall_slots[position].occupied

def test_wall_placement_out_of_bounds(board):
    position = Position(-1, 0)
    with pytest.raises(ValueError):
        board.place_wall(WallOrientation.HORIZONTAL, position)

    position = Position(0, -1)
    with pytest.raises(ValueError):
        board.place_wall(WallOrientation.VERTICAL, position)

