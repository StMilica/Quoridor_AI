import pygame
import sys
from quoridor.src.board import Board
from quoridor.src.utils.types import Position, WallOrientation
from quoridor.src.game import Game, GameState

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850  # Increased height to accommodate info text
BOARD_SIZE = 9
CELL_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT - 50) // BOARD_SIZE  # Adjusted for new height
WALL_THICKNESS = 10
GRID_THICKNESS = WALL_THICKNESS  # Make grid lines as thick as walls
PLAYER_RADIUS = CELL_SIZE // 3
DOT_RADIUS = 8
CORNER_RADIUS = 2  # Radius for rounded corners
WALL_CORNER_RADIUS = 2  # Smaller radius for wall corners
ERROR_COLOR = (112, 25, 26)  # Red color for error messages
ERROR_MESSAGE_DURATION = 3000  # Duration in milliseconds (3 seconds)

# Colors
# BOARD_COLOR = (120, 100, 80)      # Darker Coffee
# GRID_COLOR = (60, 40, 20)      # Darker Dun
# WALL_COLOR = (255, 223, 186)     # Light yellow wood
# BACKGROUND = BOARD_COLOR
# PLAYER1_COLOR = (153, 0, 0)  #  Red
# PLAYER2_COLOR = (24, 24, 132)  # Light Blue
# PLAYER1_LIGHT_COLOR = (255, 150, 150, 128)  # Light Red with alpha for player 1's valid moves
# PLAYER2_LIGHT_COLOR = (150, 150, 255, 128)  # Light Blue with alpha for player 2's valid moves
# WALL_PREVIEW_COLOR = (255, 223, 186, 128)  # Semi-transparent light yellow wood

BOARD_COLOR = (77, 64, 49)
GRID_COLOR = (54, 43, 32)
WALL_COLOR = (199, 197, 187)     # Light yellow wood
BACKGROUND = BOARD_COLOR
PLAYER1_COLOR = (137, 46, 47)  #  Red
PLAYER2_COLOR = (16, 112, 143)  # Light Blue
PLAYER1_LIGHT_COLOR = (137, 46, 47, 128)  # Light Red with alpha for player 1's valid moves
PLAYER2_LIGHT_COLOR = (16, 112, 143, 128)  # Light Blue with alpha for player 2's valid moves
WALL_PREVIEW_COLOR = (199, 197, 187, 128)  # Semi-transparent light yellow wood

# Add to the Constants section
BUTTON_COLOR = (46, 36, 27)  # Darker than board color
BUTTON_HOVER_COLOR = (100, 80, 60)  # Lighter when hovering
BUTTON_TEXT_COLOR = (199, 197, 187)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_MARGIN = 15  # Margin from screen edges

class AnimatedBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quoridor")
        self.clock = pygame.time.Clock()
        
        # Initialize game
        self.game = Game()
        self.selected_pawn = None
        self.valid_moves = []
        self.current_pawn_moves = []  # Add this line to store current player's moves
        self.wall_preview_pos = None
        self.error_message_start = None
        self.current_wall_orientation = WallOrientation.HORIZONTAL  # Default orientation
        self.pawn_selected_for_move = False  # Add this flag

        self.reset_button_rect = pygame.Rect(
            SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
            SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        self.is_button_hovered = False

    def screen_to_board_position(self, screen_pos):
        x, y = screen_pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return Position(row, col)

    def board_to_screen_position(self, position):
        return (position.col * CELL_SIZE + CELL_SIZE // 2,
                position.row * CELL_SIZE + CELL_SIZE // 2)

    def screen_to_wall_position(self, screen_pos, orientation):
        """Convert screen coordinates to wall position based on closest grid line."""
        x, y = screen_pos
        
        # Calculate distances to grid lines
        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        
        if orientation == WallOrientation.VERTICAL:
            # For vertical walls, snap to vertical grid lines
            dist_to_left = x - cell_x * CELL_SIZE
            dist_to_right = (cell_x + 1) * CELL_SIZE - x
            
            if dist_to_left < dist_to_right:
                col = cell_x - 1
            else:
                col = cell_x
                
            row = cell_y
            
        else:  # HORIZONTAL
            # For horizontal walls, snap to horizontal grid lines
            dist_to_top = y - cell_y * CELL_SIZE
            dist_to_bottom = (cell_y + 1) * CELL_SIZE - y
            
            if dist_to_top < dist_to_bottom:
                row = cell_y - 1
            else:
                row = cell_y
                
            col = cell_x
        
        # Ensure we're within valid wall placement bounds
        row = max(0, min(row, BOARD_SIZE - 2))
        col = max(0, min(col, BOARD_SIZE - 2))
        
        return Position(row, col)

    def get_wall_placement_info(self, mouse_pos):
        """Determine the best wall orientation and position based on mouse position."""
        x, y = mouse_pos
        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        
        # Calculate distances to nearest grid lines
        x_in_cell = x % CELL_SIZE
        y_in_cell = y % CELL_SIZE
        
        # Define grid line detection threshold
        GRID_THRESHOLD = WALL_THICKNESS * 2
        
        # Check if mouse is near vertical grid lines
        near_vertical = x_in_cell < GRID_THRESHOLD or x_in_cell > CELL_SIZE - GRID_THRESHOLD
        # Check if mouse is near horizontal grid lines
        near_horizontal = y_in_cell < GRID_THRESHOLD or y_in_cell > CELL_SIZE - GRID_THRESHOLD
        
        # If near vertical grid line and not near horizontal, force vertical orientation
        if near_vertical and not near_horizontal:
            self.current_wall_orientation = WallOrientation.VERTICAL
        # If near horizontal grid line and not near vertical, force horizontal orientation
        elif near_horizontal and not near_vertical:
            self.current_wall_orientation = WallOrientation.HORIZONTAL
        # If near both or neither, choose based on closest
        else:
            dist_to_vertical = min(x_in_cell, CELL_SIZE - x_in_cell)
            dist_to_horizontal = min(y_in_cell, CELL_SIZE - y_in_cell)
            self.current_wall_orientation = (
                WallOrientation.VERTICAL if dist_to_vertical < dist_to_horizontal 
                else WallOrientation.HORIZONTAL
            )
        
        # Calculate wall position based on orientation
        if self.current_wall_orientation == WallOrientation.VERTICAL:
            col = cell_x - 1 if x_in_cell < CELL_SIZE/2 else cell_x
            row = cell_y
        else:
            col = cell_x
            row = cell_y - 1 if y_in_cell < CELL_SIZE/2 else cell_y
        
        # Ensure we're within valid wall placement bounds
        row = max(0, min(row, BOARD_SIZE - 2))
        col = max(0, min(col, BOARD_SIZE - 2))
        
        return Position(row, col)

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
        pos1 = self.board_to_screen_position(self.game.board.pawn1.position)
        pygame.draw.circle(self.screen, PLAYER1_COLOR, pos1, PLAYER_RADIUS)
        
        # Draw pawn 2
        pos2 = self.board_to_screen_position(self.game.board.pawn2.position)
        pygame.draw.circle(self.screen, PLAYER2_COLOR, pos2, PLAYER_RADIUS)

    def draw_walls(self):
        # Draw placed horizontal walls
        for row in range(BOARD_SIZE - 1):
            for col in range(BOARD_SIZE - 1):
                pos = Position(row, col)
                if self.game.board.horizontal_wall_slots[pos].occupied:
                    x = col * CELL_SIZE + GRID_THICKNESS // 2
                    y = (row + 1) * CELL_SIZE - WALL_THICKNESS // 2
                    width = CELL_SIZE * 2 - GRID_THICKNESS
                    rect = pygame.Rect(x, y, width, WALL_THICKNESS)
                    pygame.draw.rect(self.screen, WALL_COLOR, rect, border_radius=WALL_CORNER_RADIUS)

        # Draw placed vertical walls
        for row in range(BOARD_SIZE - 1):
            for col in range(BOARD_SIZE - 1):
                pos = Position(row, col)
                if self.game.board.vertical_wall_slots[pos].occupied:
                    x = (col + 1) * CELL_SIZE - WALL_THICKNESS // 2
                    y = row * CELL_SIZE + GRID_THICKNESS // 2
                    height = CELL_SIZE * 2 - GRID_THICKNESS
                    rect = pygame.Rect(x, y, WALL_THICKNESS, height)
                    pygame.draw.rect(self.screen, WALL_COLOR, rect, border_radius=WALL_CORNER_RADIUS)

    def draw_valid_moves(self):
        # Don't show any moves if game is over
        if self.game.is_game_over():
            return

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_board_pos = self.screen_to_board_position(mouse_pos)

        # Draw possible moves for current player's pawn
        current_player = self.game.get_current_player()
        current_pawn = self.game.board.pawn1 if current_player == 1 else self.game.board.pawn2
        valid_move_color = PLAYER1_LIGHT_COLOR if current_player == 1 else PLAYER2_LIGHT_COLOR
        hover_move_color = (valid_move_color[0], valid_move_color[1], valid_move_color[2], 224)  # Less transparent color

        for move in self.current_pawn_moves:
            screen_pos = self.board_to_screen_position(move)
            # Create transparent surface for the dot
            dot_surface = pygame.Surface((DOT_RADIUS * 2, DOT_RADIUS * 2), pygame.SRCALPHA)
            if move == mouse_board_pos:
                pygame.draw.circle(dot_surface, hover_move_color, (DOT_RADIUS, DOT_RADIUS), DOT_RADIUS)
            else:
                pygame.draw.circle(dot_surface, valid_move_color, (DOT_RADIUS, DOT_RADIUS), DOT_RADIUS)
            # Blit the dot at the correct position, adjusting for the surface size
            self.screen.blit(dot_surface, (screen_pos[0] - DOT_RADIUS, screen_pos[1] - DOT_RADIUS))

    def draw_wall_preview(self):
        # Don't show wall preview if game is over
        if self.game.is_game_over():
            return

        current_player = self.game.get_current_player()
        if (not self.pawn_selected_for_move and 
            self.wall_preview_pos and 
            self.game.walls_remaining[current_player] > 0):  # Only show preview if walls remain
                pos = self.get_wall_placement_info(self.wall_preview_pos)
                x, y = self.wall_preview_pos
                cell_x = x % CELL_SIZE
                cell_y = y % CELL_SIZE

                # Define grid line detection threshold
                GRID_THRESHOLD = WALL_THICKNESS * 2

                # Check if mouse is near vertical or horizontal grid lines
                near_vertical = cell_x < GRID_THRESHOLD or cell_x > CELL_SIZE - GRID_THRESHOLD
                near_horizontal = cell_y < GRID_THRESHOLD or cell_y > CELL_SIZE - GRID_THRESHOLD

                if near_vertical or near_horizontal:
                    try:
                        if self.game.board.can_place_wall_at_position(self.current_wall_orientation, pos):
                            # Create a transparent surface for the wall preview
                            if self.current_wall_orientation == WallOrientation.HORIZONTAL:
                                width = CELL_SIZE * 2 - GRID_THICKNESS
                                preview_surface = pygame.Surface((width, WALL_THICKNESS), pygame.SRCALPHA)
                                pygame.draw.rect(preview_surface, WALL_PREVIEW_COLOR, 
                                               preview_surface.get_rect(), border_radius=WALL_CORNER_RADIUS)
                                x = pos.col * CELL_SIZE + GRID_THICKNESS // 2
                                y = (pos.row + 1) * CELL_SIZE - WALL_THICKNESS // 2
                                self.screen.blit(preview_surface, (x, y))
                            else:
                                height = CELL_SIZE * 2 - GRID_THICKNESS
                                preview_surface = pygame.Surface((WALL_THICKNESS, height), pygame.SRCALPHA)
                                pygame.draw.rect(preview_surface, WALL_PREVIEW_COLOR, 
                                               preview_surface.get_rect(), border_radius=WALL_CORNER_RADIUS)
                                x = (pos.col + 1) * CELL_SIZE - WALL_THICKNESS // 2
                                y = pos.row * CELL_SIZE + GRID_THICKNESS // 2
                                self.screen.blit(preview_surface, (x, y))
                    except (ValueError, IndexError):
                        pass

    def draw_info(self):
        font = pygame.font.SysFont(None, 24)
        player1_walls = self.game.get_walls_remaining(1)
        player2_walls = self.game.get_walls_remaining(2)
        current_player = self.game.get_current_player()
        current_player_text = "Red Player" if current_player == 1 else "Blue Player"

        info_text = f"Red Player walls: {player1_walls} | Blue Player walls: {player2_walls} | Current player: {current_player_text}"
        text_surface = font.render(info_text, True, (199, 197, 187))
        text_rect = text_surface.get_rect(left=60, centery=SCREEN_HEIGHT - 30)
        self.screen.blit(text_surface, text_rect)

        # Display path blocked message
        if getattr(self.game, 'path_blocked', False):
            if self.error_message_start is None:
                self.error_message_start = pygame.time.get_ticks()
            
            current_time = pygame.time.get_ticks()
            if current_time - self.error_message_start < ERROR_MESSAGE_DURATION:
                error_text1 = "There must remain at least one path"
                error_text2 = "to the goal for each pawn!"
                error_font = pygame.font.SysFont(None, 42)
                
                # Render first line (centered)
                error_surface1 = error_font.render(error_text1, True, ERROR_COLOR)
                error_rect1 = error_surface1.get_rect(center=(SCREEN_WIDTH // 2, (4 * CELL_SIZE) + (CELL_SIZE // 2) - 20))
                
                # Render second line (centered)
                error_surface2 = error_font.render(error_text2, True, ERROR_COLOR)
                error_rect2 = error_surface2.get_rect(center=(SCREEN_WIDTH // 2, (4 * CELL_SIZE) + (CELL_SIZE // 2) + 20))
                
                # Create a semi-transparent surface for the background
                background_surface = pygame.Surface((error_rect1.width + 20, error_rect2.bottom - error_rect1.top + 20), pygame.SRCALPHA)
                background_surface.fill((199, 197, 187, 184))  # Similar to WALL_COLOR with transparency
                
                # Blit the background surface
                self.screen.blit(background_surface, (error_rect1.left - 10, error_rect1.top - 10))
                
                # Blit the error text on top of the background
                self.screen.blit(error_surface1, error_rect1)
                self.screen.blit(error_surface2, error_rect2)
            else:
                self.error_message_start = None
                self.game.path_blocked = False

        if self.game.is_game_over():
            winner = self.game.get_winner()
            winner_text = "Red Player wins!" if winner == 1 else "Blue Player wins!"
            winner_font = pygame.font.SysFont(None, 48)  # Bigger font for the winner message
            winner_surface = winner_font.render(winner_text, True, (13, 89, 2))
            winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, (4 * CELL_SIZE) + (CELL_SIZE // 2)))
            
            # Create a semi-transparent surface for the background
            background_surface = pygame.Surface((winner_rect.width + 20, winner_rect.height + 20), pygame.SRCALPHA)
            background_surface.fill((199, 197, 187, 184))  # Similar to WALL_COLOR with transparency
            
            # Blit the background surface
            self.screen.blit(background_surface, (winner_rect.left - 10, winner_rect.top - 10))
            
            # Blit the winner text on top of the background
            self.screen.blit(winner_surface, winner_rect)

    def draw_reset_button(self):
        """Draw the reset button with hover effect"""
        color = BUTTON_HOVER_COLOR if self.is_button_hovered else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.reset_button_rect, border_radius=5)
        
        # Draw button text
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Reset", True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_click(self, pos):
        # Add at the beginning of handle_click method
        if self.reset_button_rect.collidepoint(pos):
            self.__init__()  # Reset the game
            return

        board_pos = self.screen_to_board_position(pos)
        current_player = self.game.get_current_player()
        current_pawn = self.game.board.pawn1 if current_player == 1 else self.game.board.pawn2

        # Check if clicking on a valid move
        if board_pos in self.current_pawn_moves:
            self.game.move_pawn(board_pos)
            self.current_pawn_moves = []
            self.valid_moves = []
            self.wall_preview_pos = None
            self.selected_pawn = None
            self.pawn_selected_for_move = False
        else:
            # Try to place wall if not moving pawn
            wall_pos = self.get_wall_placement_info(pos)
            if self.game.place_wall(self.current_wall_orientation, wall_pos):
                self.wall_preview_pos = None
                self.selected_pawn = None
                self.valid_moves = []
            else:
                # Update current player's possible moves
                try:
                    self.current_pawn_moves = self.game.board.get_all_valid_pawn_moves(current_pawn)
                except ValueError:
                    self.current_pawn_moves = []

    def run(self):
        running = True
        while running:
            # Update current player's possible moves only if game is not over
            if not self.game.is_game_over():
                current_player = self.game.get_current_player()
                current_pawn = self.game.board.pawn1 if current_player == 1 else self.game.board.pawn2
                try:
                    self.current_pawn_moves = self.game.board.get_all_valid_pawn_moves(current_pawn)
                except ValueError:
                    self.current_pawn_moves = []
            else:
                # Clear all move indicators and previews when game is over
                self.current_pawn_moves = []
                self.valid_moves = []
                self.wall_preview_pos = None
                self.selected_pawn = None
                self.pawn_selected_for_move = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.is_button_hovered = self.reset_button_rect.collidepoint(event.pos)
            
            # Update wall preview position when not moving pawn
            mouse_pos = pygame.mouse.get_pos()
            if not self.selected_pawn:
                self.wall_preview_pos = mouse_pos

            # Draw everything
            self.draw_grid()
            self.draw_walls()
            self.draw_valid_moves()  # This will now show moves for current player
            self.draw_pawns()
            self.draw_info()
            if not self.selected_pawn:
                self.draw_wall_preview()
            self.draw_reset_button()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    animated_board = AnimatedBoard()
    animated_board.run()
