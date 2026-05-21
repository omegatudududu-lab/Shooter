import pygame
import random
import json
from settings import *

# Ініціалізація модулів Pygame (екран, звуки, шрифти)
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Масштаб фону під поточні розміри ігрового вікна
background = pygame.transform.scale(BACKGROUND_IMAGE_PATH, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Налаштування звуку 
shoot_sound = pygame.mixer.Sound(DEFAULT_BLASTER_FIRE_SOUND_EFFECT)
shoot_sound.set_volume(0.3)

# Завантаження фонової музики
background_sound = pygame.mixer.music.load(BACKGROUND_SOUND)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

# Виділяємо 8 каналів міксера
pygame.mixer.set_num_channels(8)

# Створення ігрового вікна та таймера для FPS
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

running = True


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


    def draw(self):
        """Малювання об'єкта на екрані за його поточними координатами."""
        screen.blit(self.image, (self.rect.x, self.rect.y))


    def is_collide(self, gameObject: "GameObject"):
        """Ручна перевірка зіткнення з іншим об'єктом через прямокутники."""
        return self.rect.colliderect(gameObject.rect)


class Label():
    """Клас для створення та відображення текстових написів (наприклад, рахунку)."""
    def __init__(self,x,y, text, font_size, color):
        # Завантаження системного шрифту Impact та його розміру
        self.font = pygame.font.SysFont("Impact", font_size)
        self.color = color
        # Створення графічного об'єкта тексту
        self.text = self.font.render(text, True, color)
        self.x = x
        self.y = y
        
    def draw(self):
        """Відображення тексту на екрані."""
        screen.blit(self.text, (self.x, self.y))
    
    def set_text(self, new_text):
        """Оновлення тексту (викликається при зміні рахунку)."""
        self.text = self.font.render(new_text, True, self.color)
        
        

class Player(GameObject):
    """Клас гравця, яким керує користувач."""
    def __init__(self, filename, x, y, w, h):
        super().__init__(filename, x, y, w, h) 
        # Встановлюємо початкове здоров'я з файлу налаштувань
        self.hp = Player_health


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
        """Створення патрона по центру гравця та запуск звукуポストрілу."""
        # Розраховуємо координати так, щоб куля вилітала точно з центру корабля
        c = Cartridge(
            BULLET_IMAGE_PATH,
            self.rect.x + PLAYER_HITBOX_SIZE_X/2 - BULLET_HITBOX_WIDTH/2,
            self.rect.y + PLAYER_HITBOX_SIZE_Y/2,
            BULLET_HITBOX_WIDTH ,
            BULLET_HITBOX_HEIGHT)
        # Додаємо створений патрон у групу для автоматичного оновлення та малювання
        cartridgies.add(c)
        shoot_sound.play()

    def take_damage(self, damage = 1):
        """Зменшення здоров'я гравця при отриманні урону."""
        # Робимо змінну циклу глобальною, щоб зупинити гру при смерті
        global running
        self.hp -= damage
        print(f"Гравець отримав урон! Поточне HP: {self.hp}") # Допоможе в дебазі
        if self.hp <= 0:
            print("Player has been died")
            self.kill()
            running = False


            
class Cartridge(GameObject):
    """Клас патрона, який летить вгору."""
    def update(self):
        # Рух патрона вгору (зменшення координати Y)
        self.rect.y -= self.speed
        
        # Якщо патрон вилетів далеко за екран — видаляємо його для оптимізації пам'яті
        if self.rect.y < 0 - 80:
            self.kill()
        
        
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


# Створення об'єкта гравця та груп спрайтів для ворогів і патронів
player = Player(PLAYER_IMAGE_PATH, 350, 500, PLAYER_HITBOX_SIZE_X, PLAYER_HITBOX_SIZE_Y)  
enemies = pygame.sprite.Group()
cartridgies = pygame.sprite.Group()

# Цикл для спавну початкових 6 ворогів у випадкових точках над екраном
for i in range(6):
    enemy = Enemy(ENEMY_IMAGE_PATH, random.randint(0, WINDOW_WIDTH-ENEMY_HITBOX_SIZE),
                  0-ENEMY_HITBOX_SIZE*2,
                  ENEMY_HITBOX_SIZE,ENEMY_HITBOX_SIZE)
    enemies.add(enemy)

# Зчитування збереженого рахунку/рекорду з JSON-файлу
with open ("file.json", "r",encoding="UTF-8") as file:
    data = json.load(file)

# Формування початкового текста рахунку та створення графічного напису
score_counter = data["score"]
score_text = "SCORE: "+ str(score_counter)
score_label = Label(WINDOW_WIDTH-230, WINDOW_HEIGHT-45, score_text, 40,FONT_COLOR)


# ГОЛОВНИЙ ІГРОВИЙ ЦИКЛ
while running:
    # Обмеження кількості кадрів в секунду (FPS)
    clock.tick(FPS)
    
    # Очищення екрана базовим кольором та малювання текстури фону
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))
    
    # --- ОБРОБКА ПОДІЙ ---
    for event in pygame.event.get():
        # Перевірка на закриття вікна (хрестик)
        if event.type == pygame.QUIT:
            running = False
            
        # Перевірка натискання клавіш (KEYDOWN)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Стріляємо тільки якщо гравець живий
                if player.hp > 0:
                    player.shoot()
            
        # Подія EVENT_ENEMY_KILLED викликається, коли ворог вмирає від кулі
        elif event.type == EVENT_ENEMY_KILLED:
            print("ENEMY KILLED")
            # Збільшуємо рахунок та оновлюємо текст на екрані
            score_counter +=1
            score_text = "SCORE: "+ str(score_counter)
            score_label.set_text(score_text)

    # --- ОНОВЛЕННЯ ЛОГІКИ ---
    # Оновлюємо позиції патронів та ворогів
    cartridgies.update()
    enemies.update()
    
    # Оновлюємо позицію гравця, якщо у нього є здоров'я
    if player.hp > 0:
        player.update()

    # --- МАЛЮВАННЯ ШАРІВ ---
    # 1. Спочатку малюємо ворогів та патрони
    enemies.draw(screen)
    cartridgies.draw(screen)
    
    # 2. Потім малюємо модельку гравця поверх них
    if player.hp > 0:
        player.draw()
        
    # 3. Наприкінці малюємо інтерфейс (рахунок)
    score_label.draw()
   
    
    # ОБРОБКА ЗІТКНЕНЬ (КОЛІЗІЇ)
    
    # 1. Зіткнення кулі з ворогом. Куля зникає (True), ворог ні (False), бо у нього є HP
    hits_enemy_bullet = pygame.sprite.groupcollide(enemies, cartridgies,False, True)
    
    # Перебираємо словник зіткнень: наносимо урон ворогу за кожну кулю, що в нього влучила
    for enemy, bullets in   hits_enemy_bullet.items():
        for cartridge in bullets:
            enemy.take_damage()


    # 2. Зіткнення гравця з ворогами. Ворог зникає (True), бо врізався
    # Перевіряємо, чи живий гравець, перед обробкою зіткнення з ним
    if player.hp > 0:
        hits_enemy_player = pygame.sprite.spritecollide(player, enemies, True)

        for enemy in hits_enemy_player:
            score_counter +=1
            score_text = "SCORE: "+ str(score_counter)
            score_label.set_text(score_text)
            # Зменшуємо здоров'я гравця на 1 за кожного ворога
            player.take_damage()
    
        
    pygame.display.update()


pygame.quit()