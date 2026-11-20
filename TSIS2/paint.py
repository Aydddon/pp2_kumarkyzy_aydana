"""Paint app with freehand, geometry, fill, text, and timestamped PNG saves."""

import sys
from datetime import datetime
from pathlib import Path

import pygame

from tools import SHAPES, draw_shape, flood_fill


WIDTH, HEIGHT = 1100, 820
TOOLBAR_HEIGHT = 136
CANVAS_SIZE = (WIDTH, HEIGHT - TOOLBAR_HEIGHT)
CANVAS_ORIGIN = (0, TOOLBAR_HEIGHT)
WHITE = (255, 255, 255)
DARK = (35, 39, 47)
BUTTON = (55, 61, 73)
BUTTON_ACTIVE = (86, 99, 120)
PALETTE = [
    (25, 25, 30), (220, 45, 50), (40, 105, 215), (30, 155, 90),
    (245, 190, 35), (150, 70, 180), (245, 120, 35), (255, 255, 255),
]
SIZES = (2, 5, 10)
TOOLS = [
    ("Pencil", "P"), ("Line", "L"), ("Rectangle", "R"), ("Circle", "C"),
    ("Eraser", "E"), ("Picker", "K"), ("Fill", "F"), ("Text", "T"),
    ("Square", "Q"), ("Right triangle", "W"), ("Equilateral triangle", "Y"),
    ("Rhombus", "H"),
]
# Short names shown on buttons (tool names used by the logic stay unchanged).
TOOL_LABELS = {
    "Right triangle": "Right tri.",
    "Equilateral triangle": "Eq. triangle",
}

# On Mac the shortcut key is Cmd (META), on Windows/Linux it is Ctrl.
SHORTCUT_MOD = pygame.KMOD_CTRL | pygame.KMOD_META
MOD_NAME = "Cmd" if sys.platform == "darwin" else "Ctrl"

# ---------- Toolbar layout (single source of truth for drawing AND clicks) ----------
MARGIN = 12
GAP = 8
TOOLS_PER_ROW = 6
TOOL_W, TOOL_H = 150, 34

