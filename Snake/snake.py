import pygame
from random import randrange

class Snek:
    def __init__(self):

        pygame.init()
        self.alto_pantalla = 540
        self.ancho_pantalla = 540
        self.pantalla = pygame.display.set_mode((self.alto_pantalla, self.ancho_pantalla))
        pygame.display.set_caption("Sssnek")
        self.rect_pantalla = self.pantalla.get_rect()
        self.score_board = pygame.Rect(0, 0, 540, 40)
        self.clock = pygame.time.Clock()
        self.running = True

        self.size = 10
        self.velocidad_inicial = 12
        self.velocidad = self.velocidad_inicial
        self.upgrade_jump = 4
        self.next_upgrade = self.upgrade_jump
        self._crear_serpiente()

        self.font = pygame.font.Font(None, 28)
        self._crear_manzana()
        self.score = 0

        self.moving_up = False
        self.moving_down = True
        self.moving_left = False
        self.moving_right = False

    def run_game(self):
        while self.running:
            
            self._check_events()

            self._check_movimiento()

            self._check_colision()

            self._update_screen()

            self.clock.tick(self.velocidad)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not self.moving_down:
                    self.moving_up = True
                    self.moving_down = False
                    self.moving_left = False
                    self.moving_right = False
                elif event.key == pygame.K_DOWN and not self.moving_up:
                    self.moving_up = False
                    self.moving_down = True
                    self.moving_left = False
                    self.moving_right = False
                elif event.key == pygame.K_LEFT and not self.moving_right:
                    self.moving_up = False
                    self.moving_down = False
                    self.moving_left = True
                    self.moving_right = False
                elif event.key == pygame.K_RIGHT and not self.moving_left:
                    self.moving_up = False
                    self.moving_down = False
                    self.moving_left = False
                    self.moving_right = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def _check_movimiento(self):
        posicion_anterior = self.serpiente[0]
        if self.moving_up:
            self.serpiente[0] = self.serpiente[0].move(0.0, float(-self.size))
        elif self.moving_down:
            self.serpiente[0] = self.serpiente[0].move(0.0, float(self.size))
        elif self.moving_left:
            self.serpiente[0] = self.serpiente[0].move(float(-self.size), 0.0)
        elif self.moving_right:
            self.serpiente[0] = self.serpiente[0].move(float(self.size), 0.0)
        
        self._check_borde()

        for i in range(1, len(self.serpiente)):
            auxiliar = self.serpiente[i]
            self.serpiente[i] = posicion_anterior
            posicion_anterior = auxiliar

    def _check_borde(self):
        if self.serpiente[0].right > self.rect_pantalla.right:
            self.serpiente[0].update(self.rect_pantalla.left, self.serpiente[0].y, self.size, self.size)
        elif self.serpiente[0].left < self.rect_pantalla.left:
            self.serpiente[0].update(self.rect_pantalla.right, self.serpiente[0].y, self.size, self.size)
        elif self.serpiente[0].top < self.rect_pantalla.top+40:
            self.serpiente[0].update(self.serpiente[0].x, self.rect_pantalla.bottom, self.size, self.size)
        elif self.serpiente[0].bottom > self.rect_pantalla.bottom:
            self.serpiente[0].update(self.serpiente[0].x, self.rect_pantalla.top+40, self.size, self.size)

    def _check_colision(self):
        if self.serpiente[0].colliderect(self.manzana):
            self.manzanas.remove(self.manzana)
            self.score += 1
            self._check_upgrade()
            self._crear_manzana()
            self._add_snake()
        for i in range(1, len(self.serpiente)):
            if self.serpiente[0].colliderect(self.serpiente[i]):
                self._inicializar_juego()
                break

    def _inicializar_juego(self):
        self.serpiente.clear()
        self.score = 0
        self.velocidad = self.velocidad_inicial
        self.next_upgrade = self.upgrade_jump
        self._crear_serpiente()
        self._crear_manzana()

    def _check_upgrade(self):
        if self.score >= self.next_upgrade:
            self.velocidad += 1
            self.next_upgrade += self.upgrade_jump

    def _display_score(self, score):
        score_text = self.font.render("Manzanitas in my belly: " + str(score), True, "red")
        self.pantalla.blit(score_text, (10, 10))

    def _crear_serpiente(self):
        self.cabeza_serpiente = pygame.Rect(self.rect_pantalla.centerx, self.rect_pantalla.centery, self.size, self.size)
        self.cola_serpiente = pygame.Rect(self.rect_pantalla.centerx-self.size, self.rect_pantalla.centery, self.size, self.size)
        self.serpiente = [self.cabeza_serpiente, self.cola_serpiente]

    def _add_snake(self):
        pos_ultima_x = self.serpiente[len(self.serpiente)-1].x
        pos_ultima_y = self.serpiente[len(self.serpiente)-1].y
        new_snake =  pygame.Rect(pos_ultima_x, pos_ultima_y, self.size, self.size)
        self.serpiente.append(new_snake)

    def _crear_manzana(self):
        ale_pos_x = randrange(0, (self.alto_pantalla-self.size), self.size)
        ale_pos_y = randrange(self.score_board.height, (self.ancho_pantalla-self.size), self.size)
        self.manzana = pygame.Rect(ale_pos_x, ale_pos_y, self.size, self.size)
        self.manzanas = [self.manzana]

    def _update_screen(self):
        self.pantalla.fill("black")
        pygame.draw.rect(self.pantalla, "red", self.manzana)
        pygame.draw.rect(self.pantalla, "blue", self.score_board)
        self._display_score(self.score)
        for trozo in self.serpiente:
            pygame.draw.rect(self.pantalla, (58, 255, 00), trozo)
        pygame.display.flip()

if __name__ == "__main__":
    juego = Snek()
    juego.run_game()

pygame.quit()