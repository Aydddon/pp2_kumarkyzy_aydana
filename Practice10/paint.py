import pygame, math

TOOLBAR_H = 70      # height of the toolbar at the top
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Color selection: name -> RGB
COLORS = {
    'black': (0, 0, 0), 'red': (220, 30, 30), 'orange': (255, 140, 0),
    'yellow': (255, 215, 0), 'green': (0, 170, 0), 'blue': (30, 80, 220),
    'purple': (140, 40, 200), 'pink': (255, 105, 180),
}
# keyboard shortcuts for colors
COLOR_KEYS = {
    pygame.K_k: 'black', pygame.K_r: 'red', pygame.K_o: 'orange', pygame.K_y: 'yellow',
    pygame.K_g: 'green', pygame.K_b: 'blue', pygame.K_u: 'purple', pygame.K_p: 'pink',
}
# tools: number key -> name
TOOLS = ['Pencil', 'Rectangle', 'Circle', 'Eraser']


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 13)

    # canvas keeps the finished drawing
    canvas = pygame.Surface((900, 650 - TOOLBAR_H))
    canvas.fill(WHITE)

    # toolbar buttons (tools) and color swatches
    tool_rects = [pygame.Rect(10 + i * 100, 20, 92, 30) for i in range(len(TOOLS))]
    color_rects = {name: pygame.Rect(430 + i * 36, 20, 30, 30)
                   for i, name in enumerate(COLORS)}

    tool = 'Pencil'
    color_name = 'black'
    radius = 5
    drawing = False
    start = (0, 0)     # where the mouse button was pressed
    last = (0, 0)      # previous mouse position

    while True:

        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # determine if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # tools: 1-4
                if pygame.K_1 <= event.key <= pygame.K_4:
                    tool = TOOLS[event.key - pygame.K_1]
                # colors by key
                if event.key in COLOR_KEYS:
                    color_name = COLOR_KEYS[event.key]
                # brush size
                if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    radius = min(50, radius + 1)
                if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if event.pos[1] < TOOLBAR_H:
                    # click on the toolbar: choose tool or color
                    for i, r in enumerate(tool_rects):
                        if r.collidepoint(event.pos):
                            tool = TOOLS[i]
                    for name, r in color_rects.items():
                        if r.collidepoint(event.pos):
                            color_name = name
                else:
                    drawing = True
                    start = last = (event.pos[0], event.pos[1] - TOOLBAR_H)
                    if tool in ('Pencil', 'Eraser'):
                        c = WHITE if tool == 'Eraser' else COLORS[color_name]
                        pygame.draw.circle(canvas, c, start, radius)

            if event.type == pygame.MOUSEMOTION and drawing:
                position = (event.pos[0], event.pos[1] - TOOLBAR_H)
                if tool in ('Pencil', 'Eraser'):
                    # eraser = drawing with the background (white) colour
                    c = WHITE if tool == 'Eraser' else COLORS[color_name]
                    drawLineBetween(canvas, last, position, radius, c)
                    last = position

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                drawing = False
                end = (event.pos[0], event.pos[1] - TOOLBAR_H)
                if tool in ('Rectangle', 'Circle'):
                    # put the finished shape on the canvas
                    drawShape(canvas, tool, start, end, radius, COLORS[color_name])

        # ---- drawing everything ----
        screen.blit(canvas, (0, TOOLBAR_H))

        # live preview of a shape while the mouse is dragged
        if drawing and tool in ('Rectangle', 'Circle'):
            mx, my = pygame.mouse.get_pos()
            preview = canvas.copy()
            drawShape(preview, tool, start, (mx, my - TOOLBAR_H), radius, COLORS[color_name])
            screen.blit(preview, (0, TOOLBAR_H))

        drawToolbar(screen, font, tool_rects, color_rects, tool, color_name, radius)

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(surface, start, end, width, color):
    """Freehand line: circles are drawn along the line so there are no gaps."""
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy), 1)

    for i in range(iterations + 1):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(surface, color, (x, y), width)


def drawShape(surface, tool, start, end, width, color):
    """Draw a rectangle or a circle from the point where the drag started."""
    line = max(1, width // 2)
    if tool == 'Rectangle':
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                           abs(end[0] - start[0]), abs(end[1] - start[1]))
        pygame.draw.rect(surface, color, rect, line)
    elif tool == 'Circle':
        # start = centre, distance to the mouse = radius
        r = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        if r > 0:
            pygame.draw.circle(surface, color, start, r, line)


def drawToolbar(screen, font, tool_rects, color_rects, tool, color_name, radius):
    pygame.draw.rect(screen, (225, 225, 225), (0, 0, 900, TOOLBAR_H))
    for i, r in enumerate(tool_rects):
        pygame.draw.rect(screen, (170, 200, 255) if TOOLS[i] == tool else WHITE, r)
        pygame.draw.rect(screen, BLACK, r, 1)
        screen.blit(font.render("%d %s" % (i + 1, TOOLS[i]), True, BLACK), (r.x + 5, r.y + 7))
    for name, r in color_rects.items():
        pygame.draw.rect(screen, COLORS[name], r)
        pygame.draw.rect(screen, BLACK, r, 3 if name == color_name else 1)
    screen.blit(font.render("Size: %d (+/-)" % radius, True, BLACK), (730, 27))


main()