TOOL_RECTS = [
    pygame.Rect(
        MARGIN + (i % TOOLS_PER_ROW) * (TOOL_W + GAP),
        8 + (i // TOOLS_PER_ROW) * (TOOL_H + 6),
        TOOL_W, TOOL_H,
    )
    for i in range(len(TOOLS))
]

ROW3_Y, ROW3_H = 94, 32
SWATCH_RECTS = [
    pygame.Rect(MARGIN + i * 44, ROW3_Y, 36, ROW3_H) for i in range(len(PALETTE))
]
COLOR_PREVIEW_RECT = pygame.Rect(372, ROW3_Y, 36, ROW3_H)
BRUSH_LABEL_POS = (440, ROW3_Y + 8)
SIZE_RECTS = [
    pygame.Rect(520 + i * 88, ROW3_Y, 80, ROW3_H) for i in range(len(SIZES))
]
SAVE_HINT_POS = (800, ROW3_Y + 8)


def canvas_position(mouse_pos: tuple[int, int]) -> tuple[int, int]:
    return mouse_pos[0] - CANVAS_ORIGIN[0], mouse_pos[1] - CANVAS_ORIGIN[1]


def point_on_canvas(pos: tuple[int, int]) -> bool:
    return TOOLBAR_HEIGHT <= pos[1] < HEIGHT and 0 <= pos[0] < WIDTH


def draw_label(screen: pygame.Surface, font: pygame.font.Font, text: str,
               rect: pygame.Rect, color=WHITE) -> None:
    """Draw text centered in rect, shrinking it if it is too wide."""
    surface = font.render(text, True, color)
    max_width = rect.width - 10
    if surface.get_width() > max_width:
        scale = max_width / surface.get_width()
        surface = pygame.transform.smoothscale(
            surface, (max_width, max(1, int(surface.get_height() * scale)))
        )
    screen.blit(surface, surface.get_rect(center=rect.center))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 — Paint")
    canvas = pygame.Surface(CANVAS_SIZE)
    canvas.fill(WHITE)
    preview = canvas.copy()
    font = pygame.font.SysFont(None, 22)
    text_font = pygame.font.SysFont("Arial", 28)
    tool = "Pencil"
    color = PALETTE[0]
    brush_size = 5
    drawing = False
    start_pos: tuple[int, int] | None = None
    previous_pos: tuple[int, int] | None = None
    text_origin: tuple[int, int] | None = None
    text_value = ""
    saved_text = ""
    saved_until = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if text_origin is not None:
                    if event.key == pygame.K_RETURN:
                        if text_value:
                            canvas.blit(text_font.render(text_value, True, color), text_origin)
                        text_origin = None
                        text_value = ""
                        pygame.key.stop_text_input()
                    elif event.key == pygame.K_ESCAPE:
                        text_origin = None
                        text_value = ""
                        pygame.key.stop_text_input()
                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]
                else:
                    if event.key == pygame.K_q and (event.mod & SHORTCUT_MOD):
                        running = False
                    elif event.key == pygame.K_s and (event.mod & SHORTCUT_MOD):
                        filename = f"paint_{datetime.now():%Y%m%d_%H%M%S}.png"
                        pygame.image.save(canvas, Path(__file__).parent / filename)
                        print(f"Saved: {filename}")
                        saved_text = f"Saved: {filename}"
                        saved_until = pygame.time.get_ticks() + 2000
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        brush_size = SIZES[event.key - pygame.K_1]
                    else:
                        key_tools = {getattr(pygame, f"K_{key.lower()}"): name
                                     for name, key in TOOLS}
                        if event.key in key_tools:
                            tool = key_tools[event.key]

            elif event.type == pygame.TEXTINPUT and text_origin is not None:
                text_value += event.text

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    for rect, (name, _) in zip(TOOL_RECTS, TOOLS):
                        if rect.collidepoint(event.pos):
                            tool = name
                    for rect, swatch in zip(SWATCH_RECTS, PALETTE):
                        if rect.collidepoint(event.pos):
                            color = swatch
                    for rect, size in zip(SIZE_RECTS, SIZES):
                        if rect.collidepoint(event.pos):
                            brush_size = size
                elif point_on_canvas(event.pos):
                    local = canvas_position(event.pos)
                    if tool == "Text":
                        text_origin = local
                        text_value = ""
                        pygame.key.start_text_input()
                    elif tool == "Picker":
                        color = tuple(canvas.get_at(local)[:3])
                    elif tool == "Fill":
                        flood_fill(canvas, local, color)
                    elif tool == "Pencil":
                        drawing = True
                        previous_pos = local
                        pygame.draw.circle(canvas, color, local, max(1, brush_size // 2))
                    elif tool == "Eraser":
                        drawing = True
                        previous_pos = local
                        pygame.draw.circle(canvas, WHITE, local, max(1, brush_size // 2))
                    else:
                        drawing = True
                        start_pos = local
                        preview = canvas.copy()

            elif event.type == pygame.MOUSEMOTION and drawing:
                local = canvas_position(event.pos)
                if tool == "Pencil" and previous_pos is not None:
                    pygame.draw.line(canvas, color, previous_pos, local, brush_size)
                    pygame.draw.circle(canvas, color, local, max(1, brush_size // 2))
                    previous_pos = local
                elif tool == "Eraser" and previous_pos is not None:
                    pygame.draw.line(canvas, WHITE, previous_pos, local, brush_size)
                    pygame.draw.circle(canvas, WHITE, local, max(1, brush_size // 2))
                    previous_pos = local
                elif start_pos is not None:
                    preview = canvas.copy()
                    if tool == "Line":
                        pygame.draw.line(preview, color, start_pos, local, brush_size)
                    elif tool in SHAPES:
                        draw_shape(preview, tool, start_pos, local, color, brush_size)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                local = canvas_position(event.pos)
                if tool == "Line" and start_pos is not None:
                    pygame.draw.line(canvas, color, start_pos, local, brush_size)
                elif tool == "Eraser" and previous_pos is not None:
                    pygame.draw.circle(canvas, WHITE, local, max(1, brush_size // 2))
                elif tool in SHAPES and start_pos is not None:
                    draw_shape(canvas, tool, start_pos, local, color, brush_size)
                drawing = False
                start_pos = None
                previous_pos = None
                preview = canvas.copy()

        # ---------- Drawing ----------
        screen.fill((226, 229, 235))
        pygame.draw.rect(screen, DARK, (0, 0, WIDTH, TOOLBAR_HEIGHT))

        # Rows 1-2: tools
        for rect, (name, shortcut) in zip(TOOL_RECTS, TOOLS):
            pygame.draw.rect(screen, BUTTON_ACTIVE if name == tool else BUTTON,
                             rect, border_radius=5)
            label = TOOL_LABELS.get(name, name)
            draw_label(screen, font, f"{label} [{shortcut}]", rect)

        # Row 3: colors
        for rect, swatch in zip(SWATCH_RECTS, PALETTE):
            selected = swatch == color
            pygame.draw.rect(screen, swatch, rect, border_radius=4)
            pygame.draw.rect(screen, (255, 210, 70) if selected else (120, 125, 135),
                             rect, 3 if selected else 1, border_radius=4)

        # Selected color preview
        pygame.draw.rect(screen, color, COLOR_PREVIEW_RECT, border_radius=4)
        pygame.draw.rect(screen, WHITE, COLOR_PREVIEW_RECT, 2, border_radius=4)

        # Brush size buttons
        screen.blit(font.render("Brush size:", True, WHITE), BRUSH_LABEL_POS)
        for index, (rect, size) in enumerate(zip(SIZE_RECTS, SIZES)):
            pygame.draw.rect(screen, BUTTON_ACTIVE if size == brush_size else BUTTON,
                             rect, border_radius=5)
            draw_label(screen, font, f"{size}px [{index + 1}]", rect)

        screen.blit(font.render(f"{MOD_NAME}+S: save PNG", True, (225, 225, 230)),
                    SAVE_HINT_POS)

        # Canvas (preview only while a shape/line is being dragged)
        visible_canvas = preview if drawing and start_pos is not None else canvas
        screen.blit(visible_canvas, CANVAS_ORIGIN)
        pygame.draw.rect(screen, (170, 174, 182), (0, TOOLBAR_HEIGHT, WIDTH, CANVAS_SIZE[1]), 1)
        if text_origin is not None:
            rendered = text_font.render(text_value + "|", True, color)
            screen.blit(rendered, (text_origin[0], text_origin[1] + TOOLBAR_HEIGHT))

        # "Saved" notification (shown for 2 seconds)
        if pygame.time.get_ticks() < saved_until:
            msg = font.render(saved_text, True, WHITE)
            box = msg.get_rect(bottomright=(WIDTH - 12, HEIGHT - 12)).inflate(20, 12)
            pygame.draw.rect(screen, (30, 150, 90), box, border_radius=6)
            screen.blit(msg, msg.get_rect(center=box.center))

        pygame.display.flip()

    pygame.key.stop_text_input()
    pygame.quit()


if __name__ == "__main__":
    main()