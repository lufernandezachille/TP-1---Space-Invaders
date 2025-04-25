import pygame
import sys
import subprocess 
import json

imagen_fondo = pygame.image.load("fondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (1000, 600))
imagen_tutorial = pygame.image.load("tutorial.png")
imagen_titulo = pygame.image.load("titulo.png")
imagen_titulo = pygame.transform.scale(imagen_titulo, (700, 115))

def obtener_top_ranking(ruta="ranking.json", top=3):
    try:
        with open(ruta, "r") as archivo:
            datos = json.load(archivo)

            datos_filtrados = [jugador for jugador in datos if "nombre" in jugador and "puntaje" in jugador]

            datos_ordenados = sorted(datos_filtrados, key=lambda x: x["puntaje"], reverse=True)

            return datos_ordenados[:top]

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def mostrar_ranking(pantalla, fuente, fondo_color=(0, 0, 0)):
    pantalla.fill(fondo_color)
    pantalla.blit(imagen_fondo, (0,0))
    top_ranking = obtener_top_ranking()

    titulo = fuente.render("RANKING", True, (255, 255, 0))
    pantalla.blit(titulo, (420, 150))

    for i, jugador in enumerate(top_ranking):
        texto = f"{i+1}. {jugador['nombre']} - {jugador['puntaje']} pts"
        texto_render = fuente.render(texto, True, (255, 255, 255))
        pantalla.blit(texto_render, (390, 250 + i * 60))

    texto_salir = fuente.render("Presiona ESC para volver", True, (200, 200, 200))
    pantalla.blit(texto_salir, (300, 500))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                esperando = False

def mostrar_tutorial(pantalla, fuente, fondo_color=(0, 0, 0)):
    pantalla.fill(fondo_color)
    pantalla.blit(imagen_tutorial, (0, 0))
    texto_salir = fuente.render("Presiona ESC para volver", True, (200, 200, 200))
    pantalla.blit(texto_salir, (300, 550))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                esperando = False

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                esperando = False

# Inicializar Pygame
pygame.init()
ANCHO, ALTO = 1000, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú Principal")
fuente = pygame.font.SysFont("lazydog", 45)
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 100, 255)
VIOLETA = (187, 115, 209)

# Opciones del menú
opciones = ["JUGAR", "TUTORIAL", "RANKING", "SALIR"]
botones = []

# Crear botones con sus posiciones
def crear_botones():
    botones.clear()
    for i, texto in enumerate(opciones):
        superficie = fuente.render(texto, True, VIOLETA)
        rect = superficie.get_rect(center=(ANCHO // 2, 250 + i * 80))
        botones.append((texto, superficie, rect))

def dibujar_menu():
    screen.fill(NEGRO)
    screen.blit(imagen_fondo, (0,0))
    screen.blit(imagen_titulo, (150, 100))
    for texto, superficie, rect in botones:
        screen.blit(superficie, rect)
    pygame.display.flip()

def menu_principal():
    crear_botones()
    while True:
        dibujar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    for texto, _, rect in botones:
                        if rect.collidepoint(evento.pos):
                            if texto == "JUGAR":
                                print("Iniciando juego...")
                                subprocess.run(["python", "space invaders.py"])
                                return
                            elif texto == "RANKING":
                                mostrar_ranking(screen, fuente)
                            elif texto == "TUTORIAL":
                                print("Mostrar tutorial")
                                mostrar_tutorial(screen, fuente)
                            elif texto == "SALIR":
                                pygame.quit()
                                sys.exit()

        clock.tick(60)

menu_principal()
