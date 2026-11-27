#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initializing
pygame.init()

#Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ENEMY_SPEED = 5          # speed of the enemy (grows when player earns coins)
COIN_SPEED = 5           # coins always fall with the same speed
SCORE = 0                # number of enemies passed
COINS = 0                # total VALUE of collected coins (sum of weights)

N = 5                    # every N coins earned the enemy gets faster
SPEED_STEP = 1           # how much faster
next_speedup = N         # coin total at which the next speed-up happens

# NEW: coin types with different weights.
# weight = value of the coin, chance = probability of appearing (in %)
COIN_TYPES = [
    {"weight": 1, "radius": 10, "color": (205, 127, 50),  "chance": 60},   # bronze
    {"weight": 2, "radius": 13, "color": (192, 192, 192), "chance": 30},   # silver
    {"weight": 3, "radius": 16, "color": (255, 215, 0),   "chance": 10},   # gold
]

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_tiny = pygame.font.SysFont("Verdana", 12, bold=True)
game_over = font.render("Game Over", True, BLACK)

# If files from the tutorial archive are missing, simple drawn pictures are used instead
def load_image(name, size, color):
    try:
        return pygame.image.load(name)
    except (FileNotFoundError, pygame.error):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, size[0], size[1]), border_radius=8)
        pygame.draw.rect(surf, (150, 200, 255), (6, 12, size[0] - 12, 16))   # windshield
        return surf


def load_background():
    try:
        return pygame.image.load("AnimatedStreet.png")
    except (FileNotFoundError, pygame.error):
        surf = pygame.Surface((400, 600))
        surf.fill((34, 139, 34))
        pygame.draw.rect(surf, (60, 60, 60), (40, 0, 320, 600))
        for y in range(0, 600, 80):
            pygame.draw.rect(surf, (255, 255, 255), (197, y, 6, 40))
        return surf


def play_crash():
    try:
        pygame.mixer.Sound('crash.wav').play()
    except (FileNotFoundError, pygame.error):
        pass


#Images (files from the tutorial archive must be in the same folder)
background = load_background()

#Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = load_image("Enemy.png", (45, 80), (200, 30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0, ENEMY_SPEED)       # uses the enemy's own speed
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("Player.png", (45, 80), (30, 80, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)


# Coin with a random weight: bigger and differently coloured coins are worth more
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # random.choices picks one coin type using the "chance" values as probabilities
        kind = random.choices(COIN_TYPES, weights=[t["chance"] for t in COIN_TYPES])[0]
        self.weight = kind["weight"]
        r = kind["radius"]
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, kind["color"], (r, r), r)
        pygame.draw.circle(self.image, BLACK, (r, r), r, 2)
        label = font_tiny.render(str(self.weight), True, BLACK)    # weight written on the coin
        self.image.blit(label, label.get_rect(center=(r, r)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, COIN_SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.kill()


#Setting up Sprites
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event for creating coins
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 1200)

#Game Loop
while True:

    #Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == SPAWN_COIN and random.randint(1, 100) <= 75:
              C1 = Coin()
              coins.add(C1)
              all_sprites.add(C1)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Coins in the top right corner
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))
    # Current enemy speed (helps to see the speed-up working)
    speed_text = font_tiny.render("Enemy speed: " + str(ENEMY_SPEED), True, BLACK)
    DISPLAYSURF.blit(speed_text, (10, 35))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collect coins: add the weight of each collected coin
    for coin in pygame.sprite.spritecollide(P1, coins, True):
        COINS += coin.weight

    # NEW: every time the player earns N more coins, the enemy gets faster.
    # "while" is used because a heavy coin can jump over a threshold.
    while COINS >= next_speedup:
        ENEMY_SPEED += SPEED_STEP
        next_speedup += N

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          play_crash()
          time.sleep(0.5)

          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))

          pygame.display.update()
          for entity in all_sprites:
                entity.kill()
          time.sleep(2)
          pygame.quit()
          sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)