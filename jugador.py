"""Clase Jugador del videojuego."""

import pygame

from disparo import Disparo


class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()
        if image is not None:
            self.image = image.copy()
        else:
            self.image = pygame.Surface((92, 68), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (95, 214, 255), [(0, 68), (46, 0), (92, 68)])
            pygame.draw.polygon(self.image, (14, 124, 196), [(16, 60), (46, 18), (76, 60)])
        self.rect = self.image.get_rect(center=(x, y))

        self.__vida = 3
        self.__velocidad = 340
        self.__cooldown_disparo = 0.22
        self.__tiempo_ultimo_disparo = 0.0

    def get_vida(self):
        return self.__vida

    def set_vida(self, nueva_vida):
        self.__vida = max(0, min(10, nueva_vida))

    def get_velocidad(self):
        return self.__velocidad

    def set_velocidad(self, nueva_velocidad):
        self.__velocidad = max(120, min(800, nueva_velocidad))

    def mover(self, dt, teclas, ancho, alto):
        vx = 0
        vy = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            vx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            vx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            vy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            vy += 1

        vector = pygame.Vector2(vx, vy)
        if vector.length_squared() > 0:
            vector = vector.normalize() * self.__velocidad * dt
            self.rect.x += int(vector.x)
            self.rect.y += int(vector.y)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ancho, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(alto, self.rect.bottom)

    def puede_disparar(self, tiempo_actual):
        return (tiempo_actual - self.__tiempo_ultimo_disparo) >= self.__cooldown_disparo

    def disparar(self, tiempo_actual):
        self.__tiempo_ultimo_disparo = tiempo_actual
        return Disparo(
            x=self.rect.centerx,
            y=self.rect.top,
            velocidad_y=-620,
            danio=1,
            color=(255, 237, 110),
            propietario="jugador",
        )

    def recibir_danio(self, danio=1):
        self.set_vida(self.__vida - danio)

    def esta_vivo(self):
        return self.__vida > 0
