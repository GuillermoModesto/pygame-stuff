import pygame
import math
from bala import Bala

class Arma:

    def __init__(self, player):
        # VARIABLES DEL JUEGO PRINCIPAL
        self.settings = player.settings
        self.pantalla = player.pantalla_juego
        self.rect_pantalla = self.pantalla.get_rect()
        
        # IMAGENES
        self.imagen_original = pygame.image.load("./imagenes/pistola.png").convert_alpha()
        self.imagen_sin_rotar = self.imagen_original
        self.imagen_rotada = pygame.transform.flip(self.imagen_original, False, True)

        # RECT
        self.rect = self.imagen_original.get_rect()
        # Transforar la posición central en un vector en vez de tupla para trabajar con ella
        self.start = pygame.math.Vector2(self.rect.center)

        # PARA ROTACION Y MOVIMIENTO
        self.pivot = pygame.math.Vector2(player.rect.centerx, player.rect.centery) # el centro del giro
        self.circun_giro = self.pivot + (self.settings.player_size, 0) # define la circunferencia que recorrerá el objeto que gira

        # MUNICION
        self.balas = pygame.sprite.Group()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, player):
        self.check_movimiento(player)
        self.check_disparo()

    def set_posicion(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def check_movimiento(self, player):
        #Actualizar punto de pivot y arco de giro
        self.pivot = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        self.circun_giro = self.pivot + (self.settings.player_size + (self.settings.player_size//3), 0)

        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        
        #vector de distancia entre player y mouse
        mouse_offset = mouse_pos - self.pivot

        #ángulo del offset con el eje x del player (empezando a la derecha en 0, clockwise hasta -180, counter-clockwise hasta 180)
        mouse_angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x)) 

        if mouse_pos.x < player.rect.centerx:
            self.imagen_original =  self.imagen_rotada
        else:
            self.imagen_original = self.imagen_sin_rotar

        #gira la imagen con el ángulo de antes
        self.imagen_original = pygame.transform.rotate(self.imagen_original, mouse_angle)

        #calcula el nuevo centro del rect
        offset = self.pivot + (self.circun_giro - self.pivot).rotate(-mouse_angle)

        #actializa el centro del rect y su versión en vector
        self.rect = self.imagen_original.get_rect(center = offset)
        self.start = pygame.math.Vector2(self.rect.center)

    def check_disparo(self):
        if len(self.balas) > 0:
            for bala in self.balas.sprites():
                bala.posicion += bala.velocidad

            for bala in self.balas.copy():
                if bala.rect.bottom <= 0 or bala.rect.top >= self.rect_pantalla.bottom or bala.rect.right <= 0 or bala.rect.left >= self.rect_pantalla.right:
                    self.balas.remove(bala)

    def disparar(self, dt):
        distancia = pygame.mouse.get_pos() - self.start

        if distancia != 0:
            velocidad = distancia.normalize() * self.settings.bullet_speed * dt
        else:
            velocidad = 0

        nueva_bala = Bala(self, self.start, velocidad)
            
        self.balas.add(nueva_bala)

    def blitme(self):
        self.pantalla.blit(self.imagen_original, self.rect)

    def blitbullets(self):
        for bala in self.balas.sprites():
            bala.rect.center = (int(bala.posicion.x), int(bala.posicion.y))
            bala.blitme()