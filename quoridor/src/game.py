from enum import Enum
from quoridor.src.board import Board
from quoridor.src.utils.types import Position, WallOrientation

class GameState(Enum):
    """Game state enumeration."""
    ONGOING = "ongoing"
    PLAYER1_WIN = "player1_wins"  # Player 1 reached row 8
    PLAYER2_WIN = "player2_wins"  # Player 2 reached row 0

class Game:
    def __init__(self):
        """Initialize a new game."""
        self.board = Board()
        self.current_player_id = 1
        self.walls_remaining = {1: 10, 2: 10}  # Each player starts with 10 walls
        self.game_state = GameState.ONGOING
        self.path_blocked = False  # Add flag for blocked path

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_state != GameState.ONGOING

    def get_winner(self) -> int:
        """Get the winner's ID if the game is over, None otherwise."""
        if self.game_state == GameState.PLAYER1_WIN:
            return 1
        elif self.game_state == GameState.PLAYER2_WIN:
            return 2
        return None

    def _check_win_condition(self, pawn) -> bool:
        """Check if the current player has won."""
        if pawn.id == 1 and pawn.position.row == 8:
            self.game_state = GameState.PLAYER1_WIN
            return True
        elif pawn.id == 2 and pawn.position.row == 0:
            self.game_state = GameState.PLAYER2_WIN
            return True
        return False

    def move_pawn(self, target_position: Position) -> bool:
        """
        Attempt to move the current player's pawn to the target position.
        Returns True if move was successful, False otherwise.
        """
        current_pawn = self.board.pawn1 if self.current_player_id == 1 else self.board.pawn2

        try:
            self.board.move_pawn(current_pawn, target_position)
            if self._check_win_condition(current_pawn):
                return True
            self.current_player_id = 3 - self.current_player_id  # Switch between 1 and 2
            return True
        except ValueError:
            return False

    def place_wall(self, orientation: WallOrientation, position: Position) -> bool:
        """
        Attempt to place a wall for the current player.
        Returns True if wall placement was successful, False otherwise.
        """
        if self.walls_remaining[self.current_player_id] <= 0:
            return False

        try:
            # Reset path blocked flag
            self.path_blocked = False
            
            # Try to place the wall
            self.board.place_wall(orientation, position)
            
            # Check if either player is blocked from reaching their goal
            target_row1 = 8  # Target row for player 1
            target_row2 = 0  # Target row for player 2
            
            # Check paths for both players
            player1_blocked = self.board.is_path_blocked(self.board.pawn1.position, target_row1)
            player2_blocked = self.board.is_path_blocked(self.board.pawn2.position, target_row2)
            
            if player1_blocked or player2_blocked:
                # Set path blocked flag
                self.path_blocked = True
                # Remove the wall if it blocks either player
                if orientation == WallOrientation.HORIZONTAL:
                    self.board.horizontal_wall_slots[position].occupied = False
                else:
                    self.board.vertical_wall_slots[position].occupied = False
                return False
            
            # Wall placement successful, update game state
            self.walls_remaining[self.current_player_id] -= 1
            self.current_player_id = 3 - self.current_player_id  # Switch between 1 and 2
            return True
            
        except ValueError:
            return False

    def get_valid_moves(self) -> list[Position]:
        """Get all valid moves for the current player's pawn."""
        current_pawn = self.board.pawn1 if self.current_player_id == 1 else self.board.pawn2
        try:
            return self.board.get_all_valid_pawn_moves(current_pawn)
        except ValueError:
            return []

    def get_current_player(self) -> int:
        """Get the ID of the current player."""
        return self.current_player_id

    def get_walls_remaining(self, player_id: int) -> int:
        """Get the number of walls remaining for the specified player."""
        return self.walls_remaining.get(player_id, 0)

    def is_path_blocked(self) -> bool:
        """Check if the last wall placement attempt blocked a path."""
        return self.path_blocked

    def __str__(self) -> str:
        """String representation of the current game state."""
        return (
            f"Current player: {self.current_player_id}\n"
            f"Player 1 walls remaining: {self.walls_remaining[1]}\n"
            f"Player 2 walls remaining: {self.walls_remaining[2]}\n"
            f"Game state: {self.game_state.value}"
        )