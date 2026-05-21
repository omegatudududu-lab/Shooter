import pygame
import random
import json
from settings import *
from GameObject import *
from Player import *
from Enemy import *
from Cartridge import *

# Ініціалізація модулів Pygame (екран, звуки, шрифти) 12312
print("hello")
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Масштаб фону під поточні розміри ігрового вікна
background = pygame.transform.scale(BACKGROUND_IMAGE_PATH, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Налаштування звуку 
shoot_sound = pygame.mixer.Sound(DEFAULT_BLASTER_FIRE_SOUND_EFFECT)
shoot_sound.set_volume(0.3)

player_sounds = {
    "shoot_sound": shoot_sound 
}

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
        
        


            

        
        
enemies = pygame.sprite.Group()
cartridgies = pygame.sprite.Group()


# Створення об'єкта гравця та груп спрайтів для ворогів і патронів
player = Player(
    PLAYER_IMAGE_PATH,
    350, 
    500, 
    PLAYER_HITBOX_SIZE_X, 
    PLAYER_HITBOX_SIZE_Y,
    player_sounds,
    cartridgies
    )  


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
        player.draw(screen)
        
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
    if player.hp > 1:
        hits_enemy_player = pygame.sprite.spritecollide(player, enemies, True)

        for enemy in hits_enemy_player:
            score_counter +=1
            score_text = "SCORE: "+ str(score_counter)
            score_label.set_text(score_text)
            # Зменшуємо здоров'я гравця на 1 за кожного ворога
            player.take_damage()
    else:
        running = False
        with open("file.json", "w", encoding="UTF-8") as file:
            data["score"] = score_counter
            json.dump(data, file, indent=4)
        
    pygame.display.update()


pygame.quit()

