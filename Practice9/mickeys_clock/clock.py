"""Drawing helpers and time-to-angle calculations for the clock."""

from datetime import datetime
import math

import pygame


BACKGROUND = (245, 239, 222)
BLACK = (25, 25, 25)
FACE = (255, 250, 235)
RED = (205, 42, 46)
BLUE = (49, 112, 181)


def hand_angles(now: datetime) -> tuple[float, float]:
    """Return clockwise angles from 12 o'clock for (minute, second) hands."""
    minute_angle = ((now.minute % 60) + now.second / 60) * 6
    second_angle = now.second * 6
    return minute_angle, second_angle


def _draw_hand(surface: pygame.Surface, center: tuple[int, int], angle: float,
               color: tuple[int, int, int], length: int, width: int) -> None:
    """Draw a rounded hand, converting clock angles to screen coordinates."""
    import math

    radians = math.radians(angle - 90)
    end = (center[0] + round(math.cos(radians) * length),
           center[1] + round(math.sin(radians) * length))
    pygame.draw.line(surface, color, center, end, width)
    pygame.draw.circle(surface, color, end, width // 2)


def draw_clock(surface: pygame.Surface, now: datetime, font: pygame.font.Font) -> None:
    """Render a Mickey-inspired clock with a digital minute:second readout."""
    surface.fill(BACKGROUND)
    center = (400, 265)

    # Simple ears and face make the clock recognizable without image assets.
    pygame.draw.circle(surface, BLACK, (center[0] - 105, center[1] - 105), 88)
    pygame.draw.circle(surface, BLACK, (center[0] + 105, center[1] - 105), 88)
    pygame.draw.circle(surface, BLACK, center, 170)
    pygame.draw.circle(surface, FACE, center, 158)

    for tick in range(60):
        angle = math_radians(tick * 6 - 90)
        outer, inner = 145, 132 if tick % 5 == 0 else 138
        start = (center[0] + round(math.cos(angle) * inner),
                 center[1] + round(math.sin(angle) * inner))
        end = (center[0] + round(math.cos(angle) * outer),
               center[1] + round(math.sin(angle) * outer))
        pygame.draw.line(surface, BLACK, start, end, 3 if tick % 5 == 0 else 1)

    minute_angle, second_angle = hand_angles(now)
    # The right arm is the minute hand; the left arm is the second hand.
    _draw_hand(surface, center, minute_angle, BLUE, 106, 15)
    _draw_hand(surface, center, second_angle, RED, 128, 9)
    pygame.draw.circle(surface, BLACK, center, 12)

    time_text = font.render(now.strftime("%M:%S"), True, BLACK)
    surface.blit(time_text, time_text.get_rect(center=(400, 505)))
    hint = pygame.font.Font(None, 25).render("RIGHT HAND: MINUTES   LEFT HAND: SECONDS", True, BLACK)
    surface.blit(hint, hint.get_rect(center=(400, 550)))


def math_radians(degrees: float) -> float:
    """Convert degrees to radians (kept local to avoid extra dependencies)."""
    import math

    return math.radians(degrees)
