import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]]   # J shape
]

# Game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
grid = [[0] * COLUMNS for _ in range(ROWS)]

def draw_grid():
    for y in range(ROWS):
        for x in range(COLUMNS):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x, self.y = COLUMNS // 2 - len(self.shape[0]) // 2, 0

    def draw(self):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, pygame.Rect((self.x + col_index) * BLOCK_SIZE, (self.y + row_index) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    def move(self, dx, dy):
        if not self.collides(dx, dy):
            self.x += dx
            self.y += dy
        else:
            if dy > 0:
                self.lock()
                return True
        return False
    
    def collides(self, dx, dy):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.x + col_index + dx, self.y + row_index + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x]):
                        return True
        return False
    
    def lock(self):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid[self.y + row_index][self.x + col_index] = self.color
        clear_rows()

def clear_rows():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(new_grid) < ROWS:
        new_grid.insert(0, [0] * COLUMNS)
    grid = new_grid

def main():
    running = True
    current_tetromino = Tetromino()
    
    while running:
        screen.fill(BLACK)
        draw_grid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move(0, 1)
        
        if current_tetromino.move(0, 1):
            current_tetromino = Tetromino()
        
        current_tetromino.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
