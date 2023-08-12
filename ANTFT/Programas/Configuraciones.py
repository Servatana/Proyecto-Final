import pygame
import random
import Boton

pygame.init()

#reloj interno del juego (para medir duracion de animaciones y ataques)
reloj= pygame.time.Clock
fps= 60

#Ventana del juego
panel_inferior = 150
ancho_de_pantalla = 800
alto_de_pantalla = 400 + panel_inferior

pantalla= pygame.display.set_mode((ancho_de_pantalla, alto_de_pantalla))
pygame.display.set_caption ("ANTFT")

#Imagenes
    #Imagen del fondo o "background"
fondo = pygame.image.load("ANTFT/Imagenes/Backgrounds/Background_base.png").convert_alpha()
    #icono de la ventana
icono_ventana = pygame.imagen.load("ANTFT/Imagenes/Logos/Logo_ventana/Logito.png")
    #Cursor
cursor_ataque = pygame.image.load("ANTFT/Imagenes/Cursor/Ataque.png").convert_alpha()
"""cursor_curacion = pygame.image.load('Imagenes/Cursor/Curacion.png').convert_alpha()"""
    #Panel
panel = pygame.image.load("ANTFT/Imagenes/Panel_de_control/Panel.png").convert_alpha()
    #Victoria
logo_victoria = pygame.image.load("ANTFT/Imagenes/Logos/Victoria/Victory_Shield.png").convert_alpha()
    #Derrota
logo_derrota = pygame.image.load("ANTFT/Imagenes/Logos/Derrota/Defeat_Shield.png").convert_alpha()
    #Reintentar
logo_reinicio =pygame.image.load("ANTFT/Imagenes/Logos/Reintentar/ReintentarV2.png").convert_alpha()


pygame.display.set_icon(icono_ventana)

#Funcion para mostrar texto

def Mostrar_texto(Texto, fuente, color_texto, x , y):
    imagen = fuente.render(Texto, True, color_texto)
    pantalla.blit(imagen, (x, y))

#Fuente de textos
fuente = pygame.font.SysFont("Comic Sans", 25)


#Tipos de colores

Rojo = (255, 0, 0)
Verde = (0, 255, 0)

#Funcion para mostrar el fondo
def Mostrar_fondo():
    pantalla.blit(fondo, (0, 0))

#Funcion para mostrar el panel de control
def Mostrar_panel():
        #mostrar panel en rectangulo
    pantalla.blit(panel, (0, alto_de_pantalla - panel_inferior))
    #mostrar estadisticas del guerrero
    Mostrar_texto("Heroe, Salud:{Heroe.salud}", fuente, Rojo, 100, alto_de_pantalla - panel + 10)
    Mostrar_texto("Verdugo, Salud:{Verdugo.salud}", fuente, Rojo, 550, (alto_de_pantalla - panel) + 10)
    Mostrar_texto("Verdugo_compañero, Salud:{Verdugo.salud}", fuente, Rojo, 100, (alto_de_pantalla - panel) + 10 + 60)



#Variables/datos del juego

Guerrero_Actual = 1
Guerreros_Totales =3
Recarga_de_accion = 0
Espera_de_accion = 90
Atacar = False
Atacar2 = False
fin_de_juego =0
Accion = 0


clickear =False

#Clases de Personajes

class Personajes_Generales():
    def __init__(self, x, y, nombre, salud_maxima, fuerza, defensa):
        self.nombre = nombre
        self.salud = salud_maxima
        self.fuerza = fuerza

"""
#Clase de Sanador/Heales
class Sanador(Personajes_Generales):
    def __init__(self, salud_maxima=55, fuerza=4):
        self.salud = salud_maxima
        self.salud_maxima =salud_maxima
        self.fuerza = fuerza

        self.vivo = True
"""

