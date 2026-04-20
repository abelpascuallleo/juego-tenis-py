# Configuración y Constantes del Juego Tenis
import pygame

# --- Dimensiones ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# --- Colores (RGB) ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# --- Configuración de los Elementos ---
TAMANO_BOLA = 20
ANCHO_PALA = 15
ALTO_PALA = 100
PUNTUACION_GANADORA = 5
VELOCIDAD_JUGADOR = 600 # Velocidad en píxeles por segundo (para usar con Delta Time)

# --- Diccionario de Dificultades ---
DIFICULTADES = {
    "facil": {"oponente_velocidad": 300, "bola_velocidad": 350},
    "medio": {"oponente_velocidad": 450, "bola_velocidad": 450},
    "dificil": {"oponente_velocidad": 600, "bola_velocidad": 550},
}
