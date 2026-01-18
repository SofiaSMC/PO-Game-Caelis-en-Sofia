import pygame
import random
import math

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


# animate & merge tiles:
def move_tiles(window, tiles, clock, direction):
  updated = True
  blocks = set() # so you don't re-merge the same tiles per one move
  
  if direction == "left":
    sort_func = lambda x: x.col # merge in the correct order (in opposite to the movement). lambda is a one-call function
    reverse = False # asc or desc order sorting
    delta = (-MOVE_VEL, 0) # will move you to the left
    boundary_check = lambda tile: tile.col == 0 # have you hit the boundary? (end of the screen)
    get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}") # if no other tile: returns None
    merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL # should I merge based on the curr. movement of the tile
    move_check = (
      lambda tile, next_tile: tile.x > next_tile.x +RECT_WIDTH + MOVE_VEL # when you shouldn't merge
    )

    ceil = True

  # elif direction == "right":
  #   # sort_func = lambda x: x.col # merge in the correct order (in opposite to the movement). lambda is a one-call function
  #   # reverse = True # asc sorting
  #   # delta = (MOVE_VEL, 0)
  #   # boundary_check = lambda tile: tile.col == COLS - 1 # becomes COLS - 1
  #   # get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}") # plus 1
  #   # merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL # lesser than sign
  #   # lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x # other order bc right

  #   # ceil = False
  elif direction == "right":
    sort_func = lambda x: x.col
    reverse = True
    delta = (MOVE_VEL, 0)
    boundary_check = lambda tile: tile.col == COLS - 1
    get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
    merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
    move_check = (
        lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
    )
    ceil = False

  elif direction == "up":
    sort_func = lambda x: x.row
    reverse = False
    delta = (0, -MOVE_VEL)
    boundary_check = lambda tile: tile.row == 0
    get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
    merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
    move_check = (
        lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
    )
    ceil = True
  
  elif direction == "down":
    sort_func = lambda x: x.row
    reverse = True
    delta = (0, MOVE_VEL)
    boundary_check = lambda tile: tile.row == ROWS - 1
    get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
    merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
    move_check = (
        lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
    )
    ceil = False


  while updated:
    clock.tick(FPS)
    updated = False
    sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

    for i, tile in enumerate(sorted_tiles):
      if boundary_check(tile):
        continue

      next_tile = get_next_tile(tile)
      if not next_tile:
        tile.move(delta)
    
      elif (
        tile.value == next_tile.value
        and tile not in blocks
        and next_tile not in blocks
      ):
        if merge_check(tile, next_tile):
          tile.move(delta)
        else:
          next_tile.value *= 2
          sorted_tiles.pop(i)
          blocks.add(next_tile)
      
      elif move_check(tile, next_tile):
        tile.move(delta)
    
      else:
        continue

      tile.set_pos(ceil)
      updated = True

    update_tiles(window, tiles, sorted_tiles)

  return end_move(tiles)

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
def main(window):
  clock = pygame.time.Clock()
  run = True

  tiles = generate_tiles()  # example: "00": Tile(2, 0, 0), "20": Tile(2, 2, 0)
  while run:
    clock.tick(FPS) # so that it runs once every 60s. otherwise different laptops = different speed

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break

      # check for keypresses:
      if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_LEFT, pygame.K_a):
          move_tiles(window, tiles, clock, "left")

        elif event.key in (pygame.K_RIGHT, pygame.K_d):
          move_tiles(window, tiles, clock, "right")

        elif event.key in (pygame.K_UP, pygame.K_w):
          move_tiles(window, tiles, clock, "up")

        elif event.key in (pygame.K_DOWN, pygame.K_s):
          move_tiles(window, tiles, clock, "down")
      
      
    
    draw(window, tiles)
  
  pygame.quit()

if __name__ == "__main__":
  main(WINDOW) #run the loop on the window