import streamlit as st
import pygame
import random

# Initialize pygame
pygame.init()

# Define the Tetris grid
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (128, 0, 128),  # Purple
    (0, 128, 0),    # Green
    (255, 0, 0)     # Red
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Define the game logic
class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_x = 3
        self.piece_y = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color}

    def rotate_piece(self):
        self.current_piece["shape"] = [
            [self.current_piece["shape"][y][x]
             for y in range(len(self.current_piece["shape"]))]
            for x in range(len(self.current_piece["shape"][0]) - 1, -1, -1)
        ]

    def is_valid_position(self, x_offset=0, y_offset=0):
        for y, row in enumerate(self.current_piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.piece_x + x + x_offset
                    new_y = self.piece_y + y + y_offset
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (
                            new_y >= 0 and self.grid[new_y][new_x]):
                        return False
        return True

    def place_piece(self):
        for y, row in enumerate(self.current_piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.piece_y + y][self.piece_x + x] = self.current_piece["color"]
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.piece_x = 3
        self.piece_y = 0
        if not self.is_valid_position():
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = GRID_HEIGHT - len(new_grid)
        self.score += cleared_lines * 100
        self.grid = [[0] * GRID_WIDTH for _ in range(cleared_lines)] + new_grid

    def move(self, dx, dy):
        if self.is_valid_position(dx, dy):
            self.piece_x += dx
            self.piece_y += dy
        elif dy > 0:
            self.place_piece()

# Initialize the Streamlit app
def main():
    st.title("Tetris Game")
    st.sidebar.title("Controls")
    st.sidebar.text("⬅️ Move Left\n➡️ Move Right\n⬇️ Move Down\n🔄 Rotate Piece")

    # Game canvas
    tetris = Tetris()
    clock = pygame.time.Clock()

    # Game loop
    def render_game():
        canvas = pygame.Surface((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        canvas.fill(BLACK)

        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = tetris.grid[y][x] if tetris.grid[y][x] else GRAY
                pygame.draw.rect(
                    canvas,
                    color,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0 if tetris.grid[y][x] else 1
                )

        # Draw current piece
        for y, row in enumerate(tetris.current_piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        canvas,
                        tetris.current_piece["color"],
                        (
                            (tetris.piece_x + x) * BLOCK_SIZE,
                            (tetris.piece_y + y) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

        return canvas

    # Run the game in Streamlit
    with st.empty():
        while not tetris.game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetris.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        tetris.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        tetris.move(0, 1)
                    elif event.key == pygame.K_UP:
                        tetris.rotate_piece()

            tetris.move(0, 1)
            frame = render_game()
            st.image(pygame.surfarray.array3d(frame), channels="RGB")
            clock.tick(10)

    st.write("Game Over! Your score:", tetris.score)


if __name__ == "__main__":
    main()
