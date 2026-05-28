from GameObject import *
from settings import *
from Cartridge import Cartridge
class Player(GameObject):
    """Клас гравця, яким керує користувач."""
    def __init__(self, filename, x, y, w, h, player_sound, cartridgies):
        super().__init__(filename, x, y, w, h) 
        # Встановлюємо початкове здоров'я з файлу налаштувань
        self.hp = Player_health
        self.player_sound = player_sound
        self.cartridgies = cartridgies
        


    def update(self):
        """Оновлення позиції гравця на основі натиснутих клавіш."""
        # Отримуємо стан усіх клавіш клавіатури
        keys = pygame.key.get_pressed()

        # Рух гравця по осях (управління WASD)
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        
        # Обмеження: гравець не може вилетіти за ліву чи праву межі екрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WINDOW_WIDTH - self.rect.width:
            self.rect.x = WINDOW_WIDTH - self.rect.width

        # Обмеження: гравець не може вилетіти за верхню чи нижню межі екрана
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > WINDOW_HEIGHT - self.rect.height:
            self.rect.y = WINDOW_HEIGHT - self.rect.height

    def shoot(self):
        """Створення патрона по центру гравця та запуск звуку."""
        # Розраховуємо координати так, щоб куля вилітала точно з центру корабля
        c = Cartridge(
            BULLET_IMAGE_PATH,
            self.rect.x + PLAYER_HITBOX_SIZE_X/2 - BULLET_HITBOX_WIDTH/2,
            self.rect.y + PLAYER_HITBOX_SIZE_Y/2,
            BULLET_HITBOX_WIDTH ,
            BULLET_HITBOX_HEIGHT)
        # Додаємо створений патрон у групу для автоматичного оновлення та малювання
        self.cartridgies.add(c)
        self.player_sound["shoot_sound"].play()

    def take_damage(self, damage = 1):
        """Зменшення здоров'я гравця при отриманні урону."""
        # Робимо змінну циклу глобальною, щоб зупинити гру при смерті
        global running
        self.hp -= damage
        print(f"Гравець отримав урон! Поточне HP: {self.hp}") # Допоможе в дебазі
        if self.hp <= 0:
            print("Player has been died")
            self.kill()