import pygame
import random
import sys

pygame.init()

# ---------- Constants ----------
CELL = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
GREEN, DARK_GREEN = (0, 200, 0), (0, 130, 0)
RED, GRAY = (220, 30, 30), (110, 110, 110)
POINTS_PER_LEVEL = 5
BASE_FPS, FPS_STEP = 5, 2

# Food types: weight (points + growth), colour, lifetime in ms, spawn chance.
# Heavier food is rarer and disappears faster.
FOOD_TYPES = [
    {"weight": 1, "color": (220, 30, 30),  "life": 9000, "chance": 60},   # red
    {"weight": 2, "color": (255, 165, 0),  "life": 6000, "chance": 30},   # orange
    {"weight": 3, "color": (180, 60, 255), "life": 4000, "chance": 10},   # purple
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 12, bold=True)
font_big = pygame.font.SysFont("Verdana", 40)

# Walls = outer ring of the grid
walls = {(x, y) for x in range(COLS) for y in range(ROWS)
         if x in (0, COLS - 1) or y in (0, ROWS - 1)}


def spawn_food(snake):
    """Create a random weighted food on a free cell (not wall, not snake)."""
    free = [(x, y) for x in range(COLS) for y in range(ROWS)
            if (x, y) not in walls and (x, y) not in snake]
    kind = random.choices(FOOD_TYPES, weights=[t["chance"] for t in FOOD_TYPES])[0]
    return {"pos": random.choice(free), "weight": kind["weight"], "color": kind["color"],
            "life": kind["life"], "born": pygame.time.get_ticks()}   # born = spawn time


def new_game():
    snake = [(COLS // 2, ROWS // 2)]
    return {"snake": snake, "dir": (1, 0), "score": 0, "level": 1, "fps": BASE_FPS,
            "grow": 0,                      # segments still to add after eating
            "alive": True, "food": spawn_food(snake)}


def draw(state):
    screen.fill(BLACK)
    for x, y in walls:
        pygame.draw.rect(screen, GRAY, (x * CELL, y * CELL, CELL, CELL))

    # Food with weight label and a shrinking timer bar showing remaining life
    f = state["food"]
    fx, fy = f["pos"]
    pygame.draw.rect(screen, f["color"], (fx * CELL + 1, fy * CELL + 1, CELL - 2, CELL - 2))
    label = font_small.render(str(f["weight"]), True, WHITE)
    screen.blit(label, label.get_rect(center=(fx * CELL + CELL // 2, fy * CELL + CELL // 2)))
    left = max(0, 1 - (pygame.time.get_ticks() - f["born"]) / f["life"])
    pygame.draw.rect(screen, WHITE, (fx * CELL, fy * CELL - 4, int(CELL * left), 3))

    for i, (x, y) in enumerate(state["snake"]):
        pygame.draw.rect(screen, GREEN if i == 0 else DARK_GREEN, (x * CELL, y * CELL, CELL, CELL))
        pygame.draw.rect(screen, BLACK, (x * CELL, y * CELL, CELL, CELL), 1)

    hud = font.render(f"Score: {state['score']}    Level: {state['level']}", True, WHITE)
    screen.blit(hud, (10, ROWS * CELL + 8))


def step(state):
    """One game tick: expire food, move, collide, eat."""
    # Timer: if the food lived too long, replace it with a new one
    f = state["food"]
    if pygame.time.get_ticks() - f["born"] > f["life"]:
        state["food"] = spawn_food(state["snake"])

    dx, dy = state["dir"]
    hx, hy = state["snake"][0]
    head = (hx + dx, hy + dy)

    if head in walls or head in state["snake"]:       # wall or self collision
        state["alive"] = False
        return

    state["snake"].insert(0, head)
    if head == state["food"]["pos"]:
        w = state["food"]["weight"]
        state["score"] += w
        state["grow"] += w - 1                        # head already added 1 segment
        state["food"] = spawn_food(state["snake"])
        # Level depends on score; higher level = faster snake
        state["level"] = 1 + state["score"] // POINTS_PER_LEVEL
        state["fps"] = BASE_FPS + (state["level"] - 1) * FPS_STEP
    elif state["grow"] > 0:
        state["grow"] -= 1                            # grow: keep the tail this tick
    else:
        state["snake"].pop()


state = new_game()
pending_dir = state["dir"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            d = state["dir"]
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