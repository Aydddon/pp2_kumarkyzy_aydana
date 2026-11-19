"""Launch the Mickey-inspired digital clock."""

from datetime import datetime

import pygame

from clock import draw_clock


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mickey's Clock")
    font = pygame.font.Font(None, 64)
    timer = pygame.time.Clock()
    running = True
    last_second = -1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        now = datetime.now()
        if now.second != last_second:
            draw_clock(screen, now, font)
            pygame.display.flip()
            last_second = now.second
        timer.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
