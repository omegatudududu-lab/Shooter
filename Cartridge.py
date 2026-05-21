from GameObject import GameObject

class Cartridge(GameObject):
    """Клас патрона, який летить вгору."""
    def update(self):
        # Рух патрона вгору (зменшення координати Y)
        self.rect.y -= self.speed
        
        # Якщо патрон вилетів далеко за екран — видаляємо його для оптимізації пам'яті
        if self.rect.y < 0 - 80:
            self.kill()