#Clase de Guerrero/Brawler
class Guerrero(Personajes_Generales):
    def __init__(self, x, y, salud_maxima, fuerza, defensa):
        self.salud = salud_maxima
        self.salud_maxima =salud_maxima
        self.fuerza = fuerza
        self.defensa = defensa
        self.vivo = True
        self.Lista_animacion=[]
        self.Frame_contador = 0
        #0=Estatico , 1=Atacando , 2=Herido , 3=Muerto
        self.Accion = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

        
        #estatico
        Lista_cuantica1 = []
        for A in range(8):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Caballero/Pose_base/Estatico{A}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica1.append(imagen_del_personaje)
            self.Lista_animacion.append(Lista_cuantica1)
        #ataque
        Lista_cuantica2 =[]
        for B in range(6):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Caballero/Pose_de_ataque/Ataque{B}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica2.append(imagen_del_personaje)
            self.Lista_animacion.append(Lista_cuantica2)

        #herido(mendigado)
        Lista_cuantica3=[]
        for C in range(5):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Caballero/Pose_de_ataque/Ataque{C}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica3.append(imagen_del_personaje)
            self.Lista_animacion.append(Lista_cuantica3)

        #Muerte
        Lista_cuantica4=[]
        for D in range(10):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Caballero/Pose_muerte/Muerte_C{D}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica4.append(imagen_del_personaje)

        self.Lista_animacion.append(Lista_cuantica4)
        self.imagen_del_personaje = self.Lista_animacion[self.Accion][self.Frame_contador]
        self.area_de_imagen = self.imagen_del_personaje.get_rect()
        self.area_de_imagen_centro = (x , y)
    #"Imagen del personaje" es la imagen que se le da al propio personaje en el espacion, asi como "rect" es el rectangulo o "area"
    #que va a ocupar esa imagen espeficamente (Nota personal: Encuentra una imagen desente po favo)

    #Para que (algo) aparezca en la pantalla
    def Mostrar (self):
        pantalla.blit (self.imagen_del_personaje, self.area_de_imagen)

    #control de las animaciones del personaje (flujo de sprites)
    def Actualizar_animacion (self):
        Recarga_de_accion = 100
        self.imagen_del_personaje = self.Lista_animacion[self.Accion][self.Frame_contador]

        if pygame.time.get_ticks() - self.actualizar_tiempo > Recarga_de_accion:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.Frame_contador += 1

            #reinicio
        if self.Frame_contador >= len(self.Lista_animacion[self.Accion]):
            self.Frame_contador = 0
            if self.Accion == 3:
                self.Frame_contador = len(self.Lista_animacion[self,Accion]) -1
            self.Estatico()


    #Datos para la animacion de estatico
    def Estatico(self):
        self.Accion = 0
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

    #El nombre te lo dice un poco (Marca un objetivo para atacar)
    def Atacar(self, Objetivo):
        Aleatorio = random.randint(-10, 5)
        Daño = self.fuerza + Aleatorio
        Objetivo.salud -= Daño
        Objetivo.Herido2()
        if Objetivo.salud < 1:
            Objetivo.salud = 0
            Objetivo.vivo = False
            Objetivo.Muerto2

        #bases para animacion de ataque
        self.Accion = 1
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

    #Datos para animacion de daño recibido
    def Herido_Midigado(self):
        self.Accion = 2
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()


    def Muerto(self):
        self.Accion = 3
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

    def Reset (self):
        self.vivo =True
        self.salud = self.salud_maxima
        self.Frame_contador = 0
        self.Accion = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

