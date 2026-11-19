"""Arrow-key ball movement demonstration."""

import pygame

from ball import Ball


def main() -> None:
    pygame.init()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Ball")
    timer = pygame.time.Clock()
    ball = Ball(width // 2, height // 2, width, height)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_UP:
                    ball.move(0, -Ball.STEP)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, Ball.STEP)
                elif event.key == pygame.K_LEFT:
                    ball.move(-Ball.STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(Ball.STEP, 0)

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (220, 30, 40), (ball.x, ball.y), Ball.RADIUS)
        pygame.display.flip()
        timer.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
