import pytest
from quoridor.src.game import Game, GameState
from quoridor.src.utils.types import Position, WallOrientation

def test_game_initialization():
    game = Game()
    assert game.get_current_player() == 1
    assert game.get_walls_remaining(1) == 10
    assert game.get_walls_remaining(2) == 10
    assert not game.is_game_over()

def test_player1_wins():
    game = Game()
    # Move player 1 to the opposite edge, with player 2 moving back and forth
    for row in range(1, 9):
        # Player 1's turn - moving towards goal
        assert game.move_pawn(Position(row, 4))
        
        if row < 8:
            # Player 2's turn - moving between two positions
            if row % 2 == 0:
                assert game.move_pawn(Position(7, 3))
            else:
                assert game.move_pawn(Position(8, 3))
    
    assert game.is_game_over()
    assert game.get_winner() == 1

def test_wall_placement():
    game = Game()
    assert game.place_wall(WallOrientation.HORIZONTAL, Position(4, 4))
    assert game.get_walls_remaining(1) == 9
    assert game.get_current_player() == 2

def test_path_blocked_flag():
    game = Game()
    # Place walls to create a blocking situation
    assert game.place_wall(WallOrientation.HORIZONTAL, Position(1, 3))
    assert game.place_wall(WallOrientation.VERTICAL, Position(0, 3))
    assert game.place_wall(WallOrientation.VERTICAL, Position(0, 5))
    # This wall would block player 1's path
    assert not game.place_wall(WallOrientation.HORIZONTAL, Position(1, 4))
    assert game.get_walls_remaining(2) == 9  # Wall should not be placed

def test_get_valid_moves():
    game = Game()
    # Get initial valid moves for player 1
    valid_moves = game.get_valid_moves()
    assert Position(1, 4) in valid_moves
    assert len(valid_moves) > 0
    
    # Move player 1 and check player 2's valid moves
    game.move_pawn(Position(1, 4))
    valid_moves = game.get_valid_moves()
    assert Position(7, 4) in valid_moves

def test_alternating_turns():
    game = Game()
    assert game.get_current_player() == 1
    game.move_pawn(Position(1, 4))
    assert game.get_current_player() == 2
    game.place_wall(WallOrientation.HORIZONTAL, Position(5, 5))
    assert game.get_current_player() == 1

def test_invalid_consecutive_moves():
    game = Game()
    # Player 1's valid move
    assert game.move_pawn(Position(1, 4))
    # Player 1 trying to move again (should fail)
    assert not game.move_pawn(Position(2, 4))
    assert game.get_current_player() == 2

def test_game_state_string():
    game = Game()
    expected_str = (
        "Current player: 1\n"
        "Player 1 walls remaining: 10\n"
        "Player 2 walls remaining: 10\n"
        "Game state: ongoing"
    )
    assert str(game) == expected_str

def test_no_moves_after_game_over():
    game = Game()
    # Move player 1 to win
    for row in range(1, 9):
        # Player 1's turn - moving towards goal
        assert game.move_pawn(Position(row, 4))
        
        if row < 8:
            # Player 2's turn - moving between two positions
            if row % 2 == 0:
                assert game.move_pawn(Position(7, 3))
            else:
                assert game.move_pawn(Position(8, 3))
    
    assert game.is_game_over()
    # Try to make moves after game is over
    assert not game.move_pawn(Position(7, 5))
    assert not game.place_wall(WallOrientation.HORIZONTAL, Position(4, 4))

def test_wall_placement_when_out_of_walls():
    game = Game()
    
    # Place all walls for player 1 in non-overlapping positions
    for i in range(5):
        assert game.place_wall(WallOrientation.HORIZONTAL, Position(i, 0))
        assert game.place_wall(WallOrientation.HORIZONTAL, Position(i, 2))
        assert game.place_wall(WallOrientation.HORIZONTAL, Position(i, 4))
        assert game.place_wall(WallOrientation.HORIZONTAL, Position(i, 6))
    
    # Verify that player 1 has no walls remaining
    assert game.get_walls_remaining(1) == 0
    
    # Try to place one more wall for player 1
    assert not game.place_wall(WallOrientation.HORIZONTAL, Position(5, 1))  # Should fail
    
    # Verify that player 1 has no walls remaining
    assert game.get_walls_remaining(2) == 0

    # Try to place one more wall for player 2
    assert not game.place_wall(WallOrientation.HORIZONTAL, Position(7, 1))  # Should fail
