import pygame
import sys
import os
from settings import *
from entities import Ball, PlayerPaddle, OpponentPaddle
from ui import menu_principal, menu_dificultad, pantalla_fin

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def game_loop(pantalla, dificultad, fuentes):
    config = DIFICULTADES[dificultad]
    
    # Grupos de Sprites
    all_sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    
    ball = Ball(config["bola_velocidad"])
    player = PlayerPaddle(ANCHO_PANTALLA - ANCHO_PALA - 20, ALTO_PANTALLA // 2 - ALTO_PALA // 2, VELOCIDAD_JUGADOR)
    opponent = OpponentPaddle(20, ALTO_PANTALLA // 2 - ALTO_PALA // 2, config["oponente_velocidad"])
    
    all_sprites.add(player, opponent, ball)
    
    p_jugador = 0
    p_oponente = 0
    reloj = pygame.time.Clock()
    reset_timer = 0

    while True:
        dt = reloj.tick(60) / 1000.0 # Delta Time en segundos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return

        if pygame.time.get_ticks() < reset_timer:
            pantalla.fill(NEGRO)
            all_sprites.draw(pantalla)
            pygame.display.flip()
            continue

        # Actualización
        player.update(dt)
        opponent.update(dt, ball)
        ball.update(dt, particles)
        particles.update(dt)

        # Colisiones
        if pygame.sprite.collide_rect(ball, player):
            ball.bounce(player, particles)
        if pygame.sprite.collide_rect(ball, opponent):
            ball.bounce(opponent, particles)

        # Puntuación
        if ball.rect.right >= ANCHO_PANTALLA:
            p_oponente += 1
            ball.reset()
            reset_timer = pygame.time.get_ticks() + 1000
        elif ball.rect.left <= 0:
            p_jugador += 1
            ball.reset()
            reset_timer = pygame.time.get_ticks() + 1000

        # Dibujo
        pantalla.fill(NEGRO)
        
        # Estela de la bola
        for i, r in enumerate(ball.trail):
            alpha = (i + 1) * (255 // 11)
            color = (alpha, alpha, alpha)
            pygame.draw.ellipse(pantalla, color, r)
            
        all_sprites.draw(pantalla)
        particles.draw(pantalla)
        
        # UI Juego
        pygame.draw.aaline(pantalla, BLANCO, (ANCHO_PANTALLA/2, 0), (ANCHO_PANTALLA/2, ALTO_PANTALLA))
        pantalla.blit(fuentes["juego"].render(f"{p_oponente}", True, BLANCO), (ANCHO_PANTALLA/2 - 50, 20))
        pantalla.blit(fuentes["juego"].render(f"{p_jugador}", True, BLANCO), (ANCHO_PANTALLA/2 + 20, 20))

        if p_jugador >= PUNTUACION_GANADORA or p_oponente >= PUNTUACION_GANADORA:
            ganador = "¡GANASTE!" if p_jugador >= PUNTUACION_GANADORA else "¡PERDISTE!"
            pantalla_fin(pantalla, ganador, fuentes)
            return

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Tenis PY - Refactored")
    
    fuentes = {
        "titulo": pygame.font.Font(None, 80),
        "boton": pygame.font.Font(None, 40),
        "juego": pygame.font.Font(None, 74)
    }

    while True:
        menu_principal(pantalla, fuentes)
        dif = menu_dificultad(pantalla, fuentes)
        game_loop(pantalla, dif, fuentes)