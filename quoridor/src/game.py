from board import Board
from player import Player

class Game:
    def __init__(self):
        self.board = Board()
        self.players = {}
        self.current_turn = None

    def add_player(self, name, start_position, goal_row):
        """Add a player to the game."""
        if name in self.players:
            raise ValueError(f"Player '{name}' already exists.")
        player = Player(name, start_position, goal_row)
        self.players[name] = player
        if not self.current_turn:
            self.current_turn = name

    def move_player(self, player_name, new_position):
        """Move a player if it's their turn and the move is valid."""
        if player_name != self.current_turn:
            raise ValueError("It's not this player's turn.")
        if player_name not in self.players:
            raise ValueError("Player does not exist.")
        player = self.players[player_name]
        if not self.board.is_within_bounds(new_position):
            return False
        # Add additional logic to ensure valid moves (e.g., no walls blocking)
        player.move(new_position)
        self._switch_turn()
        return True

    def place_wall(self, player_name, wall_type, position):
        """Place a wall if it's the player's turn and they have walls remaining."""
        if player_name != self.current_turn:
            raise ValueError("It's not this player's turn.")
        if player_name not in self.players:
            raise ValueError("Player does not exist.")
        player = self.players[player_name]
        if player.walls_remaining <= 0:
            raise ValueError("Player has no walls remaining.")
        
        # Delegate to the Board class for the actual placement
        if self.board.place_wall(wall_type, position):
            player.use_wall()
            self._switch_turn()
            return True
        return False

    def _switch_turn(self):
        """Switch the turn to the next player."""
        player_names = list(self.players.keys())
        current_index = player_names.index(self.current_turn)
        self.current_turn = player_names[(current_index + 1) % len(player_names)]

    def display(self):
        """Display the current state of the board and players."""
        player_positions = {name: player.position for name, player in self.players.items()}
        self.board.display_board(player_positions)

    def is_game_over(self):
        """Check if any player has reached their goal row."""
        for player in self.players.values():
            if player.position[0] == player.goal_row:
                return True, player.name
        return False, None
