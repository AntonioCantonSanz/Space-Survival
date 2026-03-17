# Práctica 3.3 - Juego con Pygame

## 1. Introducción

En esta práctica se ha desarrollado un videojuego 2D en Python usando la librería Pygame, aplicando los conceptos fundamentales de Programación Orientada a Objetos (POO) estudiados en la Unidad 2.

El juego creado se llama **Space Survival**. El jugador controla una nave y debe sobrevivir mientras destruye enemigos, evita obstáculos y recoge power-ups. La partida termina cuando se cumplen condiciones de **victoria** (alcanzar una puntuación objetivo o aguantar el tiempo límite) o de **derrota** (quedarse sin vidas).

El objetivo de este desarrollo no es únicamente programar un juego funcional, sino también demostrar una arquitectura de código organizada, reutilizable y fácil de mantener.

---

## 2. Objetivos del proyecto

Los objetivos planteados para el proyecto han sido los siguientes:

1. Implementar un videojuego funcional con ventana gráfica en Pygame.
2. Aplicar clases y objetos para representar los elementos del juego.
3. Usar encapsulamiento en atributos críticos (vidas, velocidad, puntos).
4. Diseñar una jerarquía de herencia para tipos de enemigos.
5. Implementar polimorfismo mediante métodos sobrescritos.
6. Gestionar colisiones, puntuación, vidas y estados de partida.
7. Integrar entrada de usuario, audio, fuentes y control del tiempo.
8. Organizar el proyecto en módulos separados por responsabilidad.
9. Documentar técnicamente el diseño y las decisiones tomadas.

---

## 3. Tecnologías utilizadas

### Python
Lenguaje principal del proyecto. Se ha utilizado para programar toda la lógica del juego, estructurar clases y organizar módulos.

### Pygame
Librería usada para:

- Crear la ventana y renderizar gráficos.
- Capturar entrada de teclado.
- Gestionar sprites y colisiones.
- Controlar tiempo/FPS y bucle principal.
- Reproducir sonido y música.
- Renderizar textos y fuentes.

### Módulos estándar adicionales
Se han empleado módulos de Python como `random`, `os`, `math` y `struct` para generación de enemigos, gestión de rutas y síntesis de audio de respaldo.

---

## 4. Diseño del juego

### Mecánicas principales

- El jugador mueve su nave con `WASD` o flechas.
- Dispara con la tecla `ESPACIO`.
- Aparecen enemigos y obstáculos de forma periódica.
- Los enemigos pueden disparar al jugador.
- Existen power-ups de vida o puntos.
- El jugador pierde vidas al recibir impactos o chocar.
- Se gana al alcanzar la puntuación objetivo o aguantar el tiempo de partida.

### Personajes y objetos

- **Jugador**: nave controlable por teclado.
- **Enemigo básico**: enemigo estándar con velocidad media.
- **Enemigo rápido**: enemigo más veloz con movimiento en zig-zag.
- **Disparo**: proyectiles tanto del jugador como de enemigos.
- **Obstáculo**: meteoritos que caen y dañan al contacto.
- **PowerUp**: bonus de vida o de puntuación.

### Reglas del juego

1. El jugador empieza con 3 vidas.
2. Cada enemigo destruido suma puntos.
3. Si las vidas llegan a 0, aparece pantalla de `Game Over`.
4. Si se llega al objetivo de puntos o al tiempo límite, aparece `Victoria`.
5. Al final de partida se puede reiniciar (`R`) o salir (`ESC`).

---

## 5. Diseño orientado a objetos

### Clases utilizadas

El proyecto está dividido en clases con responsabilidades claras:

- `Juego`: controla el bucle principal, estado y reglas.
- `Jugador`: control del personaje principal.
- `Disparo`: representación de proyectiles.
- `Enemigo` (clase base): comportamiento común de enemigos.
- `EnemigoBasico` y `EnemigoRapido`: especializaciones de enemigo.
- `Obstaculo`: objetos que caen y dañan al jugador.
- `PowerUp`: objetos beneficiosos coleccionables.
- `AudioManager`: sistema de efectos y música.

### Relaciones de herencia

Se implementa la jerarquía:

- `Enemigo`
  - `EnemigoBasico`
  - `EnemigoRapido`

Con esto se reutiliza el comportamiento común y se extienden variantes específicas.

### Encapsulamiento

Se ha aplicado encapsulamiento en atributos clave:

- En `Jugador`: `__vida`, `__velocidad`, `__cooldown_disparo`, `__tiempo_ultimo_disparo`.
- En `Enemigo`: `__puntos`.

El acceso y modificación se realiza mediante getters y setters (`get_vida`, `set_vida`, `get_velocidad`, `set_velocidad`, `get_puntos`, `set_puntos`).

### Polimorfismo

Hay polimorfismo en la jerarquía de enemigos:

- Método común `update()` definido en la clase base `Enemigo`.
- Método `update()` sobrescrito en `EnemigoRapido` para añadir movimiento en zig-zag, manteniendo la interfaz común.

Además, ambos tipos de enemigo comparten método `dibujar()` e `intentar_disparar()`, lo que permite tratarlos de forma uniforme.

---

