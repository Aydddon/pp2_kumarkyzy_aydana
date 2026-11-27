import pygame
import random
import sys

pygame.init()

# ---------- Constants ----------
WIDTH, HEIGHT = 400, 600
FPS = 60
ROAD_LEFT, ROAD_RIGHT = 40, 360
GRAY, WHITE, YELLOW = (60, 60, 60), (255, 255, 255), (255, 215, 0)
GREEN, RED, BLUE, BLACK = (34, 139, 34), (200, 30, 30), (30, 80, 200), (0, 0, 0)

N_COINS_FOR_SPEEDUP = 5     # "N": enemy gets faster every N coins earned
ENEMY_SPEED_STEP = 1        # how much faster the enemy gets each time

# Coin types: weight (value), radius, colour, spawn probability.
# Heavier coins are bigger, differently coloured and rarer.
COIN_TYPES = [
    {"weight": 1, "radius": 10, "color": (205, 127, 50),  "chance": 60},   # bronze
    {"weight": 2, "radius": 13, "color": (192, 192, 192), "chance": 30},   # silver
    {"weight": 3, "radius": 16, "color": (255, 215, 0),   "chance": 10},   # gold
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 20)
font_coin = pygame.font.SysFont("Verdana", 12, bold=True)
font_big = pygame.font.SysFont("Verdana", 50)

road_speed = 5              # speed of the road and falling coins
enemy_speed = 5             # speed of the enemy (grows with collected coins)
score = 0                   # enemies dodged
coins = 0                   # total coin value collected
next_speedup = N_COINS_FOR_SPEEDUP   # coin total at which enemy speeds up next


def make_car(color):
    """Draw a simple top-down car on a transparent surface."""
    surf = pygame.Surface((40, 70), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, 40, 70), border_radius=8)
    pygame.draw.rect(surf, (150, 200, 255), (6, 14, 28, 16))
    pygame.draw.rect(surf, (150, 200, 255), (6, 44, 28, 12))
    for y in (6, 50):
        pygame.draw.rect(surf, BLACK, (-2, y, 5, 14))
        pygame.draw.rect(surf, BLACK, (37, y, 5, 14))
    return surf


class Player(pygame.sprite.Sprite):
    """Car controlled by the user."""
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
    """Enemy car; its speed depends on the global enemy_speed."""
    def __init__(self):
        super().__init__()
        self.image = make_car(RED)
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.center = (random.randint(ROAD_LEFT + 25, ROAD_RIGHT - 25), -40)

    def update(self):
        global score
        self.rect.y += enemy_speed
        if self.rect.top > HEIGHT:
            score += 1
            self.respawn()


class Coin(pygame.sprite.Sprite):
    """Coin with a random weight; weight decides look and value."""
    def __init__(self):
        super().__init__()
        # random.choices picks a type using the 'chance' values as probabilities
        kind = random.choices(COIN_TYPES, weights=[t["chance"] for t in COIN_TYPES])[0]
        self.weight = kind["weight"]
        r = kind["radius"]
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, kind["color"], (r, r), r)
        pygame.draw.circle(self.image, BLACK, (r, r), r, 2)
        label = font_coin.render(str(self.weight), True, BLACK)   # show weight on coin
        self.image.blit(label, label.get_rect(center=(r, r)))
        self.rect = self.image.get_rect(
            center=(random.randint(ROAD_LEFT + 25, ROAD_RIGHT - 25), -20))

    def update(self):
        self.rect.y += road_speed
        if self.rect.top > HEIGHT:
            self.kill()


def draw_road(offset):
    """Draw grass, road and scrolling dashed centre line."""
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT, 0, 4, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 4, 0, 4, HEIGHT))
    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + offset, 6, 40))


def game_over():
    screen.fill(RED)
    screen.blit(font_big.render("Game Over", True, BLACK), (60, 220))
    screen.blit(font_small.render(f"Score: {score}   Coins: {coins}", True, BLACK), (100, 300))
    pygame.display.update()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()


player = Player()
enemy = Enemy()
all_sprites = pygame.sprite.Group(player, enemy)
enemies = pygame.sprite.Group(enemy)
coin_group = pygame.sprite.Group()

SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 1200)       # chance to spawn a coin every 1.2 s

road_offset = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_COIN and random.random() < 0.75:
            c = Coin()
            coin_group.add(c)
            all_sprites.add(c)

    road_offset = (road_offset + road_speed) % 80
    draw_road(road_offset)

    all_sprites.update()
    for s in all_sprites:
        screen.blit(s.image, s.rect)

    # Collect coins: add each coin's weight, then check for enemy speed-up
    for c in pygame.sprite.spritecollide(player, coin_group, True):
        coins += c.weight
    while coins >= next_speedup:                 # 'while' in case a heavy coin skips a threshold
        enemy_speed += ENEMY_SPEED_STEP
        next_speedup += N_COINS_FOR_SPEEDUP

    # HUD
    screen.blit(font_small.render(f"Score: {score}", True, WHITE), (10, 10))
    coin_text = font_small.render(f"Coins: {coins}", True, YELLOW)
    screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10))
    screen.blit(font_coin.render(f"Enemy speed: {enemy_speed}", True, WHITE), (10, 36))

    if pygame.sprite.spritecollideany(player, enemies):
        game_over()

    pygame.display.update()
    clock.tick(FPS)