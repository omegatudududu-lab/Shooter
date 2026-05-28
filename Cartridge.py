from GameObject import GameObject
from settings import *

class Cartridge(GameObject):
    """Клас патрона, який летить вгору."""
    def update(self):
        # Рух патрона вгору (зменшення координати Y)
        self.rect.y -= self.speed
        
        # Якщо патрон вилетів далеко за екран — видаляємо його для оптимізації пам'яті
        if self.rect.y < 0 - 80:
            self.kill()

class Enemy_Cartridge(GameObject):
    """Клас патрона, який летить вниз."""
    def update(self):
        # Рух патрона вниз (збільшеня координати Y)
        self.rect.y += self.speed

        # Якщо патрон вилетів далеко за екран — видаляємо його для оптимізації пам'яті
        if self.rect.y > WINDOW_HEIGHT + 80:
            self.kill()