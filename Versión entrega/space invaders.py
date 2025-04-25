import pygame
import json
import os
#inicializar pygame
pygame.init()
ancho_ventana = 1000
alto_ventana = 600
screen = pygame.display.set_mode((ancho_ventana, alto_ventana))
clock = pygame.time.Clock()
#musiquita y sonidos
pygame.mixer.init()
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.set_volume(0.2) 
pygame.mixer.music.play(-1) 

sonido_disparo = pygame.mixer.Sound("disparo.wav")
sonido_explosion = pygame.mixer.Sound("explosion.wav")
sonido_disparo.set_volume(0.5)
sonido_explosion.set_volume(0.2)

#fotos
imagen_cohete = pygame.image.load("cohete.png")
imagen_cohete = pygame.transform.scale(imagen_cohete, (60, 60))

imagen_cohete2 = pygame.image.load("cohete2.png")
imagen_cohete2 = pygame.transform.scale(imagen_cohete2, (60, 60))

imagen_bala = pygame.image.load("bala.png")
imagen_bala = pygame.transform.scale(imagen_bala, (10, 20))

imagen_bala2 = pygame.image.load("bala2.png")
imagen_bala2 = pygame.transform.scale(imagen_bala2, (10, 20))

imagen_explosion = pygame.image.load("explosion.png")
imagen_explosion = pygame.transform.scale(imagen_explosion, (60, 60))

imagen_fondo = pygame.image.load("fondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ancho_ventana, alto_ventana))

imagen_corazon = pygame.image.load("corazon.png")
imagen_corazon = pygame.transform.scale(imagen_corazon, (40, 40))

#cosas de las balas
class Bala:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 3
        self.imagen = imagen_bala

    def mover(self):
        self.y -= self.velocidad


    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
   
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.imagen.get_width(), self.imagen.get_height())

class Bala2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 3
        self.imagen = imagen_bala2

    def mover(self):
        self.y -= self.velocidad


    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
   
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.imagen.get_width(), self.imagen.get_height())
   
balas = []
TIEMPO_ENTRE_BALAS = 800
ultima_bala = 0

balas2 = []
ultima_bala2 = 0

#cohetes 1 y 2
class Cohete:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 1
        self.imagen = imagen_cohete
        self.balas = []
        self.vidas = 3
        self.muerto = False

    def mover(self, teclas):
        if not self.muerto:
            if teclas[pygame.K_LEFT]:
                self.x -= self.velocidad
            if teclas[pygame.K_RIGHT]:
                self.x += self.velocidad
            if self.x < 0:
                self.x = 0
            if self.x > ancho_ventana - self.imagen.get_width():
                self.x = ancho_ventana - self.imagen.get_width()

    def disparar(self):
        if not self.muerto:
            x_bala = self.x + self.imagen.get_width() // 2 - imagen_bala.get_width() // 2
            y_bala = self.y
            nueva_bala = Bala(x_bala, y_bala)
            self.balas.append(nueva_bala)
            sonido_disparo.play()

    def actualizar_balas(self, pantalla):
        for bala in self.balas[:]:
            bala.mover()
            bala.dibujar(pantalla)
            if bala.y < 0:
                self.balas.remove(bala)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

class Cohete2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 1
        self.imagen = imagen_cohete2
        self.balas = []
        self.vidas = 3
        self.muerto = False

    def mover(self, teclas):
        if not self.muerto:
            if teclas[pygame.K_LEFT]:
                self.x -= self.velocidad
            if teclas[pygame.K_RIGHT]:
                self.x += self.velocidad
            if self.x < 0:
                self.x = 0
            if self.x > ancho_ventana - self.imagen.get_width():
                self.x = ancho_ventana - self.imagen.get_width()

    def disparar(self):
        if not self.muerto:
            x_bala = self.x + self.imagen.get_width() // 2 - imagen_bala.get_width() // 2
            y_bala = self.y
            nueva_bala = Bala(x_bala, y_bala)
            self.balas.append(nueva_bala)
            sonido_disparo.play()

    def actualizar_balas(self, pantalla):
        for bala in self.balas[:]:
            bala.mover()
            bala.dibujar(pantalla)
            if bala.y < 0:
                self.balas.remove(bala)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

#aliens
class Alien:
    def __init__(self, x, y, velocidad, vida, imagen, tipo_id):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.vida = vida
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, (30, 30)) 
        self.tipo = tipo_id
        self.puntos = {1: 100, 2: 50, 3: 10}.get(self.tipo, 10) 

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida <= 0:
            return True
        return False
   
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.imagen.get_width(), self.imagen.get_height())

