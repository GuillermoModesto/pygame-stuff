import pygame
from settings import Settings
from player import Player

class Game:

    def __init__(self):
        pygame.init()
        self.on = True
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.settings = Settings()
        self.fr = self.settings.frame_rate
        
        self.pantalla = pygame.display.set_mode((self.settings.ancho_pantalla, self.settings.alto_pantalla))
        self.rect_pantalla = self.pantalla.get_rect()
        pygame.display.set_caption("Shooter")

        self.player = Player(self)
        self.player.set_posicion(self.settings.ancho_pantalla//3, self.settings.alto_pantalla//3)

        self.enemigo = pygame.Rect(100, 100, 25, 25)

    def run_game(self):
        while self.on:
            # Delta time, para moviminetos independientes al frame rate (se multiplica a lo que sea)
            self.dt = self.clock.tick(self.fr) / 1000

            self._control_eventos()

            self.player.update(self.dt)

            self.player.arma.update(self.player)

            for bala in self.player.arma.balas:
                if bala.rect.colliderect(self.enemigo):
                    print("ouch")

            self._control_display()

#-------------------------------------------------------------------------------------------------------------------------------------
    
    def _control_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on = False

            elif event.type == pygame.KEYDOWN:
                self._cevent_kdown(event)

            elif event.type == pygame.KEYUP:
                self._cevent_kup(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._cevent_mdown(event)
            """
            elif event.type == pygame.MOUSEBUTTONUP:
                self._cevent_mup(event)"""
#-------------------------------------------------------------------------------------------------------------------------------------
    def _cevent_kdown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.on = False

        elif event.key == pygame.K_w:
            self.player.mov_arriba = True
        elif event.key == pygame.K_a:
            self.player.mov_izquierda = True
        elif event.key == pygame.K_s:
            self.player.mov_abajo = True
        elif event.key == pygame.K_d:
            self.player.mov_derecha = True
#-------------------------------------------------------------------------------------------------------------------------------------
    def _cevent_kup(self, event):
        if event.key == pygame.K_w:
            self.player.mov_arriba = False
        elif event.key == pygame.K_a:
            self.player.mov_izquierda = False
        elif event.key == pygame.K_s:
            self.player.mov_abajo = False
        elif event.key == pygame.K_d:
            self.player.mov_derecha = False
#-------------------------------------------------------------------------------------------------------------------------------------
    def _cevent_mdown(self, event):
        if event.button == 1: # RATON IZQUIERDO
            self.player.arma.disparar(self.dt)

        elif event.button == 2: # RATON PULSAR RUEDA
            pass

        elif event.button == 3: # RATON DERECHO
            pass
#-------------------------------------------------------------------------------------------------------------------------------------
    """def _cevent_mup(self, event):
        if event.button == 1: # RATON IZQUIERDO
            pass

        elif event.button == 2: # RATON PULSAR RUEDA
            pass

        elif event.button == 3: # RATON DERECHO
            pass"""

#-------------------------------------------------------------------------------------------------------------------------------------

    

    def _control_display(self):
        self.pantalla.fill(self.settings.color_fondo)

        self.player.arma.blitme()
        
        self.player.arma.blitbullets()
        
        pygame.draw.rect(self.pantalla, (0, 0, 0), self.enemigo)

        pygame.draw.rect(self.pantalla, self.settings.player_color, self.player.rect)

        pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------
        
    
"""--------------------------------------------------------------------------------------------------------------------------------"""

if __name__ == "__main__":
    juego = Game()
    juego.run_game()

pygame.quit()
        