class Guerrero_malo(Personajes_Generales):
    def __init__(self, x, y, salud_maxima, fuerza, defensa):
        self.salud = salud_maxima
        self.salud_maxima =salud_maxima
        self.fuerza = fuerza
        self.defensa = defensa
        self.vivo = True
        self.Lista_animacion2=[]
        self.Frame_contador = 0
        #0=Estatico , 1=Atacando , 2=Herido , 3=Muerto
        self.Accion = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

        #Estatico
        Lista_cuantica6= []
        for E in range(4):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Enemigos/Pose_estatica/Estatico{E}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica6.append(imagen_del_personaje)

        #Ataque
        Lista_cuantica7=[]
        for F in range(8):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Enemigos/Pose_de_ataque/Ataque{F}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica7.append(imagen_del_personaje)
        self.Lista_animacion2.append(Lista_cuantica7)

        #Herido
        Lista_cuantica8=[]
        for G in range(3):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Enemigos/Pose_de_daño_recibido/Pose_de_daño{G}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica8.append(imagen_del_personaje)
        self.Lista_animacion2.append(Lista_cuantica8)

        #Muerte
        Lista_cuantica9=[]
        for G in range(1):
            imagen_del_personaje = pygame.image.load(f"Imagenes/Personaje-s_jugables/Enemigos/Pose_de_daño_recibido/Pose_de_daño{G}.png")
            imagen_del_personaje = pygame.transform.scale(imagen_del_personaje, (imagen_del_personaje.get_width() * 3, imagen_del_personaje.get_height() * 3))
            Lista_cuantica9.append(imagen_del_personaje)
        self.Lista_animacion2.append(Lista_cuantica9)

        self.imagen_del_personaje = self.Lista_animacion2[self.Accion][self.Frame_contador]
        self.area_de_imagen = self.imagen_del_personaje.get_rect()
        self.area_de_imagen.centro = (x , y)
    def Mostrar2 (self):
        pantalla.blit (self.imagen_del_personaje, self.area_de_imagen)

    def Actualizar_animacion2 (self):
        Recarga_de_accion = 100
        self.imagen_del_personaje = self.Lista_animacion2[self.Accion][self.Frame_contador]

        if pygame.time.get_ticks() - self.actualizar_tiempo > Recarga_de_accion:
            self.actualizar_tiempo = pygame.time.get_ticks()
            self.Frame_contador += 1

        if self.Frame_contador >= len(self.Lista_animacion2[self.Accion]):
            self.Frame_contador = 0
            self.Estatico2

    def Estatico2(self):
        self.Accion = 0
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

        self.actualizar_tiempo = pygame.time.get_ticks()
    def Atacar2(self, Objetivo):

        Aleatorio = random.randint(-4, 10)
        Daño = self.fuerza + Aleatorio
        Objetivo.salud -= Daño - Objetivo.defensa
        Objetivo.Herido_Mitidago()
        if Objetivo.salud < 1:
            Objetivo.salud = 0
            Objetivo.vivo = False
            Objetivo.Muerto
        #bases para animacion de ataque
        self.Accion = 1
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

    #Datos para animacion de daño recibido
    def Herido2(self):
        self.Accion = 2
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()


    def Muerto2(self):
        self.Accion = 3
        self.Frame_contador = 0
        self.actualizar_tiempo = pygame.time.get_ticks()


    def Reset2 (self):
        self.vivo =True
        self.salud = self.salud_maxima
        self.Frame_contador = 0
        self.Accion = 0
        self.actualizar_tiempo = pygame.time.get_ticks()

class Barra_de_Vida ():
    def __init__(self, x, y, vida, vida_maxima):
        self.x = x
        self.y = y
        self.vida = vida
        self.vida_maxima = vida_maxima

    def Mostrar_BdV (self, vida):
        self.vida = vida
        porcentaje_de_vida = self.vida / self.vida_maxima
        pygame.draw.rect(pantalla, Rojo (self.x, self.y, 150, 20))
        pygame.draw.rect(pantalla, Verde (self.x, self.y, 150*porcentaje_de_vida, 20))
"""
class Textos_de_Daño(pygame.sprite.Sprite):
    def __init__ (self, x, y, daño, color):
        pygame.sprite.Sprite.__init__(self)
        self.imagen=fuente.render(daño, True, color)
        self.rec= self.imagen.get_rect

grupo_de_texto_de_daño = pygame.sprite.Group()
"""

#Datos de personajes
Heroe = Guerrero (200, 600, 100, 15, 5)

Verdugo = Guerrero_malo (550, 770, 100, 9, 0)
Verdugo_compañero = Guerrero_malo (550, 700, 100, 9, 0)


