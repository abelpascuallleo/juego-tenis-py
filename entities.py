import pygame
import random
from settings import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((TAMANO_BOLA, TAMANO_BOLA), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, BLANCO, (0, 0, TAMANO_BOLA, TAMANO_BOLA))
        self.rect = self.image.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
        
        self.initial_speed = speed
        self.speed_x = speed * random.choice((1, -1))
        self.speed_y = speed * random.choice((1, -1))
        self.trail = []

    def update(self, dt, particles_group):
        # Guardar estela
        self.trail.append(self.rect.copy())
        if len(self.trail) > 10:
            self.trail.pop(0)

        # Movimiento basado en Delta Time
        self.rect.x += self.speed_x * dt
        self.rect.y += self.speed_y * dt

        # Colisión con paredes
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y *= -1
        if self.rect.bottom >= ALTO_PANTALLA:
            self.rect.bottom = ALTO_PANTALLA
            self.speed_y *= -1

    def bounce(self, paddle, particles_group):
        acceleration_factor = 1.05
        max_speed = 1000
        
        if abs(self.speed_x) < max_speed:
            self.speed_x *= -acceleration_factor
        else:
            self.speed_x *= -1

        diff_y = self.rect.centery - paddle.rect.centery
        bounce_factor = diff_y / (paddle.rect.height / 2)
        self.speed_y = bounce_factor * abs(self.speed_x)

        # Crear partículas
        direction = 1 if self.rect.centerx < ANCHO_PANTALLA / 2 else -1
        for _ in range(random.randint(10, 15)):
            particles_group.add(Particle(self.rect.centerx, self.rect.centery, direction))

    def reset(self):
        self.rect.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
        self.speed_x = self.initial_speed * random.choice((1, -1))
        self.speed_y = self.initial_speed * random.choice((1, -1))
        self.trail = []

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ANCHO_PALA, ALTO_PALA))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect(topleft=(x, y))

    def keep_in_bounds(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= ALTO_PANTALLA: self.rect.bottom = ALTO_PANTALLA

class PlayerPaddle(Paddle):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt
        self.keep_in_bounds()

class OpponentPaddle(Paddle):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed

    def update(self, dt, ball):
        if self.rect.centery < ball.rect.centery:
            self.rect.y += self.speed * dt
        if self.rect.centery > ball.rect.centery:
            self.rect.y -= self.speed * dt
        self.keep_in_bounds()

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        size = random.randint(2, 4)
        self.image = pygame.Surface((size, size))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(direction * random.uniform(100, 300), random.uniform(-200, 200))
        self.lifespan = 0.5 # Segundos de vida

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.kill()
