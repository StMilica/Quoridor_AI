import pytest
from quoridor.src.board import Board

@pytest.fixture
def board():
    return Board()

def test_initial_state(board):
    """Test the initial state of the board."""
    for row in board.player_positions:
        for cell in row:
            assert not cell["occupied"]
            assert cell["can_be_occupied"]
            assert cell["player"] is None

    for row in board.horizontal_walls:
        for cell in row:
            assert not cell["occupied"]
            assert cell["can_be_occupied"]

    for row in board.vertical_walls:
        for cell in row:
            assert not cell["occupied"]
            assert cell["can_be_occupied"]

def test_player_position(board):
    """Test updating player positions."""
    board.update_player_position(0, 0, True, player=1)
    assert board.player_positions[0][0]["occupied"]
    assert not board.player_positions[0][0]["can_be_occupied"]
    assert board.player_positions[0][0]["player"] == 1

    board.update_player_position(0, 0, False)
    assert not board.player_positions[0][0]["occupied"]
    assert board.player_positions[0][0]["can_be_occupied"]
    assert board.player_positions[0][0]["player"] is None

def test_horizontal_wall(board):
    """Test placing horizontal walls and their effects."""
    board.update_horizontal_wall(1, 1, True)
    assert board.horizontal_walls[1][1]["occupied"]
    assert not board.horizontal_walls[1][1]["can_be_occupied"]

    # Adjacent horizontal walls should not be occupiable
    assert not board.horizontal_walls[1][0]["can_be_occupied"]
    assert not board.horizontal_walls[1][2]["can_be_occupied"]

    # Overlapping vertical walls should not be occupiable
    assert not board.vertical_walls[1][1]["can_be_occupied"]
    assert not board.vertical_walls[1][2]["can_be_occupied"]

def test_vertical_wall(board):
    """Test placing vertical walls and their effects."""
    board.update_vertical_wall(1, 1, True)
    assert board.vertical_walls[1][1]["occupied"]
    assert not board.vertical_walls[1][1]["can_be_occupied"]

    # Adjacent vertical walls should not be occupiable
    assert not board.vertical_walls[0][1]["can_be_occupied"]
    assert not board.vertical_walls[2][1]["can_be_occupied"]

    # Overlapping horizontal walls should not be occupiable
    assert not board.horizontal_walls[1][1]["can_be_occupied"]
    assert not board.horizontal_walls[2][1]["can_be_occupied"]

def test_validate_position(board):
    with pytest.raises(ValueError):
        board._validate_position(-1, 0, 9, 9)

    with pytest.raises(ValueError):
        board._validate_position(9, 9, 8, 9)

# def test_invalid_positions(board):
#     """Test handling of invalid positions."""
#     with pytest.raises(ValueError):
#         board.update_player_position(-1, 0, True, player=1)

#     with pytest.raises(ValueError):
#         board.update_horizontal_wall(8, 9, True)

#     with pytest.raises(ValueError):
#         board.update_vertical_wall(9, 8, True)

if __name__ == "__main__":
    pytest.main()
