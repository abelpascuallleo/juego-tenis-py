# Copyright (c) 2024 abel
# Este software se distribuye bajo la Licencia MIT.
# Ver el archivo LICENSE para más detalles.

import pytest
import pygame
import sys
import os

# Añadimos la ruta del proyecto al path de Python para que pueda encontrar 'main.py'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Ball, PlayerPaddle, OpponentPaddle, ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_JUGADOR

# Inicializamos Pygame para poder usar sus objetos como pygame.Rect
pygame.init()

@pytest.fixture
def ball():
    TAMANO_BOLA_TEST = 20
    """Fixture que crea una instancia de Ball para las pruebas."""
    return Ball(ANCHO_PANTALLA / 2 - TAMANO_BOLA_TEST / 2, ALTO_PANTALLA / 2 - TAMANO_BOLA_TEST / 2, TAMANO_BOLA_TEST, 7)

@pytest.fixture
def player_paddle():
    """Fixture que crea una instancia de PlayerPaddle para las pruebas."""
    return PlayerPaddle(ANCHO_PANTALLA - 35, ALTO_PANTALLA / 2, 15, 100, VELOCIDAD_JUGADOR)


def test_ball_creation(ball):
    """Prueba que la bola se crea con los valores iniciales correctos."""
    assert ball.rect.centerx == ANCHO_PANTALLA / 2
    assert ball.rect.centery == ALTO_PANTALLA / 2
    assert ball.initial_speed == 7

def test_ball_move(ball):
    """Prueba que la bola se mueve correctamente."""
    initial_x, initial_y = ball.rect.x, ball.rect.y
    ball.move()
    assert ball.rect.x == initial_x + ball.speed_x
    assert ball.rect.y == initial_y + ball.speed_y

def test_ball_wall_collision_top(ball):
    """Prueba que la bola rebota en la pared superior."""
    ball.rect.top = -5
    initial_speed_y = ball.speed_y
    ball.check_wall_collision()
    assert ball.speed_y == -initial_speed_y

def test_ball_wall_collision_bottom(ball):
    """Prueba que la bola rebota en la pared inferior."""
    ball.rect.bottom = ALTO_PANTALLA + 5
    initial_speed_y = ball.speed_y
    ball.check_wall_collision()
    assert ball.speed_y == -initial_speed_y

def test_player_paddle_keep_in_bounds_top(player_paddle):
    """Prueba que la pala del jugador no se sale por arriba."""
    player_paddle.rect.top = -20
    player_paddle.keep_in_bounds()
    assert player_paddle.rect.top == 0

def test_player_paddle_keep_in_bounds_bottom(player_paddle):
    """Prueba que la pala del jugador no se sale por abajo."""
    player_paddle.rect.bottom = ALTO_PANTALLA + 20
    player_paddle.keep_in_bounds()
    assert player_paddle.rect.bottom == ALTO_PANTALLA

def test_opponent_paddle_follows_ball():
    """Prueba que la pala del oponente sigue a la bola."""
    opponent = OpponentPaddle(20, ALTO_PANTALLA / 2, 15, 100, 7)
    ball = Ball(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 + 100, 20, 7) # Bola por debajo de la pala

    initial_y = opponent.rect.y
    opponent.update(ball)
    assert opponent.rect.y > initial_y # Debería moverse hacia abajo

    ball.rect.centery = int(ALTO_PANTALLA / 2 - 100) # Bola por encima de la pala
    initial_y = opponent.rect.y
    opponent.update(ball)
    assert opponent.rect.y < initial_y # Debería moverse hacia arriba

def test_ball_bounce_on_paddle(ball, player_paddle):
    """Prueba que la bola invierte su dirección y crea partículas al rebotar."""
    # Colocamos la bola justo a la izquierda de la pala, moviéndose hacia ella
    ball.rect.right = player_paddle.rect.left
    ball.speed_x = 5  # Forzamos la velocidad hacia la derecha

    initial_speed_x = ball.speed_x
    particles = []

    ball.bounce(player_paddle, particles)

    # 1. La velocidad horizontal debe invertirse y aumentar ligeramente
    assert ball.speed_x < 0
    # 2. Se deben haber creado partículas
    assert len(particles) > 0