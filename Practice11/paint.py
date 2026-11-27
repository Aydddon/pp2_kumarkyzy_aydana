import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 900, 650
TOOLBAR_H = 70
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 12)

WHITE, BLACK, LIGHT = (255, 255, 255), (0, 0, 0), (225, 225, 225)
PALETTE = [(0, 0, 0), (255, 255, 255), (220, 30, 30), (255, 140, 0), (255, 215, 0),
           (0, 170, 0), (0, 200, 200), (30, 80, 220), (140, 40, 200), (255, 105, 180),
           (120, 70, 30), (128, 128, 128)]

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill(WHITE)

# Toolbar buttons laid out in 4 columns x 2 rows: name -> (label, key)
TOOL_DEFS = [("Pencil", pygame.K_p), ("Rect", pygame.K_r), ("Circle", pygame.K_c),
             ("Eraser", pygame.K_e), ("Square", pygame.K_s), ("R.Triangle", pygame.K_t),
             ("Eq.Triangle", pygame.K_g), ("Rhombus", pygame.K_h)]
TOOLS = {}
for i, (name, key) in enumerate(TOOL_DEFS):
    TOOLS[name] = (pygame.Rect(10 + (i % 4) * 95, 8 + (i // 4) * 31, 90, 26), key)

swatches = [(pygame.Rect(410 + (i % 6) * 36, 8 + (i // 6) * 31, 30, 26), c)
            for i, c in enumerate(PALETTE)]

tool, color, size = "Pencil", BLACK, 5
drawing = False
start = (0, 0)
last = (0, 0)


def to_canvas(pos):
    """Window coordinates -> canvas coordinates."""
    return pos[0], pos[1] - TOOLBAR_H


def shape_points(tool, p1, p2):
    """Return the list of polygon vertices for a shape dragged from p1 to p2."""
    x1, y1 = p1
    x2, y2 = p2
    if tool == "Square":
        # Side = larger drag distance; signs keep the square in the drag direction
        side = max(abs(x2 - x1), abs(y2 - y1))
        sx = 1 if x2 >= x1 else -1
        sy = 1 if y2 >= y1 else -1
        return [(x1, y1), (x1 + sx * side, y1), (x1 + sx * side, y1 + sy * side),
                (x1, y1 + sy * side)]
    if tool == "R.Triangle":
        # Right angle sits at (x1, y2); legs are vertical and horizontal
        return [(x1, y1), (x1, y2), (x2, y2)]
    if tool == "Eq.Triangle":
        # Base is horizontal from (x1,y1) to (x2,y1); apex height = base * sqrt(3)/2
        base = abs(x2 - x1)
        h = base * math.sqrt(3) / 2
        apex_y = y1 - h if y2 <= y1 else y1 + h       # apex points toward drag direction
        return [(x1, y1), (x2, y1), ((x1 + x2) / 2, apex_y)]
    if tool == "Rhombus":
        # Vertices are the midpoints of the drag bounding box's sides
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        return [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    return []


def draw_shape(surface, tool, c, p1, p2):
    """Draw any shape tool (outline) onto the given surface."""
    width = max(1, size // 2)
    if tool == "Rect":
        rect = pygame.Rect(min(p1[0], p2[0]), min(p1[1], p2[1]),
                           abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
        pygame.draw.rect(surface, c, rect, width)
    elif tool == "Circle":
        radius = int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]))
        if radius > 0:
            pygame.draw.circle(surface, c, p1, radius, width)
    elif tool in ("Square", "R.Triangle", "Eq.Triangle", "Rhombus"):
        pts = shape_points(tool, p1, p2)
        if len(pts) >= 3 and p1 != p2:
            pygame.draw.polygon(surface, c, pts, width)


SHAPE_TOOLS = ("Rect", "Circle", "Square", "R.Triangle", "Eq.Triangle", "Rhombus")


def draw_line_smooth(surface, c, p1, p2, width):
    """Freehand stroke made of circles so fast movement leaves no gaps."""
    dist = max(1, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1])))
    for i in range(dist + 1):
        t = i / dist
        pygame.draw.circle(surface, c, (int(p1[0] + (p2[0] - p1[0]) * t),
                                        int(p1[1] + (p2[1] - p1[1]) * t)), width)


def draw_toolbar():
    pygame.draw.rect(screen, LIGHT, (0, 0, WIDTH, TOOLBAR_H))
    for name, (rect, key) in TOOLS.items():
        pygame.draw.rect(screen, (170, 200, 255) if name == tool else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        screen.blit(font.render(f"{name} ({pygame.key.name(key).upper()})", True, BLACK),
                    (rect.x + 3, rect.y + 6))
    for rect, c in swatches:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 3 if c == color else 1)
    pygame.draw.rect(screen, color, (640, 10, 40, 40))
    pygame.draw.rect(screen, BLACK, (640, 10, 40, 40), 1)
    screen.blit(font.render(f"Size: {size} (+/-)", True, BLACK), (690, 22))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            for name, (_, key) in TOOLS.items():
                if event.key == key:
                    tool = name
            if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                size = min(50, size + 1)
            if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                size = max(1, size - 1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] < TOOLBAR_H:
                for name, (rect, _) in TOOLS.items():
                    if rect.collidepoint(event.pos):
                        tool = name
                for rect, c in swatches:
                    if rect.collidepoint(event.pos):
                        color = c
            else:
                drawing = True
                start = last = to_canvas(event.pos)
                if tool in ("Pencil", "Eraser"):
                    pygame.draw.circle(canvas, WHITE if tool == "Eraser" else color, start, size)

        elif event.type == pygame.MOUSEMOTION and drawing:
            pos = to_canvas(event.pos)
            if tool in ("Pencil", "Eraser"):
                draw_line_smooth(canvas, WHITE if tool == "Eraser" else color, last, pos, size)
                last = pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            drawing = False
            if tool in SHAPE_TOOLS:                    # commit shape to the canvas
                draw_shape(canvas, tool, color, start, to_canvas(event.pos))

    screen.blit(canvas, (0, TOOLBAR_H))
    if drawing and tool in SHAPE_TOOLS:                # live preview while dragging
        preview = canvas.copy()
        draw_shape(preview, tool, color, start, to_canvas(pygame.mouse.get_pos()))
        screen.blit(preview, (0, TOOLBAR_H))
    draw_toolbar()

    pygame.display.flip()
    clock.tick(120)