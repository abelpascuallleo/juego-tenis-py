# Copyright (c) 2024 abel
# Este software se distribuye bajo la Licencia MIT.
# Ver el archivo LICENSE para más detalles.
import pygame
import sys
import os
import random

# --- Constantes ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Colores (en formato RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# --- Configuración de los Elementos del Juego ---
TAMANO_BOLA = 20
ANCHO_PALA = 15
ALTO_PALA = 100
PUNTUACION_GANADORA = 5
VELOCIDAD_JUGADOR = 10 # Velocidad de movimiento para las palas de los jugadores

# --- Diccionario de Dificultades ---
DIFICULTADES = {
    "facil": {"oponente_velocidad": 5, "bola_velocidad": 6},
    "medio": {"oponente_velocidad": 7, "bola_velocidad": 7},
    "dificil": {"oponente_velocidad": 9, "bola_velocidad": 8},
}

# --- Clases del Juego ---

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS (o similar)
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ball:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed * random.choice((1, -1))
        self.speed_y = speed * random.choice((1, -1))
        self.initial_speed = speed
        self.trail = []

    def move(self):
        self.trail.append(self.rect.copy())
        if len(self.trail) > 10: # Limita la longitud de la estela
            self.trail.pop(0)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_wall_collision(self):
        if self.rect.top <= 0 or self.rect.bottom >= ALTO_PANTALLA:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (int(ANCHO_PANTALLA / 2), int(ALTO_PANTALLA / 2))
        self.speed_x = self.initial_speed * random.choice((1, -1))
        self.speed_y = self.initial_speed * random.choice((1, -1))
        self.trail = []

    def bounce(self, paddle, particle_list):
        # Aumentamos la velocidad con cada golpe, con un límite.
        acceleration_factor = 1.05
        max_speed_x = 15 # Límite de velocidad horizontal

        if abs(self.speed_x) < max_speed_x:
            self.speed_x *= -acceleration_factor
        else:
            self.speed_x *= -1

        # Calculamos la diferencia vertical entre el centro de la bola y la pala
        diff_y = self.rect.centery - paddle.rect.centery
        
        # Normalizamos la diferencia para obtener un factor de rebote
        bounce_factor = diff_y / (paddle.rect.height / 2)
        # La velocidad vertical ahora depende de la velocidad horizontal actual para mantener la proporción.
        self.speed_y = bounce_factor * abs(self.speed_x)

        # --- Creación de Partículas ---
        # Determinamos la dirección de las partículas (lejos de la pala)
        particle_direction = 1 if self.rect.centerx < ANCHO_PANTALLA / 2 else -1
        # Creamos entre 10 y 15 partículas
        for _ in range(random.randint(10, 15)):
            particle = Particle(self.rect.centerx, self.rect.centery, particle_direction)
            particle_list.append(particle)
        
    def draw(self, screen):
        # Dibujamos la estela
        for i, rect in enumerate(self.trail):
            # El color se desvanece a medida que se aleja
            alpha = (i + 1) * (255 // (len(self.trail) + 1))
            color = (alpha, alpha, alpha)
            pygame.draw.ellipse(screen, color, rect)
        # Dibujamos la pelota principal
        pygame.draw.ellipse(screen, BLANCO, self.rect)

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLANCO, self.rect)

    def keep_in_bounds(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= ALTO_PANTALLA:
            self.rect.bottom = ALTO_PANTALLA

class PlayerPaddle(Paddle):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height)
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.keep_in_bounds()

class OpponentPaddle(Paddle):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height)
        self.speed = speed

    def update(self, ball):
        if self.rect.centery < ball.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > ball.rect.centery:
            self.rect.y -= self.speed
        self.keep_in_bounds()

class Particle:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        # Partículas pequeñas de 2 a 4 píxeles
        self.size = random.randint(2, 4)
        # La velocidad horizontal es en la dirección opuesta al golpe
        self.speed_x = direction * random.uniform(1, 4)
        # La velocidad vertical es aleatoria hacia arriba o abajo
        self.speed_y = random.uniform(-3, 3)
        # Tiempo de vida en fotogramas (aprox. medio segundo a 60 FPS)
        self.lifespan = 30

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, BLANCO, (self.x, self.y, self.size, self.size))

