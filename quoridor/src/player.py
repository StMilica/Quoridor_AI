class Player:
    def __init__(self, name, start_position, goal_row):
        """Initialize a player with a name, starting position, and goal row."""
        self.name = name
        self.position = start_position  # Current position as a tuple (row, col)
        self.goal_row = goal_row        # The row the player must reach to win
        self.walls_remaining = 10      # Number of walls the player can place

    def move(self, new_position):
        """Update the player's position."""
        self.position = new_position

    def use_wall(self):
        """Reduce the number of remaining walls by one."""
        if self.walls_remaining > 0:
            self.walls_remaining -= 1
        else:
            raise ValueError(f"{self.name} has no walls remaining.")

    def __repr__(self):
        return f"Player(name={self.name}, position={self.position}, goal_row={self.goal_row}, walls_remaining={self.walls_remaining})"
