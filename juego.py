"""Modulo principal de logica del videojuego."""
import os
import random

import pygame

import config
from audio_manager import AudioManager
from enemigo import EnemigoBasico, EnemigoRapido
from jugador import Jugador
from obstaculo import Obstaculo
from powerup import PowerUp


class Juego:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.TITULO)
        self.pantalla = pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
        self.reloj = pygame.time.Clock()

        self.fondo_game = self._cargar_imagen_escalada(
            ["game_background.jpg"],
            (config.ANCHO_VENTANA, config.ALTO_VENTANA),
        )
        self.fondo_menu = self._cargar_imagen_escalada(
            ["menu_background.jpg"],
            (config.ANCHO_VENTANA, config.ALTO_VENTANA),
        )
        self.sprite_jugador = self._cargar_imagen_escalada(["player.jpg", "player.png"], (92, 68), alpha=True)
        self.sprite_enemigo_basico = self._cargar_imagen_escalada(
            ["enemy_1.jpg", "enemy_1.png"], (76, 56), alpha=True
        )
        self.sprite_enemigo_rapido = self._cargar_imagen_escalada(
            ["enemy_2.jpg", "enemy_2.png"], (60, 40), alpha=True
        )
        if self.sprite_enemigo_basico is not None:
            self.sprite_enemigo_basico = pygame.transform.rotate(self.sprite_enemigo_basico, 180)
        if self.sprite_enemigo_rapido is not None:
            self.sprite_enemigo_rapido = pygame.transform.rotate(self.sprite_enemigo_rapido, 180)

        self.audio = AudioManager()
        self.fuente_ui = self._cargar_fuente(20)
        self.fuente_menu_titulo = self._cargar_fuente_personalizada(30)

        self.estado = "MENU"
        self.puntuacion = 0
        self.tiempo_transcurrido_s = 0.0

        self._ultimo_spawn_enemigo = 0.0
        self._ultimo_spawn_obstaculo = 0.0
        self._ultimo_spawn_powerup = 0.0

        self._crear_escena()
        self.audio.reproducir_musica_menu()

    def _cambiar_estado(self, nuevo_estado):
        if self.estado == nuevo_estado:
            return

        self.estado = nuevo_estado
        if self.estado == "MENU":
            self.audio.reproducir_musica_menu()
        elif self.estado == "GAME":
            self.audio.reproducir_musica_juego()
        elif self.estado == "WIN":
            self.audio.detener_musica()
            self.audio.reproducir_victoria()
        elif self.estado == "LOSE":
            self.audio.detener_musica()
            self.audio.reproducir_derrota()

    def _cargar_fuente(self, size):
        ruta = config.RUTA_FUENTE_PRINCIPAL
        if os.path.exists(ruta):
            return pygame.font.Font(ruta, size)
        return pygame.font.SysFont("consolas", size)

    def _cargar_fuente_personalizada(self, size):
        ruta = config.RUTA_FUENTE_PERSONALIZADA
        if os.path.exists(ruta):
            return pygame.font.Font(ruta, size)
        return pygame.font.SysFont("consolas", size)

    def _cargar_imagen_escalada(self, nombres, size, alpha=False):
        for nombre in nombres:
            ruta = os.path.join(config.RUTA_ASSETS, "images", nombre)
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta)
                imagen = imagen.convert_alpha() if alpha else imagen.convert()
                return pygame.transform.scale(imagen, size)
        return None

    def _crear_escena(self):
        self.jugador = Jugador(config.ANCHO_VENTANA // 2, config.ALTO_VENTANA - 70, image=self.sprite_jugador)

        self.grupo_jugador = pygame.sprite.GroupSingle(self.jugador)
        self.grupo_enemigos = pygame.sprite.Group()
        self.grupo_disparos = pygame.sprite.Group()
        self.grupo_obstaculos = pygame.sprite.Group()
        self.grupo_powerups = pygame.sprite.Group()

    def _tiempo_transcurrido(self):
        return self.tiempo_transcurrido_s

    def _gestionar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if self.estado == "MENU" and evento.type in {pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN}:
                self._cambiar_estado("GAME")

            if self.estado == "GAME" and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                tiempo_actual = self._tiempo_transcurrido()
                if self.jugador.puede_disparar(tiempo_actual):
                    self.grupo_disparos.add(self.jugador.disparar(tiempo_actual))
                    self.audio.reproducir_disparo()

            if self.estado in {"LOSE", "WIN"} and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.reiniciar()
                if evento.key == pygame.K_ESCAPE:
                    return False

        return True

    def _spawnear_objetos(self, tiempo_actual):
        if tiempo_actual - self._ultimo_spawn_enemigo >= 0.95:
            x = random.randint(40, config.ANCHO_VENTANA - 40)
            clase = random.choice([EnemigoBasico, EnemigoRapido])
            if clase is EnemigoBasico:
                self.grupo_enemigos.add(clase(x, -30, image=self.sprite_enemigo_basico))
            else:
                self.grupo_enemigos.add(clase(x, -30, image=self.sprite_enemigo_rapido))
            self._ultimo_spawn_enemigo = tiempo_actual

        if tiempo_actual - self._ultimo_spawn_obstaculo >= 1.7:
            x = random.randint(30, config.ANCHO_VENTANA - 30)
            self.grupo_obstaculos.add(Obstaculo(x, -30))
            self._ultimo_spawn_obstaculo = tiempo_actual

        if tiempo_actual - self._ultimo_spawn_powerup >= 9.5:
            x = random.randint(30, config.ANCHO_VENTANA - 30)
            self.grupo_powerups.add(PowerUp(x, -20))
            self._ultimo_spawn_powerup = tiempo_actual

    def _disparos_enemigos(self, tiempo_actual):
        for enemigo in self.grupo_enemigos:
            disparo = enemigo.intentar_disparar(tiempo_actual)
            if disparo:
                self.grupo_disparos.add(disparo)

    def _actualizar(self, dt):
        if self.estado != "GAME":
            return

        self.tiempo_transcurrido_s += dt
        tiempo_actual = self._tiempo_transcurrido()
        teclas = pygame.key.get_pressed()

        self.jugador.mover(dt, teclas, config.ANCHO_VENTANA, config.ALTO_VENTANA)

        self._spawnear_objetos(tiempo_actual)
        self._disparos_enemigos(tiempo_actual)

        self.grupo_enemigos.update(dt)
        self.grupo_disparos.update(dt)
        self.grupo_obstaculos.update(dt)
        self.grupo_powerups.update(dt)

        self._resolver_colisiones()
        self._actualizar_estado_partida(tiempo_actual)

    def _resolver_colisiones(self):
        # Disparos del jugador contra enemigos.
        for disparo in list(self.grupo_disparos):
            if disparo.propietario != "jugador":
                continue
            impacto = pygame.sprite.spritecollideany(disparo, self.grupo_enemigos)
            if impacto:
                destruido = impacto.recibir_danio(disparo.danio)
                disparo.kill()
                if destruido:
                    self.puntuacion += impacto.get_puntos()

        # Disparos enemigos contra jugador.
        for disparo in list(self.grupo_disparos):
            if disparo.propietario != "enemigo":
                continue
            if self.jugador.rect.colliderect(disparo.rect):
                self.jugador.recibir_danio(1)
                disparo.kill()

        # Colisiones directas con enemigos y obstaculos.
        if pygame.sprite.spritecollideany(self.jugador, self.grupo_enemigos):
            self.jugador.recibir_danio(1)
        if pygame.sprite.spritecollideany(self.jugador, self.grupo_obstaculos):
            self.jugador.recibir_danio(1)

        # Recoger powerups.
        powerup = pygame.sprite.spritecollideany(self.jugador, self.grupo_powerups)
        if powerup:
            if powerup.tipo == "vida":
                self.jugador.set_vida(self.jugador.get_vida() + 1)
            else:
                self.puntuacion += 80
            powerup.kill()

    def _actualizar_estado_partida(self, tiempo_actual):
        if not self.jugador.esta_vivo():
            self._cambiar_estado("LOSE")
            return

        if self.puntuacion >= config.PUNTOS_VICTORIA or tiempo_actual >= config.TIEMPO_LIMITE_SEGUNDOS:
            self._cambiar_estado("WIN")

    def _dibujar_fondo(self):
        if self.fondo_game is not None:
            self.pantalla.blit(self.fondo_game, (0, 0))
            return

        self.pantalla.fill(config.COLOR_FONDO)
        for _ in range(40):
            x = random.randint(0, config.ANCHO_VENTANA)
            y = random.randint(0, config.ALTO_VENTANA)
            self.pantalla.set_at((x, y), (40, 58, 82))

    def _dibujar_ui(self):
        tiempo_restante = max(0, config.TIEMPO_LIMITE_SEGUNDOS - int(self._tiempo_transcurrido()))

        texto_puntos = self.fuente_ui.render(f"Puntos: {self.puntuacion}", True, config.COLOR_TEXTO)
        texto_vidas = self.fuente_ui.render(f"Vidas: {self.jugador.get_vida()}", True, config.COLOR_TEXTO)
        texto_tiempo = self.fuente_ui.render(f"Tiempo: {tiempo_restante}s", True, config.COLOR_TEXTO)

        self.pantalla.blit(texto_puntos, (20, 16))
        self.pantalla.blit(texto_vidas, (20, 46))
        self.pantalla.blit(texto_tiempo, (20, 76))

    def _dibujar_estado_final(self):
        if self.estado not in {"LOSE", "WIN"}:
            return

        titulo = "GAME OVER" if self.estado == "LOSE" else "VICTORIA"
        color = config.COLOR_ALERTA if self.estado == "LOSE" else (130, 255, 158)

        titulo_surf = self.fuente_menu_titulo.render(titulo, True, color)
        instruccion = self.fuente_ui.render("Pulsa R para reiniciar o ESC para salir", True, config.COLOR_TEXTO)

        self.pantalla.blit(
            titulo_surf,
            titulo_surf.get_rect(center=(config.ANCHO_VENTANA // 2, config.ALTO_VENTANA // 2 - 20)),
        )
        self.pantalla.blit(
            instruccion,
            instruccion.get_rect(center=(config.ANCHO_VENTANA // 2, config.ALTO_VENTANA // 2 + 30)),
        )

    def _dibujar(self):
        if self.estado == "MENU":
            if self.fondo_menu is not None:
                self.pantalla.blit(self.fondo_menu, (0, 0))
            else:
                self.pantalla.fill(config.COLOR_FONDO)
            texto_menu = self.fuente_menu_titulo.render("Presiona cualquier tecla para comenzar", True, config.COLOR_MENU)
            self.pantalla.blit(
                texto_menu,
                texto_menu.get_rect(center=(config.ANCHO_VENTANA // 2, config.ALTO_VENTANA // 2)),
            )
            pygame.display.flip()
            return

        self._dibujar_fondo()
        self.grupo_jugador.draw(self.pantalla)

        for enemigo in self.grupo_enemigos:
            enemigo.dibujar(self.pantalla)

        self.grupo_disparos.draw(self.pantalla)
        self.grupo_obstaculos.draw(self.pantalla)
        self.grupo_powerups.draw(self.pantalla)

        self._dibujar_ui()
        self._dibujar_estado_final()

        pygame.display.flip()

    def reiniciar(self):
        self.puntuacion = 0
        self.estado = "GAME"
        self.tiempo_transcurrido_s = 0.0
        self._ultimo_spawn_enemigo = 0.0
        self._ultimo_spawn_obstaculo = 0.0
        self._ultimo_spawn_powerup = 0.0
        self._crear_escena()
        self.audio.reproducir_musica_juego()

    def ejecutar(self):
        activo = True
        while activo:
            dt = self.reloj.tick(config.FPS) / 1000.0
            activo = self._gestionar_eventos()
            self._actualizar(dt)
            self._dibujar()

        pygame.quit()
