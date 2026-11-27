import pygame
import random
import sys

pygame.init()

# ---------- Constants ----------
CELL = 20                       # size of one grid cell in pixels
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40   # extra 40px for the HUD
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
GREEN, DARK_GREEN = (0, 200, 0), (0, 130, 0)
RED, GRAY = (220, 30, 30), (110, 110, 110)
FOODS_PER_LEVEL = 3             # foods needed to reach the next level
BASE_FPS, FPS_STEP = 5, 2       # starting speed and speed gain per level

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 40)

# Walls = the outer ring of the grid
walls = {(x, y) for x in range(COLS) for y in range(ROWS)
         if x in (0, COLS - 1) or y in (0, ROWS - 1)}


def new_game():
    """Return a fresh game state dictionary."""
    snake = [(COLS // 2, ROWS // 2)]            # list of (x, y) cells, head first
    state = {"snake": snake, "dir": (1, 0), "score": 0, "level": 1,
             "eaten": 0, "fps": BASE_FPS, "alive": True}
    state["food"] = random_food(snake)
    return state


def random_food(snake):
    """Pick a random cell that is neither a wall nor part of the snake."""
    free = [(x, y) for x in range(COLS) for y in range(ROWS)
            if (x, y) not in walls and (x, y) not in snake]
    return random.choice(free)


def draw(state):
    screen.fill(BLACK)
    # Walls
    for x, y in walls:
        pygame.draw.rect(screen, GRAY, (x * CELL, y * CELL, CELL, CELL))
    # Food
    fx, fy = state["food"]
    pygame.draw.rect(screen, RED, (fx * CELL + 2, fy * CELL + 2, CELL - 4, CELL - 4))
    # Snake (head brighter than body)
    for i, (x, y) in enumerate(state["snake"]):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))
        pygame.draw.rect(screen, BLACK, (x * CELL, y * CELL, CELL, CELL), 1)
    # HUD
    hud = font.render(f"Score: {state['score']}    Level: {state['level']}", True, WHITE)
    screen.blit(hud, (10, ROWS * CELL + 8))


def step(state):
    """Advance the game by one tick: move, check collisions, eat food."""
    dx, dy = state["dir"]
    hx, hy = state["snake"][0]
    head = (hx + dx, hy + dy)

    # Border/wall collision or hitting itself -> game over
    if head in walls or head in state["snake"]:
        state["alive"] = False
        return

    state["snake"].insert(0, head)
    if head == state["food"]:
        state["score"] += 1
        state["eaten"] += 1
        state["food"] = random_food(state["snake"])
        # Level up every FOODS_PER_LEVEL foods and speed the game up
        if state["eaten"] % FOODS_PER_LEVEL == 0:
            state["level"] += 1
            state["fps"] += FPS_STEP
    else:
        state["snake"].pop()                     # no food: tail follows the head


state = new_game()
pending_dir = state["dir"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            d = state["dir"]
            # Disallow reversing directly into yourself
            if event.key == pygame.K_UP and d != (0, 1):
                pending_dir = (0, -1)
            elif event.key == pygame.K_DOWN and d != (0, -1):
                pending_dir = (0, 1)
            elif event.key == pygame.K_LEFT and d != (1, 0):
                pending_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT and d != (-1, 0):
                pending_dir = (1, 0)
            elif event.key == pygame.K_r and not state["alive"]:
                state = new_game()
                pending_dir = state["dir"]

    if state["alive"]:
        state["dir"] = pending_dir
        step(state)

    draw(state)
    if not state["alive"]:
        text = font_big.render("GAME OVER", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        sub = font.render("Press R to restart", True, WHITE)
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

    pygame.display.flip()
    clock.tick(state["fps"])