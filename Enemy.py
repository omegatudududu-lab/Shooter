
from GameObject import *
from settings import *
import random

class Enemy(GameObject):
    """Клас ворога, який летить вниз."""
    def __init__(self, filename, x, y, w, h):
        super().__init__(filename, x, y, w, h)
        self.hp = Enemy_health
        self.speed = ENEMY_SPEED
        
    def update(self):
        # Рух ворога вниз (збільшення координати Y)
        self.rect.y += self.speed
        
        # Якщо ворог долетів до низу екрана, повертаємо його нагору у випадкову точку X
        if self.rect.y > WINDOW_WIDTH:
            self.rect.y = 0 - self.rect.height*2
            self.rect.x = random.randint(0, WINDOW_WIDTH-ENEMY_HITBOX_SIZE)
            
    def take_damage(self, damage = 1):
        """Отримання урону ворогом."""
        self.hp -= damage
        # Якщо здоров'я закінчилося — знищуємо ворога
        if self.hp <= 0:
            self.kill()
            # Надсилаємо системну подію про вбивство ворога для оновлення рахунку
            pygame.event.post(pygame.event.Event(EVENT_ENEMY_KILLED))