tipos_alien = [
    {"velocidad": 0.1, "vida": 3, "imagen": "alien3.png"},
    {"velocidad": 0.1, "vida": 2, "imagen": "alien2.png"},
    {"velocidad": 0.1, "vida": 1, "imagen": "alien1.png"},  
]

#más variables globales
aliens = []
espacio_x = 40
espacio_y = 40
inicio_x = 70
inicio_y = 50
       
direccion = 1
paso_lateral = 10
paso_vertical = 10
puntaje_jugador1 = 0
puntaje_jugador2 = 0

TIEMPO_ENTRE_PASOS = 600
ultimo_paso = pygame.time.get_ticks()

#explosiones
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagen = imagen_explosion
        self.inicio = pygame.time.get_ticks()
        self.duracion = 30

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y)) 
        sonido_explosion.play() 

    def ha_terminado(self):
        return pygame.time.get_ticks() - self.inicio > self.duracion

explosiones = []

#proyectiles
class ProyectilAlien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 2
        self.imagen = pygame.transform.scale(pygame.image.load("misil.png"), (30, 30))

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.imagen.get_width(), self.imagen.get_height())

#escudos
class BloqueEscudo:
    def __init__(self, x, y):
        self.ancho = 10
        self.alto = 10
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.color = (0, 255, 0)  # Verde
        self.activo = True

    def dibujar(self, pantalla):
        if self.activo:
            pygame.draw.rect(pantalla, self.color, self.rect)

    def destruir(self):
        self.activo = False

mostrar_nivel = True
pedir_nombre = True
esperando_generar_aliens = True
nivel = 1
TIEMPO_ENTRE_PASOS = 1000  
TIEMPO_ENTRE_DISPAROS_ALIEN = 2000

proyectiles_alien = []
ultimo_disparo_alien = pygame.time.get_ticks()

#funciones
def mostrar_pantalla_game_over():
    fuente = pygame.font.Font(None, 100)
    texto = fuente.render("GAME OVER", True, (255, 0, 0))
    texto_rect = texto.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))

    screen.fill((0, 0, 0))
    screen.blit(imagen_fondo, (0,0))
    screen.blit(texto, texto_rect)
    pygame.display.flip()

    esperar = True
    while esperar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                esperar = False

def mostrar_mensaje_nivel(nivel):
    fuente = pygame.font.Font(None, 70)
    texto = fuente.render(f"Nivel {nivel}", True, (255, 255, 0))
    texto_rect = texto.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    screen.fill((0, 0, 0))
    screen.blit(imagen_fondo, (0,0))
    screen.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.delay(1500)

