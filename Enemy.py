from GameObject import *
from settings import *
from Cartridge import Enemy_Cartridge
import random

class Enemy(GameObject):
    """Клас ворога, який летить вниз."""
    
    def __init__(self, filename, x, y, w, h, enemy_cartridgies, enemy_sounds):
        super().__init__(filename, x, y, w, h)
        self.hp = Enemy_health
        self.speed = ENEMY_SPEED
        self.enemy_cartridgies = enemy_cartridgies
        self.enemy_sounds = enemy_sounds
        
        # Таймер стрільби (хаотичний для кожного ворога)
        self.shoot_delay = random.randint(100, 300) 
        self.timer = 0

    def update(self):
        # Рух ворога вниз
        self.rect.y += self.speed

        # Логіка таймера стрільби
        self.timer += 1
        if self.timer >= self.shoot_delay:
            self.shoot()
            self.timer = 0
            self.shoot_delay = random.randint(100, 300) # Змінюємо затримку для хаотичності

        # Якщо ворог долетів до низу екрана (виправлено WINDOW_WIDTH на WINDOW_HEIGHT)
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = 0 - self.rect.height * 2
            self.rect.x = random.randint(0, WINDOW_WIDTH - ENEMY_HITBOX_SIZE)

    def shoot(self):
        """Створення патрона по центру ворога."""
        e = Enemy_Cartridge(
            ENEMY_BULLET_IMAGE_PATH,
            self.rect.x + ENEMY_HITBOX_SIZE / 2 - ENEMY_BULLET_HITBOX_WIDTH / 2,
            self.rect.y + ENEMY_HITBOX_SIZE,
            ENEMY_BULLET_HITBOX_WIDTH,
            ENEMY_BULLET_HITBOX_HEIGHT
        )
        self.enemy_cartridgies.add(e)
        
        # Запуск індивідуального звуку пострілу ворога
        self.enemy_sounds["shoot_sound"].play()

    def take_damage(self, damage = 1):
        """Отримання урону ворогом."""
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            pygame.event.post(pygame.event.Event(EVENT_ENEMY_KILLED))