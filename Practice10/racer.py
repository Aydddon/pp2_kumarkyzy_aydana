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
YELLOW = (255, 215, 0)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5       # speed of enemy and coins (grows with time)
SCORE = 0       # number of enemies passed
COINS = 0       # number of collected coins

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
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


#Images and sound (files from the tutorial archive must be in the same folder)
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
        self.rect.move_ip(0, SPEED)
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


# NEW: Coin class - a coin that appears at a random place at the top
# and falls down the road like the enemy does
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # No coin image in the archive, so we draw the coin on a surface
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (12, 12), 12)
        pygame.draw.circle(self.image, BLACK, (12, 12), 12, 2)
        pygame.draw.circle(self.image, BLACK, (12, 12), 6, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)   # random x position

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):      # missed coin disappears
            self.kill()


#Setting up Sprites
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()          # NEW: group of coins
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding new User events
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
SPAWN_COIN = pygame.USEREVENT + 2      # NEW: event for creating coins
pygame.time.set_timer(SPAWN_COIN, 1500)

#Game Loop
while True:

    #Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
        # NEW: with 70% chance a coin appears each time the event fires
        if event.type == SPAWN_COIN and random.randint(1, 100) <= 70:
              C1 = Coin()
              coins.add(C1)
              all_sprites.add(C1)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # NEW: number of collected coins in the top right corner
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # NEW: player touches a coin -> coin is removed (True) and counter grows
    for coin in pygame.sprite.spritecollide(P1, coins, True):
        COINS += 1

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