def seleccionar_modo(screen):
    fuente = pygame.font.Font(None, 50)
    boton_1 = pygame.Rect(200, 250, 250, 60)
    boton_2 = pygame.Rect(550, 250, 250, 60)
    seleccionando = True
    modo_dos_jugadores = False  

    while seleccionando:
        screen.fill((0, 0, 0))
        screen.blit(imagen_fondo, (0,0))

        pygame.draw.rect(screen, (100, 100, 255), boton_1)
        pygame.draw.rect(screen, (100, 255, 100), boton_2)

        texto1 = fuente.render("1 Jugador", True, (255, 255, 255))
        texto2 = fuente.render("2 Jugadores", True, (255, 255, 255))
        screen.blit(texto1, (boton_1.x + 40, boton_1.y + 10))
        screen.blit(texto2, (boton_2.x + 25, boton_2.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_1.collidepoint(event.pos):
                    modo_dos_jugadores = False
                    seleccionando = False
                elif boton_2.collidepoint(event.pos):
                    modo_dos_jugadores = True
                    seleccionando = False

        pygame.display.flip()

    return modo_dos_jugadores

def pedir_nombre(screen, font, jugador_numero):
    nombre = ""
    escribiendo = True

    while escribiendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre.strip() != "":
                    escribiendo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12:
                        nombre += event.unicode

        screen.fill((0, 0, 0))
        screen.blit(imagen_fondo, (0,0))
        texto = font.render(f"Ingresá tu nombre, Jugador {jugador_numero}:", True, (255, 255, 255))
        nombre_render = font.render(nombre, True, (0, 255, 0))

        screen.blit(texto, (100, 200))
        screen.blit(nombre_render, (100, 250))
        pygame.display.flip()
    
    return nombre

def generar_aliens_para_nivel(nivel):
    aliens_generados = []
    for fila in range(5):
        if fila == 0:
            tipo = tipos_alien[0]
            tipo_id = 1
        elif fila in [1, 2]:
            tipo = tipos_alien[1]
            tipo_id = 2
        else:
            tipo = tipos_alien[2]
            tipo_id = 3

        for columna in range(11):
            x = inicio_x + columna * espacio_x
            y = inicio_y + fila * espacio_y
            nuevo_alien = Alien(x, y, tipo["velocidad"] + nivel * 0.05, tipo["vida"], tipo["imagen"], tipo_id)
            aliens_generados.append(nuevo_alien)
    return aliens_generados

def almacenar_puntajes(nombre1, puntaje1, nombre2=None, puntaje2=None, archivo='ranking.json'):
    if not os.path.exists(archivo):
        with open(archivo, 'w') as f:
            json.dump([], f)

    with open(archivo, 'r') as f:
        datos = json.load(f)

    datos.append({"nombre": jugador1_nombre, "puntaje": puntaje1})
    if nombre2 and puntaje2 is not None:
        datos.append({"nombre": jugador2_nombre, "puntaje": puntaje2})

    with open(archivo, 'w') as f:
        json.dump(datos, f, indent=4)

def crear_escudo(x_base, y_base):
    bloques = []
    for fila in range(4): 
        for columna in range(10): 
            x = x_base + columna * 10
            y = y_base + fila * 10
            bloques.append(BloqueEscudo(x, y))
    return bloques

velocidad_cohete = 4
cohete = Cohete(100, 530)
cohete2 = Cohete2(800, 530)
dos_jugadores = seleccionar_modo(screen)
puntuacion1 = 0
puntuacion2 = 0
bloques_escudo = []
for x in [150, 350, 550, 750]:
    bloques_escudo.extend(crear_escudo(x, 450))

#bucle principal del juego
running = True
while running:
    screen.fill("black")
    screen.blit(imagen_fondo, (0, 0))
    tiempo_actual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()
    for bloque in bloques_escudo:
        bloque.dibujar(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and tiempo_actual - ultima_bala > TIEMPO_ENTRE_BALAS:
                cohete.disparar()
                ultima_bala = tiempo_actual
            if dos_jugadores and event.key == pygame.K_LSHIFT:
                if (tiempo_actual - ultima_bala2 > TIEMPO_ENTRE_BALAS) and cohete2:
                    cohete2.disparar()
                    ultima_bala2 = tiempo_actual

    if pedir_nombre:
        screen = pygame.display.set_mode((1000, 600))
        font = pygame.font.Font(None, 40)
        if not dos_jugadores:
            jugador1_nombre = pedir_nombre(screen, font, 1)
            pedir_nombre = False
        if dos_jugadores:
            jugador1_nombre = pedir_nombre(screen, font, 1)
            jugador2_nombre = pedir_nombre(screen, font, 2)
            pedir_nombre = False
    
    if mostrar_nivel:
        mostrar_mensaje_nivel(nivel)
        esperando_generar_aliens = True
        mostrar_nivel = False

    if esperando_generar_aliens:
        aliens = generar_aliens_para_nivel(nivel)
        esperando_generar_aliens = False

    if not aliens:
        if nivel < 10:
            nivel += 1
            vidas = 3
            mostrar_mensaje_nivel(nivel)
            mostrar_nivel = True
        else:
            print("¡Ganaste el juego!")
            running = False

    if cohete: 
        cohete.mover(teclas)
    if cohete2:
        if dos_jugadores and cohete2:
            if teclas[pygame.K_a]:
                cohete2.x -= cohete2.velocidad
            if teclas[pygame.K_d]:
                cohete2.x += cohete2.velocidad

    if tiempo_actual - ultimo_paso >= TIEMPO_ENTRE_PASOS:
        if aliens:
            extremo_izquierdo = min(alien.x for alien in aliens)
            extremo_derecho = max(alien.x for alien in aliens) + 50
            if direccion == 1 and extremo_derecho + paso_lateral >= ancho_ventana:
                direccion = -1
                for alien in aliens:
                    alien.y += paso_vertical
            elif direccion == -1 and extremo_izquierdo - paso_lateral <= 0:
                direccion = 1
                for alien in aliens:
                    alien.y += paso_vertical
            for alien in aliens:
                alien.x += direccion * paso_lateral
            ultimo_paso = tiempo_actual

    aliens_por_columna = {}
    for alien in aliens:
        columna_encontrada = False
        for x_col in aliens_por_columna:
            if abs(alien.x - x_col) < 30:
                if alien.y > aliens_por_columna[x_col].y:
                    aliens_por_columna[x_col] = alien
                columna_encontrada = True
                break
        if not columna_encontrada:
            aliens_por_columna[alien.x] = alien

    if tiempo_actual - ultimo_disparo_alien > TIEMPO_ENTRE_DISPAROS_ALIEN:
        for alien in aliens_por_columna.values():
            if cohete and abs(alien.x - cohete.x) < 20:
                proyectiles_alien.append(ProyectilAlien(alien.x + 20, alien.y + 50))
                ultimo_disparo_alien = tiempo_actual
                break
            elif cohete2 and abs(alien.x - cohete2.x) < 20:
                proyectiles_alien.append(ProyectilAlien(alien.x + 20, alien.y + 50))
                ultimo_disparo_alien = tiempo_actual
                break

    if cohete:
        cohete.dibujar(screen)
        cohete.actualizar_balas(screen)

    if dos_jugadores and cohete2 and not cohete2.muerto:
        cohete2.dibujar(screen)
        cohete2.actualizar_balas(screen)

    for alien in aliens:
        alien.dibujar(screen)

    for proyectil in proyectiles_alien[:]:
        proyectil.mover()
        proyectil.dibujar(screen)
        if cohete and proyectil.get_rect().colliderect(pygame.Rect(cohete.x, cohete.y, 60, 60)):
            cohete.vidas -= 1
            proyectiles_alien.remove(proyectil)
            if cohete.vidas <= 0:
                explosiones.append(Explosion(cohete.x, cohete.y))
                cohete = None
        elif cohete2 and proyectil.get_rect().colliderect(pygame.Rect(cohete2.x, cohete2.y, 60, 60)):
            cohete2.vidas -= 1
            proyectiles_alien.remove(proyectil)
            if cohete2.vidas <= 0:
                explosiones.append(Explosion(cohete2.x, cohete2.y))
                cohete2 = None
        elif proyectil.y > alto_ventana:
            proyectiles_alien.remove(proyectil)

    if cohete and cohete.vidas <= 0 :
        cohete.muerto = True
        explosiones.append(Explosion(cohete.x, cohete.y)) 
        cohete.x = -999
        
    if cohete2 and cohete2.vidas <= 0 and not cohete2.muerto:
        cohete2.muerto = True
        explosiones.append(Explosion(cohete2.x, cohete2.y))
        cohete2.x = -999

    if cohete:
        for bala in cohete.balas[:]:
            for alien in aliens[:]:
                if bala.get_rect().colliderect(alien.get_rect()):
                    if alien.recibir_daño(1):
                        puntuacion1 += alien.puntos
                        aliens.remove(alien)
                        explosiones.append(Explosion(alien.x, alien.y))  
                    if bala in cohete.balas:
                        cohete.balas.remove(bala)
                    break

    if cohete2:
        for bala in cohete2.balas[:]:
            for alien in aliens[:]:
                if bala.get_rect().colliderect(alien.get_rect()):
                    if alien.recibir_daño(1):
                        puntuacion2 += alien.puntos
                        aliens.remove(alien)
                        explosiones.append(Explosion(alien.x, alien.y))  
                    if bala in cohete2.balas:
                        cohete2.balas.remove(bala)
                    break

    if cohete:
        for i in range(cohete.vidas):
            screen.blit(imagen_corazon, (10 + i * 50, 10))
        
    if cohete2 : 
        if dos_jugadores :
            for i in range(cohete2.vidas):
                screen.blit(imagen_corazon, (ancho_ventana - 50 * (i + 1), 10))
                
    font = pygame.font.SysFont("Arial", 24)

    texto1 = font.render(f"Jugador 1: {puntuacion1}", True, "white")
    screen.blit(texto1, (200, 10))

    if dos_jugadores:
        texto2 = font.render(f"Jugador 2: {puntuacion2}", True, "white")
        screen.blit(texto2, (ancho_ventana - 300, 10)) 

    for explosion in explosiones[:]:
        explosion.dibujar(screen)
        if explosion.ha_terminado():
            explosiones.remove(explosion)
    
    for bloque in bloques_escudo:
        bloque.dibujar(screen)

    for proyectil in proyectiles_alien[:]:
        for bloque in bloques_escudo:
            if bloque.activo and proyectil.get_rect().colliderect(bloque.rect):
                bloque.destruir()
                proyectiles_alien.remove(proyectil)
                break
    if cohete:
        for bala in cohete.balas[:]:
            for bloque in bloques_escudo:
                if bloque.activo and bala.get_rect().colliderect(bloque.rect):
                    bloque.destruir()
                    cohete.balas.remove(bala)
                    break
    if cohete2:
        for bala in cohete2.balas[:]:
            for bloque in bloques_escudo:
                if bloque.activo and bala.get_rect().colliderect(bloque.rect):
                    bloque.destruir()
                    cohete2.balas.remove(bala)
                    break

    if not cohete and not dos_jugadores:
        mostrar_pantalla_game_over() 
        almacenar_puntajes(jugador1_nombre, puntuacion1)
        running = False
    if dos_jugadores and not cohete and not cohete2:
        mostrar_pantalla_game_over() 
        almacenar_puntajes(jugador1_nombre, puntuacion1, jugador2_nombre, puntuacion2)
        running = False

    pygame.display.flip()
clock.tick(60)

pygame.quit()
