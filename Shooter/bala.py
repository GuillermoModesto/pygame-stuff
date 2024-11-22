import pygame
from pygame.sprite import Sprite

class Bala(Sprite):

    def __init__(self, arma, posicion, velocidad):
        super().__init__()
        self.pantalla = arma.pantalla
        
        self.posicion = posicion
        self.velocidad = velocidad
        self.imagen_original = pygame.image.load("./imagenes/bala_001.bmp").convert_alpha()
        self.rect = self.imagen_original.get_rect()

    def blitme(self):
        self.pantalla.blit(self.imagen_original, self.rect)