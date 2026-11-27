import pygame
import random
import sys

pygame.init()

# ---------- Constants ----------
WIDTH, HEIGHT = 400, 600
FPS = 60
ROAD_LEFT, ROAD_RIGHT = 40, 360          # road borders (grass outside)
GRAY, WHITE, YELLOW = (60, 60, 60), (255, 255, 255), (255, 215, 0)
GREEN, RED, BLUE, BLACK = (34, 139, 34), (200, 30, 30), (30, 80, 200), (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 50)

speed = 5          # how fast enemies, coins and road move (grows over time)
score = 0          # number of enemies dodged
coins = 0          # number of coins collected


def make_car(color):
    """Draw a simple top-down car on a transparent surface and return it."""
    surf = pygame.Surface((40, 70), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, 40, 70), border_radius=8)       # body
    pygame.draw.rect(surf, (150, 200, 255), (6, 14, 28, 16))             # windshield
    pygame.draw.rect(surf, (150, 200, 255), (6, 44, 28, 12))             # rear window
    for y in (6, 50):                                                    # wheels
        pygame.draw.rect(surf, BLACK, (-2, y, 5, 14))
        pygame.draw.rect(surf, BLACK, (37, y, 5, 14))
    return surf


class Player(pygame.sprite.Sprite):
    """The car controlled by the user."""
    def __init__(self):
        super().__init__()
        self.image = make_car(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > ROAD_LEFT:
            self.rect.x -= 6
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < ROAD_RIGHT:
            self.rect.x += 6


class Enemy(pygame.sprite.Sprite):
    """Enemy car that drives down the screen; respawns at the top."""
    def __init__(self):
        super().__init__()
        self.image = make_car(RED)
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.center = (random.randint(ROAD_LEFT + 25, ROAD_RIGHT - 25), -40)

    def update(self):
        global score
        self.rect.y += speed
        if self.rect.top > HEIGHT:        # passed the bottom -> player scores
            score += 1
            self.respawn()


class Coin(pygame.sprite.Sprite):
    """Coin that appears at a random x position and falls with the road."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (12, 12), 12)
        pygame.draw.circle(self.image, (200, 150, 0), (12, 12), 12, 2)
        pygame.draw.circle(self.image, (200, 150, 0), (12, 12), 6, 2)
        self.rect = self.image.get_rect(
            center=(random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20), -20))

    def update(self):
        self.rect.y += speed
        if self.rect.top > HEIGHT:        # missed coin disappears
            self.kill()


def draw_road(offset):
    """Draw grass, road and scrolling dashed lane markings."""
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT, 0, 4, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 4, 0, 4, HEIGHT))
    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + offset, 6, 40))


def game_over():
    """Show the game over screen, then quit."""
    screen.fill(RED)
    screen.blit(font_big.render("Game Over", True, BLACK), (60, 220))
    screen.blit(font_small.render(f"Score: {score}   Coins: {coins}", True, BLACK), (100, 300))
    pygame.display.update()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()


# ---------- Sprites ----------
player = Player()
enemy = Enemy()
all_sprites = pygame.sprite.Group(player, enemy)
enemies = pygame.sprite.Group(enemy)
coin_group = pygame.sprite.Group()

SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 1500)       # try to spawn a coin every 1.5 s
INC_SPEED = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 3000)        # road gets faster every 3 s

road_offset = 0

# ---------- Main loop ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            speed += 0.5
        if event.type == SPAWN_COIN and random.random() < 0.7:   # random appearance
            c = Coin()
            coin_group.add(c)
            all_sprites.add(c)

    road_offset = (road_offset + speed) % 80
    draw_road(road_offset)

    all_sprites.update()
    for s in all_sprites:
        screen.blit(s.image, s.rect)

    # Collect coins
    for _ in pygame.sprite.spritecollide(player, coin_group, True):
        coins += 1

    # HUD: score top-left, coins top-right
    screen.blit(font_small.render(f"Score: {score}", True, WHITE), (10, 10))
    coin_text = font_small.render(f"Coins: {coins}", True, YELLOW)
    screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10))

    # Crash with enemy
    if pygame.sprite.spritecollideany(player, enemies):
        game_over()

    pygame.display.update()
    clock.tick(FPS)