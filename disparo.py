"""Clase Disparo para proyectiles del jugador y enemigos."""

import pygame


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_y, danio, color, propietario):
        super().__init__()
        self.image = pygame.Surface((6, 14), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, 6, 14), border_radius=3)
        self.rect = self.image.get_rect(center=(x, y))
        self._velocidad_y = velocidad_y
        self._danio = danio
        self._propietario = propietario

    @property
    def danio(self):
        return self._danio

    @property
    def propietario(self):
        return self._propietario

    def update(self, dt):
        self.rect.y += int(self._velocidad_y * dt)
        if self.rect.bottom < 0 or self.rect.top > 620:
            self.kill()
