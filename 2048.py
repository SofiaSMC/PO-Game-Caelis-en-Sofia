import pygame
import random
import math
import copy

pygame.init()
# constants
FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS #// means div to an interger, not float
RECT_WIDTH = WIDTH // COLS
OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

# set up window:
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20 # velocity

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# game-over:
import sys

def game_over_popup(window, clock):
    font = pygame.font.SysFont("comicsans", 72, bold=True)
    button_font = pygame.font.SysFont("comicsans", 48, bold=True)

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))

    restart_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 70)
    quit_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 70)

    while True:
        clock.tick(FPS)
        window.blit(overlay, (0, 0))

        # "Game Over" tekst
        text = font.render("Game Over", True, (255, 255, 255))
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 150))

        # Knoppen
        pygame.draw.rect(window, (0, 200, 0), restart_rect)
        pygame.draw.rect(window, (200, 0, 0), quit_rect)

        restart_text = button_font.render("Restart", True, (255, 255, 255))
        quit_text = button_font.render("Quit", True, (255, 255, 255))

        window.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
        window.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# set up:
class Tile: # define tiles as a class
  COLORS = [ # original 2048 tile colors
    (237, 229, 218),
    (238, 225, 201),
    (243, 178, 122),
    (246, 150, 101),
    (247, 124, 95),
    (237, 108, 115),
    (237, 204, 99),
    (236, 202, 90),
  ]

  def __init__(self, value, row, col):
    self.value = value
    self.row = row
    self.col = col
    self.x = col * RECT_WIDTH
    self.y = row * RECT_HEIGHT

  def get_color(self):
    color_index = int(math.log2(self.value)) - 1 # make sure it's int, and -1 bc index starts at 0
    color = self.COLORS[color_index]
    return color

  def draw(self, window):
    color = self.get_color()
    pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

    text = FONT.render(str(self.value), 1, FONT_COLOR) # 1 = for antialiasing
    # surface that contains text

    # where will the text be put
    window.blit( # blit "paste" it onto another surface
      text,
      (   self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
          self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)
      ), 
    )

  def set_pos(self, ceil=False):
    if ceil:
      self.row = math.ceil(self.y / RECT_HEIGHT)
      self.col = math.ceil(self.x / RECT_WIDTH)

    else:
      self.row = math.floor(self.y / RECT_HEIGHT)
      self.col = math.floor(self.x / RECT_WIDTH) 

  def move(self, delta):
    self.x += delta[0]
    self.y += delta[1]


# set up window/drawing:
def draw_grid(window): # draw the grid
  for row in range(1, ROWS):
    y = row * RECT_HEIGHT
    pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
  
  for col in range(1, COLS):
    x = col * RECT_WIDTH
    pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
  
  pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles): # draw inside the window
  window.fill(BACKGROUND_COLOR)

  for tile in tiles.values(): # tiles is a dictionary = faster
    tile.draw(window)

  draw_grid(window)

  pygame.display.update()


# create tiles functions:
def get_random_pos(tiles): # get position for new tiles
  row = None
  col = None

  while True: # to not have the same pos
    row = random.randrange(0, ROWS)
    col = random.randrange(0, COLS)

    if f"{row}{col}" not in tiles: # check if the position is already taken
      break
  
  return row, col

def generate_tiles(): # generate new tiles
  tiles = {}
  for i in range(2):
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(2, row, col) # starting tile
  
  return tiles

# logic based on logged tiles positons first:
def can_move(grid):
    size = len(grid)
    for y in range(size):
        for x in range(size):
            if grid[y][x] == 0:
                return True
            if x < size - 1 and grid[y][x] == grid[y][x + 1]:
                return True
            if y < size - 1 and grid[y][x] == grid[y + 1][x]:
                return True
    return False

def move_grid(grid, direction):
    size = len(grid)
    moved = False
    new_grid = copy.deepcopy(grid)

    def process_line(line):
        nonlocal moved
        merged_line = [0] * size
        skip = False
        insert_pos = 0
        for i in range(size):
            if line[i] == 0:
                continue
            if not skip and insert_pos > 0 and merged_line[insert_pos - 1] == line[i]:
                merged_line[insert_pos - 1] *= 2
                skip = True
                moved = True
            else:
                merged_line[insert_pos] = line[i]
                if i != insert_pos:
                    moved = True
                insert_pos += 1
                skip = False
        return merged_line

    if direction in ['left', 'right']:
        for y in range(size):
            line = new_grid[y][:]
            if direction == 'right':
                line.reverse()
            merged = process_line(line)
            if direction == 'right':
                merged.reverse()
            new_grid[y] = merged
    elif direction in ['up', 'down']:
        for x in range(size):
            line = [new_grid[y][x] for y in range(size)]
            if direction == 'down':
                line.reverse()
            merged = process_line(line)
            if direction == 'down':
                merged.reverse()
            for y in range(size):
                new_grid[y][x] = merged[y]

    return new_grid, moved

# animate & merge tiles:
def move_tiles(window, tiles, clock, direction):
    # 1. Convert current tiles dict to a 2D list of values
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for tile in tiles.values():
        grid[tile.row][tile.col] = tile.value

    # 2. Move/merge using the logic function
    new_grid, moved = move_grid(grid, direction)

    # 3. If nothing moved, check game over
    if not moved:
        if not can_move(grid):
            choice = game_over_popup(window, clock)
            if choice == "restart":
                return "restart"
            return

    # 4. Update tiles based on new_grid
    new_tiles = {}
    for r in range(ROWS):
        for c in range(COLS):
            if new_grid[r][c] != 0:
                new_tiles[f"{r}{c}"] = Tile(new_grid[r][c], r, c)

    # 5. Add one new tile in random empty spot
    empty_positions = [(r, c) for r in range(ROWS) for c in range(COLS) if f"{r}{c}" not in new_tiles]
    if empty_positions:
        r, c = random.choice(empty_positions)
        new_tiles[f"{r}{c}"] = Tile(random.choice([2, 4]), r, c)

    # 6. Replace old tiles with new tiles
    tiles.clear()
    tiles.update(new_tiles)

    # 7. Redraw the window
    draw(window, tiles)


def end_move(tiles):
  if len(tiles) == 16:
    return "lost"
  
  row, col = get_random_pos(tiles)
  tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col) # insert a new tile (2 or 4)
  return "continue"



def update_tiles(window, tiles, sorted_tiles):
  tiles.clear()
  for tile in sorted_tiles:
    tiles[f"{tile.row}{tile.col}"] = tile
  
  draw(window, tiles)

# main loop (event loop):
# main loop (event loop):
def main(window):
    while True:  # outer loop voor restart
        clock = pygame.time.Clock()
        run = True
        tiles = generate_tiles()

        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    result = None
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        result = move_tiles(window, tiles, clock, "left")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        result = move_tiles(window, tiles, clock, "right")
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        result = move_tiles(window, tiles, clock, "up")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        result = move_tiles(window, tiles, clock, "down")

                    if result == "restart":
                        run = False  # stop inner loop om te herstarten
                        break

            draw(window, tiles)

if __name__ == "__main__":
  main(WINDOW) #run the loop on the window
