"""Configuracion general del juego."""

import os

ANCHO_VENTANA = 960
ALTO_VENTANA = 600
TITULO = "Practica 3.3 - Space Survival"
FPS = 60

COLOR_FONDO = (8, 15, 28)
COLOR_TEXTO = (255, 255, 255)
COLOR_ALERTA = (255, 97, 97)
COLOR_MENU = (0, 255, 0)

PUNTOS_VICTORIA = 500
TIEMPO_LIMITE_SEGUNDOS = 120

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_ASSETS = os.path.join(BASE_DIR, "assets")
RUTA_FUENTE_PRINCIPAL = os.path.join(RUTA_ASSETS, "fonts", "PressStart2P-Regular.ttf")
RUTA_FUENTE_PERSONALIZADA = os.path.join(RUTA_ASSETS, "fonts", "font.ttf")