## 6. Explicación de las clases principales

### Clase `Juego`

Es el núcleo de la aplicación.

Responsabilidades:

- Inicializar Pygame y la ventana.
- Cargar fuentes y sistema de audio.
- Crear y gestionar grupos de sprites.
- Controlar eventos de teclado y cierre.
- Actualizar entidades con movimiento dependiente de FPS (`dt`).
- Resolver colisiones entre entidades.
- Administrar puntuación, vidas, victoria y derrota.
- Dibujar escena y elementos UI.

Métodos clave:

- `_gestionar_eventos()`
- `_spawnear_objetos()`
- `_resolver_colisiones()`
- `_actualizar_estado_partida()`
- `ejecutar()`
- `reiniciar()`

### Clase `Jugador`

Representa la nave del usuario.

Responsabilidades:

- Gestionar movimiento con entrada de usuario.
- Limitar su posición a la pantalla.
- Gestionar vidas y velocidad encapsuladas.
- Crear disparos con cooldown.

Métodos destacados:

- `mover(dt, teclas, ancho, alto)`
- `puede_disparar(tiempo_actual)`
- `disparar(tiempo_actual)`
- `recibir_danio(danio)`

### Clase `Enemigo` y subclases

`Enemigo` define comportamiento común para todos los enemigos.

Responsabilidades:

- Movimiento vertical base.
- Vida y daño recibido.
- Valor en puntos.
- Capacidad de disparo.

`EnemigoBasico` define sprite y stats normales.

`EnemigoRapido` redefine `update()` para comportamiento polimórfico más agresivo (zig-zag).

### Clase `Disparo`

Encapsula los proyectiles.

Responsabilidades:

- Direccionar movimiento (sube o baja según propietario).
- Guardar daño y tipo de propietario (`jugador` o `enemigo`).
- Destruirse cuando sale de pantalla.

### Clase `Obstaculo`

Genera meteoritos con tamaño y velocidad aleatorios.

Responsabilidades:

- Descender por pantalla.
- Provocar daño por colisión directa.

### Clase `PowerUp`

Objeto de mejora aleatoria.

Tipos:

- `vida`: aumenta la vida del jugador.
- `puntos`: incrementa puntuación.

### Clase `AudioManager`

Gestiona sonido y música.

Responsabilidades:

- Inicializar mixer.
- Reproducir efectos (`disparo`, `explosion`, `powerup`, `gameover`).
- Mantener música de fondo.

Para no depender de ficheros externos obligatorios, incluye síntesis simple de tonos como respaldo.

---

## 7. Problemas encontrados y soluciones

### Problema 1: Dependencia de recursos externos

Dificultad: normalmente Pygame requiere imágenes, audios y fuentes externas, y si faltan puede fallar la ejecución.

Solución:

- Se dibujaron sprites con primitivas de Pygame (`draw.polygon`, `draw.circle`, `draw.rect`) para evitar dependencias de imágenes.
- Se añadió sistema de audio con tonos sintéticos de fallback.
- Para fuentes, se intenta cargar una fuente importada desde `assets/fonts` y si no existe se utiliza una fuente del sistema.

### Problema 2: Movimiento consistente en distintos equipos

Dificultad: sin delta time (`dt`) la velocidad cambia según FPS.

Solución:

- Todo movimiento de entidades utiliza factor `dt` para escalar desplazamientos.

### Problema 3: Organización de colisiones

Dificultad: hay múltiples tipos de colisiones (disparos, enemigos, obstáculos, power-ups).

Solución:

- Se centralizó la lógica en `_resolver_colisiones()` y se separó por casos para legibilidad.

### Problema 4: Gestión de estados de juego

Dificultad: evitar mezclar lógica de juego activo con pantalla final.

Solución:

- Se implementó la variable de estado (`jugando`, `game_over`, `victoria`) y condicionales claras en actualización y eventos.

---

## 8. Mejoras futuras

Si se dispusiera de más tiempo, se proponen las siguientes mejoras:

1. Añadir menú principal con selección de dificultad.
2. Incluir jefe final con patrones de ataque complejos.
3. Implementar sistema de niveles y progresión.
4. Guardar récord de puntuación en fichero.
5. Sustituir gráficos programáticos por sprites artísticos.
6. Integrar música en archivos reales (`.ogg`/`.wav`) y más efectos.
7. Incorporar animaciones de explosión y partículas.
8. Añadir pantalla de pausa y opciones de audio.
9. Incluir soporte para mando.

---

## Estructura final del proyecto

```text
game_project/
  main.py
  juego.py
  config.py
  jugador.py
  enemigo.py
  disparo.py
  obstaculo.py
  powerup.py
  audio_manager.py
  requirements.txt
  assets/
    images/
    sounds/
    fonts/
  documentos/
    memoria_practica_3_3.md
```

---

## Conclusión

La práctica cumple los requisitos técnicos obligatorios del enunciado: uso de clases, encapsulamiento, herencia, polimorfismo, colisiones, puntuación/vidas, pantalla final y módulos de entrada, audio, fuentes y tiempo. Además, se ha mantenido una organización modular del código para facilitar su mantenimiento, ampliación y presentación en clase.
