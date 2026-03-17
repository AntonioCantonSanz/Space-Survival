"""Gestion de audio del juego con musica por estado y efectos puntuales."""

import os

import pygame

import config


class AudioManager:
    def __init__(self):
        self.habilitado = False
        self._musica_actual = None
        self._sfx_disparo = None
        self._sfx_win = None
        self._sfx_lose = None
        self._ruta_menu_music = None
        self._ruta_game_music = None

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.habilitado = True
            self._cargar_audio()
        except pygame.error:
            self.habilitado = False

    def _cargar_audio(self):
        base = os.path.join(config.RUTA_ASSETS, "sounds")
        self._ruta_menu_music = os.path.join(base, "menu_music.mp3")
        self._ruta_game_music = os.path.join(base, "game_music.mp3")

        ruta_shoot = os.path.join(base, "shoot.mp3")
        ruta_win = os.path.join(base, "win.mp3")
        ruta_lose = os.path.join(base, "lose.mp3")

        if os.path.exists(ruta_shoot):
            self._sfx_disparo = pygame.mixer.Sound(ruta_shoot)
        if os.path.exists(ruta_win):
            self._sfx_win = pygame.mixer.Sound(ruta_win)
        if os.path.exists(ruta_lose):
            self._sfx_lose = pygame.mixer.Sound(ruta_lose)

    def _reproducir_musica(self, ruta):
        if not self.habilitado or not ruta or not os.path.exists(ruta):
            return
        if self._musica_actual == ruta:
            return
        pygame.mixer.music.stop()
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play(loops=-1)
        self._musica_actual = ruta

    def reproducir_musica_menu(self):
        self._reproducir_musica(self._ruta_menu_music)

    def reproducir_musica_juego(self):
        self._reproducir_musica(self._ruta_game_music)

    def reproducir_disparo(self):
        if self.habilitado and self._sfx_disparo:
            self._sfx_disparo.play()

    def reproducir_victoria(self):
        if self.habilitado and self._sfx_win:
            self._sfx_win.play()

    def reproducir_derrota(self):
        if self.habilitado and self._sfx_lose:
            self._sfx_lose.play()

    def reproducir_gameover(self):
        self.reproducir_derrota()

    def detener_musica(self):
        if self.habilitado:
            pygame.mixer.music.stop()
            self._musica_actual = None