def menu_principal(pantalla, fuentes):
    """
    Muestra el menú de inicio y espera a que el jugador haga clic en "Jugar".
    """
    reloj = pygame.time.Clock()

    titulo_texto = fuentes["titulo"].render("TENIS", True, BLANCO)
    rect_titulo = titulo_texto.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 100))

    # Crear botón para jugar
    boton_jugar = pygame.Rect(ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2, 300, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    return # Sale de la función para continuar

        pantalla.fill(NEGRO)
        pantalla.blit(titulo_texto, rect_titulo)

        pygame.draw.rect(pantalla, BLANCO, boton_jugar)
        texto_boton = fuentes["boton"].render("Jugar", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect(center=boton_jugar.center)
        pantalla.blit(texto_boton, rect_texto_boton)

        pygame.display.flip()
        reloj.tick(60)

def menu_dificultad(pantalla, fuentes):
    """Muestra el menú para elegir dificultad y devuelve la selección."""
    reloj = pygame.time.Clock()

    titulo_texto = fuentes["titulo"].render("ELIGE LA DIFICULTAD", True, BLANCO)
    rect_titulo = titulo_texto.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 150))

    # Crear botones para cada dificultad
    botones = {}
    pos_y_inicial = ALTO_PANTALLA / 2 - 80
    for i, dificultad in enumerate(DIFICULTADES.keys()):
        pos_y = pos_y_inicial + i * 80
        boton_rect = pygame.Rect(ANCHO_PANTALLA / 2 - 125, pos_y, 250, 60)
        botones[dificultad] = boton_rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for dificultad, rect in botones.items():
                    if rect.collidepoint(event.pos):
                        return dificultad # Devolvemos la dificultad elegida

        pantalla.fill(NEGRO)
        pantalla.blit(titulo_texto, rect_titulo)

        # Dibujar cada botón
        for dificultad, rect in botones.items():
            pygame.draw.rect(pantalla, BLANCO, rect)
            texto_boton = fuentes["boton"].render(dificultad.capitalize(), True, NEGRO)
            rect_texto_boton = texto_boton.get_rect(center=rect.center)
            pantalla.blit(texto_boton, rect_texto_boton)

        pygame.display.flip()
        reloj.tick(60)

