import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 900, 650
TOOLBAR_H = 70
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 14)

WHITE, BLACK, LIGHT = (255, 255, 255), (0, 0, 0), (225, 225, 225)
PALETTE = [(0, 0, 0), (255, 255, 255), (220, 30, 30), (255, 140, 0), (255, 215, 0),
           (0, 170, 0), (0, 200, 200), (30, 80, 220), (140, 40, 200), (255, 105, 180),
           (120, 70, 30), (128, 128, 128)]

# Canvas holds the finished drawing (everything below the toolbar)
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill(WHITE)

# Toolbar buttons: name -> (rect, key shortcut)
TOOLS = {"Pencil": (pygame.Rect(10, 10, 80, 26), pygame.K_p),
         "Rect": (pygame.Rect(10, 40, 80, 26), pygame.K_r),
         "Circle": (pygame.Rect(100, 10, 80, 26), pygame.K_c),
         "Eraser": (pygame.Rect(100, 40, 80, 26), pygame.K_e)}
swatches = [(pygame.Rect(210 + (i % 6) * 36, 8 + (i // 6) * 31, 30, 26), c)
            for i, c in enumerate(PALETTE)]

tool, color, size = "Pencil", BLACK, 5
drawing = False
start = (0, 0)       # where the mouse was pressed (for shapes)
last = (0, 0)        # previous mouse position (for freehand lines)


def to_canvas(pos):
    """Convert window coordinates to canvas coordinates."""
    return pos[0], pos[1] - TOOLBAR_H


def draw_shape(surface, tool, c, p1, p2):
    """Draw a rectangle or circle defined by drag start p1 and current p2."""
    if tool == "Rect":
        rect = pygame.Rect(min(p1[0], p2[0]), min(p1[1], p2[1]),
                           abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
        pygame.draw.rect(surface, c, rect, max(1, size // 2))
    elif tool == "Circle":
        radius = int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]))   # center = start point
        if radius > 0:
            pygame.draw.circle(surface, c, p1, radius, max(1, size // 2))


def draw_line_smooth(surface, c, p1, p2, width):
    """Freehand stroke: circles along the line so there are no gaps."""
    dist = max(1, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1])))
    for i in range(dist + 1):
        t = i / dist
        x = int(p1[0] + (p2[0] - p1[0]) * t)
        y = int(p1[1] + (p2[1] - p1[1]) * t)
        pygame.draw.circle(surface, c, (x, y), width)


def draw_toolbar():
    pygame.draw.rect(screen, LIGHT, (0, 0, WIDTH, TOOLBAR_H))
    for name, (rect, key) in TOOLS.items():
        pygame.draw.rect(screen, (170, 200, 255) if name == tool else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        label = f"{name} ({pygame.key.name(key).upper()})"
        screen.blit(font.render(label, True, BLACK), (rect.x + 4, rect.y + 5))
    for rect, c in swatches:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 3 if c == color else 1)
    # Current color + size preview
    pygame.draw.rect(screen, color, (450, 10, 40, 40))
    pygame.draw.rect(screen, BLACK, (450, 10, 40, 40), 1)
    screen.blit(font.render(f"Size: {size}  (+/-)", True, BLACK), (500, 22))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            for name, (_, key) in TOOLS.items():       # keyboard tool shortcuts
                if event.key == key:
                    tool = name
            if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                size = min(50, size + 1)
            if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                size = max(1, size - 1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] < TOOLBAR_H:               # click on the toolbar
                for name, (rect, _) in TOOLS.items():
                    if rect.collidepoint(event.pos):
                        tool = name
                for rect, c in swatches:               # color selection
                    if rect.collidepoint(event.pos):
                        color = c
            else:                                      # start drawing on canvas
                drawing = True
                start = last = to_canvas(event.pos)
                if tool in ("Pencil", "Eraser"):
                    c = WHITE if tool == "Eraser" else color
                    pygame.draw.circle(canvas, c, start, size)

        elif event.type == pygame.MOUSEMOTION and drawing:
            pos = to_canvas(event.pos)
            if tool in ("Pencil", "Eraser"):
                c = WHITE if tool == "Eraser" else color    # eraser paints white
                draw_line_smooth(canvas, c, last, pos, size)
                last = pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            drawing = False
            if tool in ("Rect", "Circle"):             # commit the shape to canvas
                draw_shape(canvas, tool, color, start, to_canvas(event.pos))

    # ---- Render ----
    screen.blit(canvas, (0, TOOLBAR_H))
    # Live preview of shape while dragging (not yet committed)
    if drawing and tool in ("Rect", "Circle"):
        preview = canvas.copy()
        draw_shape(preview, tool, color, start, to_canvas(pygame.mouse.get_pos()))
        screen.blit(preview, (0, TOOLBAR_H))
    draw_toolbar()

    pygame.display.flip()
    clock.tick(120)