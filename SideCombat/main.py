import pygame
from Character import Character
from Player import Player
from Settings import Settings

class main():
    def __init__(self):

        pygame.init()

        #game settings
        self.settings = Settings()

        #main window setup
        self.screen_width = self.settings.SCREEN_WIDTH
        self.screen_height = self.settings.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("2D Combat")

        #background (placeholder for now)
        self.bg_image = pygame.image.load("assets/origbig.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))

        #ground (maybe i should do a class for diferent types of obstacles)
        self.ground_level = self.settings.ground_level

        #character instancing
        self.player = Player(self)
        self.enemy = Character(self, self.settings.INI_PLAYER_POS_X+500, self.settings.INI_PLAYER_POS_Y, self.settings.PLAYER_WIDTH, self.settings.PLAYER_HEIGHT, 0)

        #FPS control
        self.FPS = self.settings.GAME_FPS
        self.clock = pygame.time.Clock()

        self.run = True

    #--------------------------------------------------MAIN GAME LOOP--------------------------------------------------#

    def run_game(self):
        while self.run:

            #FPS control
            dt = self.clock.tick(self.FPS) / self.FPS

            #event handler
            self._event_control()

            #player stuff
            self.player.control_movement(self.screen_width, self.settings.gravity, self.screen_height - self.settings.ground_level, dt)
            self.player.control_attack(self.enemy)
            self.player.control_throw(self.enemy, self.settings.gravity, self.screen_height - self.settings.ground_level)
            self.player.update_anim()

            #display control
            self._display()

    #--------------------------------------------------EVENTS--------------------------------------------------#
    
    def _event_control(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                self._keydown_event_control(event)

            if event.type == pygame.KEYUP:
                self._keyup_event_control(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    self.player.attack = True
                    self.player.attacking = True
                    self.player.update_action(3)

    def _keydown_event_control(self, event):

        #lateral movement
        if event.key == pygame.K_a:
            self.player.move_left = True
            self.player.flipped = True
            self.player.update_action(1)
        if event.key == pygame.K_d:
            self.player.move_right = True
            if self.player.flipped:
                self.player.flipped = False
            self.player.update_action(1)

        #jumping
        if event.key == pygame.K_SPACE and not self.player.on_air:
            self.player.jump = True
            self.player.update_action(2)

        #throw coin
        if event.key == pygame.K_f:
            #CHAGE THIS (add force to the throw instead of throwing)
            self.player.coin_onair = True
            self.player.coin_thrown = True

    def _keyup_event_control(self, event):

        #end lateral movement
        if event.key == pygame.K_a:
            self.player.move_left = False
            self.player.stoped = True
        if event.key == pygame.K_d:
            self.player.move_right = False
            self.player.stoped = True
        #CHAGE THIS (throw the coin when released with the calculated force above)

    #--------------------------------------------------DISPLAY--------------------------------------------------#
            
    def _display(self):

        #background placeholder
        self.screen.blit(self.bg_image, (0, 0))

        #player placeholder
        self.player.draw(self.screen)

        #coind placeholder
        pygame.draw.rect(self.screen, (0, 0, 255), self.player.coin)

        #enemy placeholder
        self.enemy.draw(self.screen)

        #DELETE (i just need it to see how the hitbox functions)
        pygame.draw.rect(self.screen, (0, 255, 0), self.player.atk_hb)

        pygame.display.update()



# ---> GAME CALL <---
        
if __name__ == "__main__":
    game = main()
    game.run_game()

pygame.quit()