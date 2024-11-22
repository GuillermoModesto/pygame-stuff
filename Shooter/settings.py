import pygame

class Settings:

    def __init__(self):
        self.frame_rate = 60

        # PANTALLA
        self.ancho_pantalla = 700
        self.alto_pantalla = 700
        self.color_fondo = (100, 100, 100)

        # JUGADOR
        self.player_size = 25
        self.player_color = (255, 0, 0)
        self.player_speed = 200
    
        # BALA
        self.bullet_speed = 900
        self.bullet_size = 5