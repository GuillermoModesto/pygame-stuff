import pygame
from arma import Arma

class Player:

    def __init__(self, game):
        # VARIABLES DEL JUEGO PRINCIPAL
        self.settings = game.settings
        self.pantalla_juego = game.pantalla
        self.rect_pantalla_juego = self.pantalla_juego.get_rect()

        # RECT
        self.rect = pygame.Rect((0, 0), (game.settings.player_size, game.settings.player_size))

        # ARMAS
        self.arma = Arma(self)
        self.arma.set_posicion(self.rect.x, self.rect.y)
        self.arma.start = pygame.math.Vector2(self.arma.rect.center) #Inicio del vector de direccion jugador -> arma

        # PARA EL MOVIMIENTO
        self.mov_arriba = False
        self.mov_abajo = False
        self.mov_derecha = False
        self.mov_izquierda = False

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, dt):
        self.check_movimiento(dt)

    def set_posicion(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def check_movimiento(self, dt):
        if self.mov_abajo or self.mov_arriba or self.mov_derecha or self.mov_izquierda:
            self.arma.start = pygame.math.Vector2(self.rect.center)

        if self.mov_arriba and self.rect.top > self.rect_pantalla_juego.top:
            self.y -= self.settings.player_speed * dt
            self.rect.centery = self.y
        if self.mov_abajo and self.rect.bottom < self.rect_pantalla_juego.bottom:
            self.y += self.settings.player_speed * dt
            self.rect.centery = self.y
        if self.mov_izquierda and self.rect.left > self.rect_pantalla_juego.left:
            self.x -= self.settings.player_speed * dt
            self.rect.centerx = self.x
        if self.mov_derecha and self.rect.right < self.rect_pantalla_juego.right:
            self.x += self.settings.player_speed * dt
            self.rect.centerx = self.x

    