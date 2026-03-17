"""Jerarquia de enemigos con herencia y polimorfismo."""

import random

import pygame

from disparo import Disparo


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, vida, puntos):
        super().__init__()
        self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self._velocidad = velocidad
        self._vida = vida
        self.__puntos = puntos
        self._tiempo_ultimo_disparo = 0.0
        self._cooldown_disparo = random.uniform(1.3, 2.7)

    def get_puntos(self):
        return self.__puntos

    def set_puntos(self, puntos):
        self.__puntos = max(0, puntos)

    def recibir_danio(self, danio):
        self._vida -= danio
        if self._vida <= 0:
            self.kill()
            return True
        return False

    def update(self, dt):
        self.rect.y += int(self._velocidad * dt)
        if self.rect.top > 620:
            self.kill()

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

    def intentar_disparar(self, tiempo_actual):
        if tiempo_actual - self._tiempo_ultimo_disparo >= self._cooldown_disparo:
            self._tiempo_ultimo_disparo = tiempo_actual
            return Disparo(
                x=self.rect.centerx,
                y=self.rect.bottom,
                velocidad_y=320,
                danio=1,
                color=(255, 90, 90),
                propietario="enemigo",
            )
        return None


class EnemigoBasico(Enemigo):
    def __init__(self, x, y, image=None):
        super().__init__(x, y, velocidad=140, vida=1, puntos=50)
        if image is not None:
            self.image = image.copy()
        else:
            self.image = pygame.Surface((76, 56), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (250, 125, 94), (0, 0, 76, 56), border_radius=12)
            pygame.draw.circle(self.image, (255, 236, 132), (24, 26), 6)
            pygame.draw.circle(self.image, (255, 236, 132), (52, 26), 6)
        self.rect = self.image.get_rect(center=(x, y))


class EnemigoRapido(Enemigo):
    def __init__(self, x, y, image=None):
        super().__init__(x, y, velocidad=240, vida=1, puntos=90)
        if image is not None:
            self.image = image.copy()
        else:
            self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (180, 255, 170), [(0, 0), (30, 40), (60, 0)])
            pygame.draw.polygon(self.image, (96, 190, 86), [(10, 6), (30, 32), (50, 6)])
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        # Sobrescritura polimorfica: movimiento en zig-zag ademas de avanzar.
        self.rect.y += int(self._velocidad * dt)
        self.rect.x += int(110 * dt * (1 if (self.rect.y // 24) % 2 == 0 else -1))
        if self.rect.top > 620:
            self.kill()
