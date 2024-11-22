import pygame

class Character():
    def __init__(self, game, ini_pos_x, ini_pos_y, width, height, size):

        self.size = size

        self.rect = pygame.Rect((ini_pos_x, ini_pos_y), (width, height))

        #for combat
        self.max_health = game.settings.ini_char_health
        self.health = self.max_health
        self.attack_strenght = game.settings.ini_char_attack
        self.attack = False
        self.attacking = False
        self.defense = game.settings.ini_char_deffense
        self.evation = game.settings.ini_char_evation
        self.crit_chance = game.settings.ini_char_crit_chance
        self.crit_damage = game.settings.ini_char_crit_damage

    #--------------------------------------------------SPRITESHEETS--------------------------------------------------#

    def load_images(self, sprite_sheet, steps):
        frames = []
        for i in range (steps):
            temp_image = sprite_sheet.subsurface(i * self.size, 0, self.size, self.size) #frame size for player is 128px,128px
            frames.append(pygame.transform.scale(temp_image, (self.size * 2.1, self.size * 2.1)))
        return frames
    
    #--------------------------------------------------COMBAT--------------------------------------------------#

    def control_stats(self):
        
        #health
        if self.health < 0:
            self.health = 0
        elif self.health > self.max_health:
            self.health = self.max_health

    #--------------------------------------------------DISPLAY--------------------------------------------------#

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)