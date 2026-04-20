import pygame
import sys
from settings import *

def menu_principal(pantalla, fuentes):
    reloj = pygame.time.Clock()
    titulo_texto = fuentes["titulo"].render("TENIS PY", True, BLANCO)
    rect_titulo = titulo_texto.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 100))
    boton_jugar = pygame.Rect(ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2, 300, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    return

        pantalla.fill(NEGRO)
        pantalla.blit(titulo_texto, rect_titulo)
        pygame.draw.rect(pantalla, BLANCO, boton_jugar, border_radius=10)
        texto_boton = fuentes["boton"].render("JUGAR", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect(center=boton_jugar.center)
        pantalla.blit(texto_boton, rect_texto_boton)
        pygame.display.flip()
        reloj.tick(60)

def menu_dificultad(pantalla, fuentes):
    reloj = pygame.time.Clock()
    botones = {}
    for i, dif in enumerate(DIFICULTADES.keys()):
        rect = pygame.Rect(ANCHO_PANTALLA / 2 - 125, 220 + i * 80, 250, 60)
        botones[dif] = rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for dif, rect in botones.items():
                    if rect.collidepoint(event.pos):
                        return dif

        pantalla.fill(NEGRO)
        for dif, rect in botones.items():
            pygame.draw.rect(pantalla, BLANCO, rect, border_radius=10)
            txt = fuentes["boton"].render(dif.capitalize(), True, NEGRO)
            pantalla.blit(txt, txt.get_rect(center=rect.center))
        pygame.display.flip()
        reloj.tick(60)

def pantalla_fin(pantalla, ganador, fuentes):
    reloj = pygame.time.Clock()
    boton_menu = pygame.Rect(ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 + 50, 300, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_menu.collidepoint(event.pos):
                    return

        pantalla.fill(NEGRO)
        txt = fuentes["titulo"].render(ganador, True, BLANCO)
        pantalla.blit(txt, txt.get_rect(center=(ANCHO_PANTALLA/2, ALTO_PANTALLA/2 - 50)))
        pygame.draw.rect(pantalla, BLANCO, boton_menu, border_radius=10)
        txt_btn = fuentes["boton"].render("MENU", True, NEGRO)
        pantalla.blit(txt_btn, txt_btn.get_rect(center=boton_menu.center))
        pygame.display.flip()
        reloj.tick(60)
