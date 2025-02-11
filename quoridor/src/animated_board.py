import pygame
import sys
from quoridor.src.board import Board
from quoridor.src.utils.types import Position, WallOrientation

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 9
CELL_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // BOARD_SIZE
WALL_THICKNESS = 8
GRID_THICKNESS = WALL_THICKNESS  # Make grid lines as thick as walls
PLAYER_RADIUS = CELL_SIZE // 3
DOT_RADIUS = 8
CORNER_RADIUS = 4  # Radius for rounded corners
WALL_CORNER_RADIUS = 2  # Smaller radius for wall corners

# Colors
BOARD_COLOR = (120, 100, 80)      # Darker Coffee
GRID_COLOR = (60, 40, 20)      # Darker Dun
WALL_COLOR = (255, 223, 186)     # Light yellow wood
BACKGROUND = BOARD_COLOR
PLAYER1_COLOR = (153, 0, 0)  #  Red
PLAYER2_COLOR = (24, 24, 132)  # Light Blue
PLAYER1_LIGHT_COLOR = (255, 150, 150)  # Light Red for player 1's valid moves
PLAYER2_LIGHT_COLOR = (150, 150, 255)  # Light Blue for player 2's valid moves
WALL_PREVIEW_COLOR = (255, 223, 186, 128)  # Semi-transparent light yellow wood

class AnimatedBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quoridor")
        self.clock = pygame.time.Clock()
        
        # Initialize game board
        self.board = Board()
        self.selected_pawn = None
        self.valid_moves = []
        self.placing_wall = False
        self.wall_orientation = WallOrientation.HORIZONTAL
        self.wall_preview_pos = None

    def screen_to_board_position(self, screen_pos):
        x, y = screen_pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return Position(row, col)

    def board_to_screen_position(self, position):
        return (position.col * CELL_SIZE + CELL_SIZE // 2,
                position.row * CELL_SIZE + CELL_SIZE // 2)

    def draw_grid(self):
        self.screen.fill(BACKGROUND)
        
        # Draw squares with rounded corners
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE + GRID_THICKNESS // 2
                y = row * CELL_SIZE + GRID_THICKNESS // 2
                width = CELL_SIZE - GRID_THICKNESS
                height = CELL_SIZE - GRID_THICKNESS
                
                # Draw rounded rectangle
                rect = pygame.Rect(x, y, width, height)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, border_radius=CORNER_RADIUS)

    def draw_pawns(self):
        # Draw pawn 1
        pos1 = self.board_to_screen_position(self.board.pawn1.position)
        pygame.draw.circle(self.screen, PLAYER1_COLOR, pos1, PLAYER_RADIUS)
        
        # Draw pawn 2
        pos2 = self.board_to_screen_position(self.board.pawn2.position)
        pygame.draw.circle(self.screen, PLAYER2_COLOR, pos2, PLAYER_RADIUS)

    def draw_walls(self):
        # Draw placed horizontal walls
        for row in range(BOARD_SIZE - 1):
            for col in range(BOARD_SIZE - 1):
                pos = Position(row, col)
                if self.board.horizontal_wall_slots[pos].occupied:
                    x = col * CELL_SIZE + GRID_THICKNESS // 2
                    y = (row + 1) * CELL_SIZE - WALL_THICKNESS // 2
                    width = CELL_SIZE * 2 - GRID_THICKNESS
                    rect = pygame.Rect(x, y, width, WALL_THICKNESS)
                    pygame.draw.rect(self.screen, WALL_COLOR, rect, border_radius=WALL_CORNER_RADIUS)

        # Draw placed vertical walls
        for row in range(BOARD_SIZE - 1):
            for col in range(BOARD_SIZE - 1):
                pos = Position(row, col)
                if self.board.vertical_wall_slots[pos].occupied:
                    x = (col + 1) * CELL_SIZE - WALL_THICKNESS // 2
                    y = row * CELL_SIZE + GRID_THICKNESS // 2
                    height = CELL_SIZE * 2 - GRID_THICKNESS
                    rect = pygame.Rect(x, y, WALL_THICKNESS, height)
                    pygame.draw.rect(self.screen, WALL_COLOR, rect, border_radius=WALL_CORNER_RADIUS)

    def draw_valid_moves(self):
        if self.selected_pawn and self.valid_moves:
            # Choose color based on selected pawn
            valid_move_color = (PLAYER1_LIGHT_COLOR 
                              if self.selected_pawn.id == 1 
                              else PLAYER2_LIGHT_COLOR)
            
            for move in self.valid_moves:
                screen_pos = self.board_to_screen_position(move)
                pygame.draw.circle(self.screen, valid_move_color, screen_pos, DOT_RADIUS)

    def draw_wall_preview(self):
        if self.placing_wall and self.wall_preview_pos:
            pos = self.wall_preview_pos
            try:
                if self.board.can_place_wall_at_position(self.wall_orientation, pos):
                    if self.wall_orientation == WallOrientation.HORIZONTAL:
                        x = pos.col * CELL_SIZE + GRID_THICKNESS // 2
                        y = (pos.row + 1) * CELL_SIZE - WALL_THICKNESS // 2
                        width = CELL_SIZE * 2 - GRID_THICKNESS
                        rect = pygame.Rect(x, y, width, WALL_THICKNESS)
                        pygame.draw.rect(self.screen, WALL_PREVIEW_COLOR, rect, border_radius=WALL_CORNER_RADIUS)
                    else:
                        x = (pos.col + 1) * CELL_SIZE - WALL_THICKNESS // 2
                        y = pos.row * CELL_SIZE + GRID_THICKNESS // 2
                        height = CELL_SIZE * 2 - GRID_THICKNESS
                        rect = pygame.Rect(x, y, WALL_THICKNESS, height)
                        pygame.draw.rect(self.screen, WALL_PREVIEW_COLOR, rect, border_radius=WALL_CORNER_RADIUS)
            except (ValueError, IndexError):
                pass

    def handle_click(self, pos):
        board_pos = self.screen_to_board_position(pos)
        
        if self.placing_wall:
            try:
                self.board.place_wall(self.wall_orientation, board_pos)
                self.placing_wall = False
                self.wall_preview_pos = None
            except ValueError:
                pass
        else:
            # Check if clicking on a pawn
            if board_pos == self.board.pawn1.position:
                self.selected_pawn = self.board.pawn1
                self.valid_moves = self.board.get_all_valid_pawn_moves(self.selected_pawn)
            elif board_pos == self.board.pawn2.position:
                self.selected_pawn = self.board.pawn2
                self.valid_moves = self.board.get_all_valid_pawn_moves(self.selected_pawn)
            # Check if clicking on a valid move
            elif self.selected_pawn and board_pos in self.valid_moves:
                self.board.move_pawn(self.selected_pawn, board_pos)
                self.selected_pawn = None
                self.valid_moves = []

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  # Toggle wall placement mode
                        self.placing_wall = not self.placing_wall
                        self.selected_pawn = None
                        self.valid_moves = []
                    elif event.key == pygame.K_r:  # Rotate wall orientation
                        if self.placing_wall:
                            self.wall_orientation = (WallOrientation.VERTICAL 
                                if self.wall_orientation == WallOrientation.HORIZONTAL 
                                else WallOrientation.HORIZONTAL)
            
            # Update wall preview position
            if self.placing_wall:
                mouse_pos = pygame.mouse.get_pos()
                self.wall_preview_pos = self.screen_to_board_position(mouse_pos)

            # Draw everything
            self.draw_grid()
            self.draw_walls()
            self.draw_valid_moves()
            self.draw_pawns()
            if self.placing_wall:
                self.draw_wall_preview()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    animated_board = AnimatedBoard()
    animated_board.run()
