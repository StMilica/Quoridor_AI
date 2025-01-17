import pygame
import sys
import os

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WALL_THICKNESS = 10
PLAYER_RADIUS = CELL_SIZE // 4
DOT_RADIUS = 5

# Colors
BACKGROUND_COLOR = (240, 240, 240)
GRID_COLOR = (200, 200, 200)
PLAYER_COLOR = [(255, 0, 0), (0, 0, 255)]  # Player 1: Red, Player 2: Blue
WALL_COLOR = (0, 0, 0)
DOT_COLOR = (50, 255, 50)

# Position the pygame window to avoid blocking VSCode
os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"  # Adjust as needed

class AnimatedBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quoridor")
        self.clock = pygame.time.Clock()

        # Board data
        self.player_positions = [[{"occupied": False, "can_be_occupied": True, "player": None} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_positions[0][4]["occupied"] = True
        self.player_positions[0][4]["can_be_occupied"] = False
        self.player_positions[0][4]["player"] = 0

        self.player_positions[8][4]["occupied"] = True
        self.player_positions[8][4]["can_be_occupied"] = False
        self.player_positions[8][4]["player"] = 1

        self.horizontal_walls = [[False] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)]
        self.vertical_walls = [[False] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)]

        self.selected_player = None  # Track the currently selected player

    def draw_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                pygame.draw.rect(self.screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def draw_players(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.player_positions[row][col]
                if cell["occupied"] and cell["player"] is not None:
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    color = PLAYER_COLOR[cell["player"]]
                    pygame.draw.circle(self.screen, color, (x, y), PLAYER_RADIUS)

    def draw_highlight(self):
        if self.selected_player is not None:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.player_positions[row][col]["can_be_occupied"]:
                        x = col * CELL_SIZE + CELL_SIZE // 2
                        y = row * CELL_SIZE + CELL_SIZE // 2
                        pygame.draw.circle(self.screen, DOT_COLOR, (x, y), DOT_RADIUS)

    def draw_walls(self):
        # Draw horizontal walls
        for row in range(GRID_SIZE - 1):
            for col in range(GRID_SIZE - 1):
                if self.horizontal_walls[row][col]:
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE + CELL_SIZE
                    pygame.draw.rect(
                        self.screen, WALL_COLOR, (x, y - WALL_THICKNESS // 2, CELL_SIZE, WALL_THICKNESS)
                    )
        # Draw vertical walls
        for row in range(GRID_SIZE - 1):
            for col in range(GRID_SIZE - 1):
                if self.vertical_walls[row][col]:
                    x = col * CELL_SIZE + CELL_SIZE
                    y = row * CELL_SIZE
                    pygame.draw.rect(
                        self.screen, WALL_COLOR, (x - WALL_THICKNESS // 2, y, WALL_THICKNESS, CELL_SIZE)
                    )

    def handle_click(self, pos):
        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE

        if self.selected_player is None:
            # Select player if clicked on one
            cell = self.player_positions[row][col]
            if cell["occupied"] and cell["player"] is not None:
                self.selected_player = (row, col)
        else:
            # Move the selected player
            if self.player_positions[row][col]["can_be_occupied"]:
                old_row, old_col = self.selected_player
                player = self.player_positions[old_row][old_col]["player"]

                # Update old position
                self.player_positions[old_row][old_col]["occupied"] = False
                self.player_positions[old_row][old_col]["can_be_occupied"] = True
                self.player_positions[old_row][old_col]["player"] = None

                # Update new position
                self.player_positions[row][col]["occupied"] = True
                self.player_positions[row][col]["can_be_occupied"] = False
                self.player_positions[row][col]["player"] = player

                self.selected_player = None

    def run(self):
        while True:
            self.screen.fill(BACKGROUND_COLOR)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Drawing the board
            self.draw_grid()
            self.draw_players()
            self.draw_highlight()
            self.draw_walls()

            # Update the display
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    board = AnimatedBoard()
    board.run()
