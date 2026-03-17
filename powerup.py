"""PowerUp que mejora vida o puntuacion."""

import random

import pygame


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.tipo = random.choice(["vida", "puntos"])
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        color = (131, 255, 160) if self.tipo == "vida" else (255, 220, 105)
        pygame.draw.circle(self.image, color, (12, 12), 12)
        pygame.draw.circle(self.image, (255, 255, 255), (12, 12), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self._velocidad = 110

    def update(self, dt):
        self.rect.y += int(self._velocidad * dt)
        if self.rect.top > 620:
            self.kill()
