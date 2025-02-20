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