Heroe_barra_de_vida = Barra_de_Vida (100, alto_de_pantalla - panel_inferior + 40, Heroe.salud, Heroe.salud_maxima)
Verdugo_barra_de_vida = Barra_de_Vida (100, alto_de_pantalla - panel_inferior + 40, Verdugo.salud, Verdugo.salud_maxima)
Verdugo_compañero_barra_de_vida = Barra_de_Vida (100, alto_de_pantalla - panel_inferior + 40, Verdugo_compañero.salud, Verdugo_compañero.salud_maxima)


#Boton de reinicio

Boton_reinicio = Boton.Boton (pantalla, 330, 120, logo_reinicio, 120, 30)


while True:
    for evento in pygame.event.get():
        reloj.tick(fps)

        Mostrar_fondo


        Mostrar_panel
        Heroe_barra_de_vida.Mostrar_BdV(Heroe.salud)
        Verdugo_barra_de_vida.Mostrar_BdV(Verdugo.salud)
        Verdugo_compañero_barra_de_vida.Mostrar_BdV(Verdugo_compañero.salud)


        Heroe.Actualizar_animacion
        Heroe.Mostrar()

        Verdugo.Actualizar_animacion2
        Verdugo.Mostrar2
        Verdugo_compañero.Actualizar_animacion2
        Verdugo_compañero.Mostrar2


        """grupo_de_texto_de_daño."""

    if fin_de_juego == 0:
            #Control de las acciones del jugador
            Atacar = False
            Objetivo = None
            pos = pygame.mouse.get_pos()
            """if Verdugo.area_de_imagen.collidepoint(pos):
                pygame.mouse.set_visible(False)
                pantalla.blits(cursor_ataque, pos)
                if clickear == True and Verdugo == vivo:
                    Atacar == True
                    Objetivo = Verdugo
            if Verdugo_compañero.area_de_imagen.collidepoint(pos):
                pygame.mouse.set_visible(False)
                pantalla.blits(cursor_ataque, pos)
                if clickear == True and Verdugo_compañero == vivo:
                    Atacar == True
                    Objetivo == Verdugo_compañero"""



                #Turno del jugador
                #Chequeo de turno, si es que es valido
            if Heroe.vivo == True:
                if Guerrero_Actual == 1:
                    Recarga_de_accion += 1
                    if Recarga_de_accion >= Espera_de_accion:
                        if Atacar == True and Objetivo != None:
                            Heroe.Atacar(Objetivo)
                            Guerrero_Actual += 1
                            Recarga_de_accion = 0
            
            else:
                fin_de_juego = -1

                #Turno enemigo
            if Guerrero_Actual == 2:
                if Verdugo.vivo == True:
                    Recarga_de_accion += 1
                    if Recarga_de_accion >= Espera_de_accion:
                        Verdugo.Atacar2(Heroe)
                        Guerrero_Actual += 1
                        Recarga_de_accion = 0
                else:
                    Guerrero_Actual= 1
            if Guerrero_Actual == 2:
                if Verdugo_compañero.vivo == True:
                    Recarga_de_accion += 1
                    if Recarga_de_accion >= Espera_de_accion:
                        Verdugo_compañero.Atacar2(Heroe)
                        Guerrero_Actual += 1
                        Recarga_de_accion = 0
                else:
                    Guerrero_Actual= 1

            if Guerrero_Actual > Guerreros_Totales:
                Guerrero_Actual = 1

            if Verdugo and Verdugo_compañero != Verdugo.vivo and Verdugo_compañero.vivo:
                fin_de_juego = 1

            
            if fin_de_juego != 0:
                if fin_de_juego == 1:
                    pantalla.blit(logo_victoria, (250, 25))
                if fin_de_juego == -1:
                    pantalla.blit(logo_derrota, (250, 25))
                if Boton_reinicio.mostrar():
                    Heroe.Reset
                    Verdugo.Reset2
                    Verdugo_compañero.Reset2
                    Guerrero_Actual = 1
                    Recarga_de_accion
                    fin_de_juego = 0

            pygame.display.update

            if evento.type == pygame.quit:

        
                pygame.display.update
                pygame.quit()