def pantalla_fin_juego(pantalla, ganador_texto, fuentes):
    """
    Muestra la pantalla de fin de juego con opciones para rejugar o volver al menú.
    Devuelve True si se quiere volver a jugar, False para volver al menú.
    """
    reloj = pygame.time.Clock()

    texto_ganador = fuentes["titulo"].render(ganador_texto, True, BLANCO)
    rect_ganador = texto_ganador.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 100))

    boton_rejugar = pygame.Rect(ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 + 50, 300, 60)
    texto_rejugar = fuentes["boton"].render("Volver a Jugar", True, NEGRO)
    rect_texto_rejugar = texto_rejugar.get_rect(center=boton_rejugar.center)

    boton_menu = pygame.Rect(ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 + 130, 300, 60)
    texto_menu = fuentes["boton"].render("Menú Principal", True, NEGRO)
    rect_texto_menu = texto_menu.get_rect(center=boton_menu.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rejugar.collidepoint(event.pos):
                    return True  # Volver a jugar
                if boton_menu.collidepoint(event.pos):
                    return False # Volver al menú

        pantalla.fill(NEGRO)
        pantalla.blit(texto_ganador, rect_ganador)
        pygame.draw.rect(pantalla, BLANCO, boton_rejugar)
        pantalla.blit(texto_rejugar, rect_texto_rejugar)
        pygame.draw.rect(pantalla, BLANCO, boton_menu)
        pantalla.blit(texto_menu, rect_texto_menu)

        pygame.display.flip()
        reloj.tick(60)

def game_loop(pantalla, dificultad, fuentes):
    """
    Esta es la función principal que contendrá nuestro juego.
    """
    # --- Configuración basada en el modo de juego y la dificultad ---
    config = DIFICULTADES[dificultad]
    oponente_velocidad = config["oponente_velocidad"]
    bola_velocidad_inicial = config["bola_velocidad"]

    # --- Creación de los Objetos del Juego usando Clases ---
    ball = Ball(ANCHO_PANTALLA / 2 - TAMANO_BOLA / 2, ALTO_PANTALLA / 2 - TAMANO_BOLA / 2, TAMANO_BOLA, bola_velocidad_inicial)
    player = PlayerPaddle(ANCHO_PANTALLA - ANCHO_PALA - 20, ALTO_PANTALLA / 2 - ALTO_PALA / 2, ANCHO_PALA, ALTO_PALA, VELOCIDAD_JUGADOR)
    opponent = OpponentPaddle(20, ALTO_PANTALLA / 2 - ALTO_PALA / 2, ANCHO_PALA, ALTO_PALA, oponente_velocidad)

    # --- Variables de Puntuación y Estado ---
    puntuacion_jugador = 0
    puntuacion_oponente = 0
    paused = False
    reset_timer = 0 # Temporizador para el reinicio de la bola

    # --- Control de Tiempo ---
    reloj = pygame.time.Clock()

    # --- Lista para Partículas ---
    particles = []

    # --- Bucle de Partida Individual ---
    while True:
        # --- Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_x:
                    return # Salimos de game_loop para volver al menú principal

        # Si hay un temporizador de reinicio, no hacemos nada más hasta que termine
        if reset_timer > pygame.time.get_ticks():
            pygame.display.flip()
            reloj.tick(60)
            continue

        if not paused:
            # --- Lógica del Juego ---
            player.update()
            ball.move()
            opponent.update(ball)
            
            ball.check_wall_collision()
            
            if ball.rect.colliderect(player.rect):
                ball.bounce(player, particles)
            if ball.rect.colliderect(opponent.rect):
                ball.bounce(opponent, particles)

            # Lógica de Puntuación
            if ball.rect.right >= ANCHO_PANTALLA or ball.rect.left <= 0:
                if ball.rect.right >= ANCHO_PANTALLA:
                    puntuacion_oponente += 1
                else:
                    puntuacion_jugador += 1
                ball.reset()
                reset_timer = pygame.time.get_ticks() + 1000 # Esperar 1 segundo
            else:
                # Actualizar partículas
                for particle in particles:
                    particle.update()
                # Eliminar partículas muertas (con list comprehension para eficiencia)
                particles = [p for p in particles if p.lifespan > 0]

            # --- Dibujo ---
            pantalla.fill(NEGRO)
            player.draw(pantalla)
            opponent.draw(pantalla)
            ball.draw(pantalla)
            # Dibujar partículas
            for particle in particles:
                particle.draw(pantalla)
            pygame.draw.aaline(pantalla, BLANCO, (ANCHO_PANTALLA / 2, 0), (ANCHO_PANTALLA / 2, ALTO_PANTALLA))

            texto_jugador = fuentes["juego"].render(f"{puntuacion_jugador}", False, BLANCO)
            pantalla.blit(texto_jugador, (ANCHO_PANTALLA / 2 + 20, 20))
            texto_oponente = fuentes["juego"].render(f"{puntuacion_oponente}", False, BLANCO)
            pantalla.blit(texto_oponente, (ANCHO_PANTALLA / 2 - 50, 20))

            # Dibujamos el texto de ayuda en la parte superior
            info_texto = fuentes["info"].render("Mover: ↑/↓ | Salir: X | Pausa: P", True, BLANCO)
            pantalla.blit(info_texto, (10, 10))

            # --- Comprobación de Fin de Juego ---
            if paused: # Si el juego está en pausa, mostramos el texto "PAUSA"
                # Dibujamos una capa semitransparente
                overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150)) # Negro con 150 de alpha (0-255)
                pantalla.blit(overlay, (0, 0))
                # Dibujamos el texto de pausa
                texto_pausa = fuentes["titulo"].render("PAUSA", True, BLANCO)
                rect_pausa = texto_pausa.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2))
                pantalla.blit(texto_pausa, rect_pausa)

            ganador_texto = ""
            if puntuacion_jugador >= PUNTUACION_GANADORA:
                ganador_texto = "¡Has ganado!"
            if puntuacion_oponente >= PUNTUACION_GANADORA:
                ganador_texto = "¡Has perdido!"
                
            if ganador_texto:
                if not pantalla_fin_juego(pantalla, ganador_texto, fuentes):
                    return # Si el jugador elige "Menú Principal", salimos de game_loop
                else:
                    game_loop(pantalla, dificultad, fuentes) # Reiniciamos el juego

            # --- Actualización de la Pantalla ---
            pygame.display.flip()
            reloj.tick(60)

if __name__ == '__main__':
    # --- Inicialización General ---
    pygame.init()
    # Creamos la superficie principal donde dibujaremos todo.
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    # Le damos un título a la ventana.
    pygame.display.set_caption('Tenis con Pygame')

    # --- Cargar Icono ---
    try:
        icon = pygame.image.load(resource_path("icon.ico"))
        pygame.display.set_icon(icon)
    except (pygame.error, FileNotFoundError):
        print("¡Advertencia! No se pudo cargar el archivo de icono 'icon.ico'.")

    # --- Cargar Fuentes una sola vez ---
    fuentes = {
        "titulo": pygame.font.Font(None, 74),
        "boton": pygame.font.Font(None, 50),
        "juego": pygame.font.Font(None, 74),
        "info": pygame.font.Font(None, 24)
    }

    # Bucle principal del programa
    while True:
        menu_principal(pantalla, fuentes)
        dificultad_elegida = menu_dificultad(pantalla, fuentes)
        game_loop(pantalla, dificultad_elegida, fuentes)

        # Cuando game_loop termina (porque el usuario eligió "Menú Principal"),
        # el bucle vuelve a empezar, mostrando de nuevo el menú de inicio.

    pygame.quit()