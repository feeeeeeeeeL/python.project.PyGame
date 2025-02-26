import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры игрового окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Mario-like Platformer")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Часы для управления FPS
clock = pygame.time.Clock()
FPS = 60

# Загрузка изображений
player_image = pygame.Surface((50, 50))
player_image.fill(GREEN)
coin_image = pygame.Surface((30, 30))
coin_image.fill(WHITE)
enemy_image = pygame.Surface((50, 50))
enemy_image.fill(RED)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 150
        self.change_x = 0
        self.change_y = 0
        self.is_jumping = False
        self.score = 0

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Проверка коллизий с краями экрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y > HEIGHT:
            self.rect.y = HEIGHT
            self.change_y = 0

    def calc_grav(self):
        if self.rect.y < HEIGHT - 50:
            self.change_y += 1  # Имитация гравитации
        else:
            self.change_y = 0
            self.rect.y = HEIGHT - 50
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.change_y = -15
            self.is_jumping = True


# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Создание монет и врагов
for i in range(5):
    coin = Coin(random.randint(100, WIDTH - 100), random.randint(50, HEIGHT - 200))
    coins.add(coin)
    all_sprites.add(coin)

for i in range(3):
    enemy = Enemy(random.randint(100, WIDTH - 100), random.randint(50, HEIGHT - 150))
    enemies.add(enemy)
    all_sprites.add(enemy)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.change_x = 0

    if keys[pygame.K_LEFT]:
        player.change_x = -5
    if keys[pygame.K_RIGHT]:
        player.change_x = 5
    if keys[pygame.K_SPACE]:
        player.jump()

    # Обновляем все спрайты
    all_sprites.update()

    # Проверка на сбор монет
    coins_collected = pygame.sprite.spritecollide(player, coins, True)
    for coin in coins_collected:
        player.score += 1

    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Отображение счёта
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {player.score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()