import pygame

# Розміри ігрового вікна (ширина та висота в пікселях)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Шляхи до файлів зображень (текстур) для ігрових об'єктів
ENEMY_IMAGE_PATH = r"images\Enemy.png"
PLAYER_IMAGE_PATH = r"images\Plane.png"
BULLET_IMAGE_PATH = r"images\fire.png"

# Попереднє завантаження фонового зображення через Pygame
BACKGROUND_IMAGE_PATH = pygame.image.load(r"images\Space_Backround.jpg")

# Шляхи до аудіофайлів (звуковий ефект пострілу та фонова музика)
DEFAULT_BLASTER_FIRE_SOUND_EFFECT = r"sound\shoot_effect.mp3"
BACKGROUND_SOUND = r"sound\background_sound.1.mp3"


# Частота оновлення кадрів (плавність гри)
FPS = 120

# Базовий колір заливки екрана (темно-сірий у форматі RGB)
BACKGROUND_COLOR = (32, 32, 32)

# Кількість життів (HP) для гравця та ворогів за замовчуванням
Player_health = 3
Enemy_health = 2

# Стандартна швидкість руху для базового класу GameObject
DEFAULT_SPEED = 4

# Розміри хітбоксів (ширина та висота прямокутників зіткнення)
PLAYER_HITBOX_SIZE_X = 55
PLAYER_HITBOX_SIZE_Y = 40
ENEMY_HITBOX_SIZE = 40
BULLET_HITBOX_WIDTH = 7
BULLET_HITBOX_HEIGHT = 25

# Швидкість руху ворогів (падіння вниз)
ENEMY_SPEED = 1

# Створення унікального ідентифікатора для власної події "Ворога вбито"
EVENT_ENEMY_KILLED = pygame.USEREVENT + 1

# Колір шрифту для виведення тексту рахунку (темно-червоний у форматі RGB)
FONT_COLOR = (100,20,30)