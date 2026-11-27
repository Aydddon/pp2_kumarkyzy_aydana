"""Drawing and flood-fill helpers for the paint application."""

from collections import deque

import pygame


SHAPES = {
    "Rectangle", "Circle", "Square", "Right triangle",
    "Equilateral triangle", "Rhombus",
}


def normalized_rect(start: tuple[int, int], end: tuple[int, int]) -> pygame.Rect:
    """Return a rectangle spanning two points in any drag direction."""
    return pygame.Rect(start, (end[0] - start[0], end[1] - start[1])).normalize()


def shape_points(name: str, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    """Build polygon vertices for the non-circular shape tools."""
    x1, y1 = start
    x2, y2 = end
    if name == "Square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        x2 = x1 + (side if x2 >= x1 else -side)
        y2 = y1 + (side if y2 >= y1 else -side)
        return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    if name == "Right triangle":
        return [(x1, y1), (x2, y2), (x1, y2)]
    rect = normalized_rect(start, end)
    if name == "Equilateral triangle":
        # Use the available width and derive the correct equilateral height.
        half_width = rect.width // 2
        height = round(rect.width * 0.8660254)
        top = (rect.centerx, rect.bottom if end[1] < start[1] else rect.top)
        base_y = top[1] - height if top[1] == rect.bottom else top[1] + height
        return [(top[0], top[1]), (rect.left, base_y), (rect.right, base_y)]
    if name == "Rhombus":
        return [rect.midtop, rect.midright, rect.midbottom, rect.midleft]
    return []


def draw_shape(surface: pygame.Surface, name: str, start: tuple[int, int],
               end: tuple[int, int], color: tuple[int, int, int], width: int) -> None:
    """Draw an outlined shape with the active stroke thickness."""
    if name == "Circle":
        radius = round(pygame.Vector2(end).distance_to(start))
        if radius:
            pygame.draw.circle(surface, color, start, radius)
    elif name == "Rectangle":
        rect = normalized_rect(start, end)
        if rect.width and rect.height:
            pygame.draw.rect(surface, color, rect, width)
    else:
        points = shape_points(name, start, end)
        if points and len(set(points)) >= 3:
            pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface: pygame.Surface, point: tuple[int, int],
               replacement: tuple[int, int, int]) -> bool:
    """Replace a connected region with an exact-color, iterative scanline fill.

    A scanline queue avoids Python recursion limits and groups neighboring pixels
    into spans so large regions need less queue storage than a pixel queue.
    """
    width, height = surface.get_size()
    x, y = point
    if not (0 <= x < width and 0 <= y < height):
        return False
    target = surface.get_at((x, y))
    replacement_rgba = (*replacement, 255)
    if tuple(target) == replacement_rgba:
        return False

    queue = deque([(x, y)])
    while queue:
        seed_x, seed_y = queue.pop()
        if surface.get_at((seed_x, seed_y)) != target:
            continue

        left = seed_x
        while left > 0 and surface.get_at((left - 1, seed_y)) == target:
            left -= 1
        right = seed_x
        while right + 1 < width and surface.get_at((right + 1, seed_y)) == target:
            right += 1
        pygame.draw.line(surface, replacement, (left, seed_y), (right, seed_y))

        for adjacent_y in (seed_y - 1, seed_y + 1):
            if not 0 <= adjacent_y < height:
                continue
            scan_x = left
            while scan_x <= right:
                if surface.get_at((scan_x, adjacent_y)) == target:
                    queue.append((scan_x, adjacent_y))
                    scan_x += 1
                    while scan_x <= right and surface.get_at((scan_x, adjacent_y)) == target:
                        scan_x += 1
                else:
                    scan_x += 1
    return True
