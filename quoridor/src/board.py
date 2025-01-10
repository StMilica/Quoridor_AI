class Board:
    def __init__(self):
        self.size = 9  # 9x9 grid
        self.grid = [[0] * self.size for _ in range(self.size)]  # 0 represents empty spaces
        self.horizontal_walls = []  # Store horizontal walls
        self.vertical_walls = []    # Store vertical walls

    def is_within_bounds(self, position):
        """Check if a position is within the board."""
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def place_wall(self, wall_type, position, players):
        """Place a wall on the board if valid and ensure it does not block all paths."""
        x, y = position
        if not self.is_within_bounds(position):
            return False

        # Simulate placing the wall
        if wall_type == 'horizontal':
            if any(pos in self.horizontal_walls for pos in [(x, y), (x, y - 1), (x, y + 1)]):
                return False
            self.horizontal_walls.append(position)
        elif wall_type == 'vertical':
            if any(pos in self.horizontal_walls for pos in [(x, y), (x - 1, y), (x + 1, y)]):
                return False
            self.vertical_walls.append(position)
        else:
            return False

        # Check if the wall blocks all paths for any player
        if not self._all_paths_valid(players):
            # Remove the wall if it blocks all paths
            if wall_type == 'horizontal':
                self.horizontal_walls.remove(position)
            elif wall_type == 'vertical':
                self.vertical_walls.remove(position)
            return False

        return True

    def _all_paths_valid(self, players):
        """Check if all players still have a valid path to their goal."""
        for player in players.values():
            if not self._has_path_to_goal(player.position, player.goal_row):
                return False
        return True

    def _has_path_to_goal(self, start, goal_row):
        """Check if a player has a valid path to their goal row using BFS."""
        from collections import deque

        queue = deque([start])
        visited = set()
        visited.add(start)

        while queue:
            x, y = queue.popleft()

            # Check if the current position is on the goal row
            if x == goal_row:
                return True

            # Explore neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.is_within_bounds((nx, ny)):
                    if not self.is_path_blocked((x, y), (nx, ny)):
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        return False

    def is_path_blocked(self, position1, position2):
        """Check if a wall blocks the direct path between two positions."""
        x1, y1 = position1
        x2, y2 = position2

        if x1 == x2:  # Horizontal movement
            if y2 > y1:  # Moving right
                return (x1, y1) in self.vertical_walls or (x1 - 1, y1) in self.vertical_walls
            if y1 > y2:  # Moving left
                return (x1, y2) in self.vertical_walls or (x1 - 1, y2) in self.vertical_walls

        elif y1 == y2:  # Vertical movement
            if x2 > x1:  # Moving down
                return (x1, y1) in self.horizontal_walls or (x1, y1 - 1) in self.horizontal_walls
            if x1 > x2:  # Moving up
                return (x2, y1) in self.horizontal_walls or (x2, y1 - 1) in self.horizontal_walls

        return False

    def display_board(self, players):
        """Print a text-based representation of the board."""
        board = [['.' for _ in range(self.size)] for _ in range(self.size)]

        # Mark player positions
        for player, position in players.items():
            x, y = position
            board[x][y] = player[0]  # Use the first letter of the player's name

        # Print the board
        for row in board:
            print(' '.join(row))
