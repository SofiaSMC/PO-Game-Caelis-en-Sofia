import pygame
import random
import sys

# --- Config ---
SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
WINDOW_SIZE = SIZE * TILE_SIZE + (SIZE + 1) * TILE_MARGIN
FPS = 60

# --- Board & game logic ---
board = [[0]*SIZE for _ in range(SIZE)]
score = 0

def add_tile():
    empty = [(r,c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2

def compress(row):
    row = [n for n in row if n]
    return row + [0]*(SIZE-len(row))

def merge(row):
    global score
    for i in range(SIZE-1):
        if row[i] and row[i] == row[i+1]:
            row[i] *= 2
            score += row[i]
            row[i+1] = 0
    return row

def move_left():
    moved = False
    for r in range(SIZE):
        new = compress(merge(compress(board[r])))
        if new != board[r]:
            moved = True
        board[r] = new
    return moved

def rotate():
    global board
    board = [list(r) for r in zip(*board[::-1])]

def move(turns):
    for _ in range(turns):
        rotate()
    moved = move_left()
    for _ in range((4-turns)%4):
        rotate()
    return moved

# --- Game over check ---
def game_over():
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return False
    for r in range(SIZE):
        for c in range(SIZE-1):
            if board[r][c] == board[r][c+1]:
                return False
    for c in range(SIZE):
        for r in range(SIZE-1):
            if board[r][c] == board[r+1][c]:
                return False
    return True

# --- Colors ---
BACKGROUND_COLOR = (0, 0, 0)
COLORS = {
    0: (40, 40, 40),
    2: (255, 179, 179),
    4: (255, 128, 128),
    8: (255, 102, 102),
    16: (255, 77, 77),
    32: (255, 51, 51),
    64: (255, 26, 26),
    128: (255, 204, 102),
    256: (255, 178, 0),
    512: (255, 153, 0),
    1024: (255, 128, 0),
    2048: (255, 102, 0)
}
TEXT_COLOR = {
    2: (60, 60, 60),
    4: (60, 60, 60),
    8: (255, 255, 255),
    16: (255, 255, 255),
    32: (255, 255, 255),
    64: (255, 255, 255),
    128: (255, 255, 255),
    256: (255, 255, 255),
    512: (255, 255, 255),
    1024: (255, 255, 255),
    2048: (255, 255, 255),
}

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("2048 (Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 40, bold=True)
game_over_font = pygame.font.SysFont("arial", 60, bold=True)
button_font = pygame.font.SysFont("arial", 30, bold=True)

# --- Draw board ---
def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for r in range(SIZE):
        for c in range(SIZE):
            val = board[r][c]
            color = COLORS.get(val, (255, 0, 0))
            x = TILE_MARGIN + c * (TILE_SIZE + TILE_MARGIN)
            y = TILE_MARGIN + r * (TILE_SIZE + TILE_MARGIN)
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)
            
            if val != 0:
                text_color = TEXT_COLOR.get(val, (255, 255, 255))
                text_surface = font.render(str(val), True, text_color)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE/2, y + TILE_SIZE/2))
                screen.blit(text_surface, text_rect)
    
    # score bovenaan
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

# --- Draw game over screen with buttons ---
def draw_game_over():
    screen.fill(BACKGROUND_COLOR)
    # game over tekst
    text_surface = game_over_font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 - 80))
    screen.blit(text_surface, text_rect)
    # score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 - 20))
    screen.blit(score_surface, score_rect)
    # restart knop
    restart_rect = pygame.Rect(WINDOW_SIZE/2 - 100, WINDOW_SIZE/2 + 40, 200, 50)
    pygame.draw.rect(screen, (0, 128, 0), restart_rect, border_radius=8)
    restart_text = button_font.render("Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)
    # quit knop
    quit_rect = pygame.Rect(WINDOW_SIZE/2 - 100, WINDOW_SIZE/2 + 110, 200, 50)
    pygame.draw.rect(screen, (128, 0, 0), quit_rect, border_radius=8)
    quit_text = button_font.render("Quit", True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, quit_text_rect)

    pygame.display.update()
    return restart_rect, quit_rect

# --- Main game loop ---
add_tile()
add_tile()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            moved = False
            if event.key == pygame.K_a:
                moved = move(0)
            elif event.key == pygame.K_s:
                moved = move(1)
            elif event.key == pygame.K_d:
                moved = move(2)
            elif event.key == pygame.K_w:
                moved = move(3)
            if moved:
                add_tile()

    draw_board()
    pygame.display.update()
    clock.tick(FPS)

    if game_over():
        restart_btn, quit_btn = draw_game_over()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.collidepoint(event.pos):
                        # reset game
                        board = [[0]*SIZE for _ in range(SIZE)]
                        score = 0
                        add_tile()
                        add_tile()
                        waiting = False
                    elif quit_btn.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
