"""Obstaculos que descienden y pueden danar al jugador."""

import random

import pygame


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tam = random.randint(24, 44)
        self.image = pygame.Surface((tam, tam), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (114, 117, 126), (tam // 2, tam // 2), tam // 2)
        pygame.draw.circle(self.image, (84, 88, 98), (tam // 3, tam // 3), tam // 6)
        self.rect = self.image.get_rect(center=(x, y))
        self._velocidad = random.randint(100, 170)

    def update(self, dt):
        self.rect.y += int(self._velocidad * dt)
        if self.rect.top > 620:
            self.kill()
