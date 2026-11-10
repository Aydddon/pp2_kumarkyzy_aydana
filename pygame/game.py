import random
import pygame

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Самая простая игра на Pygame")

# Цвета (RGB)
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Игрок (позиция, размеры и скорость)
player_x = 300
player_y = 200
player_size = 30
player_speed = 5

# Еда (позиция и размеры)
food_size = 25
food_x = random.randint(50, WIDTH - 50)
food_y = random.randint(50, HEIGHT - 50)

# Счет
score = 0
font = pygame.font.SysFont(None, 36)

# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
  # 1. Обработка событий (выход из игры)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # 2. Управление с клавиатуры (стрелки)
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] and player_x > 0:
    player_x -= player_speed
  if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
    player_x += player_speed
  if keys[pygame.K_UP] and player_y > 0:
    player_y -= player_speed
  if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
    player_y += player_speed

  # 3. Проверка столкновения игрока с едой
  # Создаем прямоугольники для игрока и еды, чтобы проверить пересечение
  player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
  food_rect = pygame.Rect(food_x, food_y, food_size, food_size)

  if player_rect.colliderect(food_rect):
    score += 1
    # Перемещаем еду в случайное место
    food_x = random.randint(50, WIDTH - 50)
    food_y = random.randint(50, HEIGHT - 50)

  # 4. Отрисовка графики
  screen.fill(WHITE)  # Заливаем фон белым цветом

  # Рисуем игрока (синий квадрат) и еду (красный квадрат)
  pygame.draw.rect(screen, BLUE, player_rect)
  pygame.draw.rect(screen, RED, food_rect)

  # Отображение счета на экране
  score_text = font.render(f"Счет: {score}", True, BLACK)
  screen.blit(score_text, (15, 15))

  # Обновление экрана
  pygame.display.flip()

  # Ограничение до 60 кадров в секунду
  clock.tick(60)

pygame.quit()