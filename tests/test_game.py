from quoridor.src.board import Board
from quoridor.src.player import Player

def test_place_wall():
    board = Board()
    assert board.place_wall("horizontal", (4, 4), {}) is True
    assert board.place_wall("horizontal", (4, 4), {}) is False  # Cannot place a duplicate wall

def test_is_within_bounds():
    board = Board()
    assert board.is_within_bounds((4, 4)) is True
    assert board.is_within_bounds((9, 4)) is False

def test_path_validation():
    board = Board()
    players = {
        "Player 1": Player("Player 1", (0, 4), 8),
        "Player 2": Player("Player 2", (8, 4), 0),
    }
    assert board.place_wall("horizontal", (4, 4), players) is True
    assert board.place_wall("horizontal", (4, 5), players) is True
    # Adding a blocking wall should return False
    # assert board.place_wall("horizontal", (4, 6), players) is False
