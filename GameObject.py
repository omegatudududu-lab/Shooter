import pygame
from settings import *

class GameObject(pygame.sprite.Sprite):
    """Базовий клас для всіх рухомих об'єктів у грі."""
    def __init__(self, filename, x, y, w, h):
        # Ініціалізація суперкласу Sprite для роботи груп
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        # Хітбокс об'єкта
        self.rect = pygame.Rect(x, y, w, h)

        # Завантаження та масштабування текстури під розмір хітбокса
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (w, h))

        # Базова швидкість руху об'єкта за замовчуванням
        self.speed = DEFAULT_SPEED


    def draw(self, screen):
        """Малювання об'єкта на екрані за його поточними координатами."""
        screen.blit(self.image, (self.rect.x, self.rect.y))


    def is_collide(self, gameObject: "GameObject"):
        """Ручна перевірка зіткнення з іншим об'єктом через прямокутники."""
        return self.rect.colliderect(gameObject.rect)
