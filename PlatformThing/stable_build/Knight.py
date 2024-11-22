import pygame
from debug import *

class Knight():
    def __init__(self, x, y, screen, world_rects):

        self.size = (14, 19)
        self.index = 0
        self.counter = 0

        self.screen = screen
        self.world_rects = world_rects

        self.idle_sheet = pygame.image.load(f"img/knight/knight_idle_sheet.png").convert_alpha()
        self.run_sheet = pygame.image.load(f"img/knight/knight_run_sheet.png").convert_alpha()

        aux = self.idle_sheet.subsurface(0, 0, self.size[0], self.size[1])
        self.image = pygame.transform.scale(aux, (self.size[0]*3.5, self.size[1]*3.5))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

        self.vel_x = 0
        self.vel_y = 0
        self.sprinting = False
        self.moving = False
        self.jumped = False
        self.flipped = False

    ######################################################################
    ############ MAIN UPDATE FUNCTION (to be called on main) #############
    ######################################################################

    def update(self, cam_offset_x, cam_offset_y, world_limit):
        key = pygame.key.get_pressed()

        # Animations
        if key[pygame.K_a] or key[pygame.K_d]: # Run animation
            self.animate(self.run_sheet, 16, 8) # sprite_sheet, steps(number of sprites), anim_cooldown
        else: # Idle animation
            self.animate(self.idle_sheet, 4, 10)
        
        # X movement
        self.move_x(key, .5, 7.5, 1, 1.7) # event key, increment,  maximun x velocity and sprint modifiers for increment and max_vel_x

        # Friction
        if self.jumped == False:
            self.friction(key, 1.3) # event key and value to subtract to current speed each tick

        # Y movement
        self.move_y(key, 20) # event key and initial jump strength
        
        # Gravity
        self.gravity(30, 1) # terminal velocity and value to subtract to current Y velocity each tick
        
        # Collision
        
        self.collision() 

        # Update position confining player to screen
        if self.rect.x + self.vel_x <= 0: #left side limit
            self.rect.x = 0
        elif self.rect.right + self.vel_x >= world_limit: #right side limit
            self.rect.right = world_limit
        else:
            self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        #pygame.draw.rect(self.screen, (0,0,0), self.rect, 2)
        self.screen.blit(self.image, (self.rect.x - cam_offset_x, self.rect.y - cam_offset_y))

    #############################################################
    ################# MOVEMENT AND "PHYSICS" ####################
    #############################################################

    def move_x(self, key, increment, max_vel_x, sprint_increment_modifier, sprint_maxX_modifier):
        if key[pygame.K_LSHIFT] or self.sprinting and self.jumped:
            self.sprinting = True
        else:
            self.sprinting = False

        if self.sprinting:
            max_vel_x *= sprint_maxX_modifier
            increment *= sprint_increment_modifier

        if key[pygame.K_a]:
            if self.vel_x <= -max_vel_x:
                self.vel_x = -max_vel_x
            else:
                self.vel_x -= increment
            self.flipped = True
        if key[pygame.K_d]:
            if self.vel_x >= max_vel_x:
                self.vel_x = max_vel_x
            else:
                self.vel_x += increment
            self.flipped = False
        
        debug(f"bool:{self.sprinting}, max:{max_vel_x}, increment:{increment}, actual{self.vel_x}")

    def friction(self, key, amount):
        if not key[pygame.K_a] and not key[pygame.K_d]:
            if self.vel_x < 0:
                self.vel_x += amount
            elif self.vel_x > 0:
                self.vel_x -= amount
            if self.vel_x < amount and self.vel_x > -amount:
                self.vel_x = 0

    def move_y(self, key, initial_value):
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -initial_value
            self.jumped = True

    def gravity(self, terminal_velocity, amount):
        if self.vel_y < terminal_velocity:
            self.vel_y += amount
        else:
            self.vel_y = terminal_velocity

    ################################################
    ################# COLLISION ####################
    ################################################

    def collision(self):
        #aux = pygame.Rect(self.rect.x + self.vel_x, self.rect.y + self.vel_y, self.width, self.height)
        #pygame.draw.rect(self.screen, (0,255,0), aux, 2)
        for tile in self.world_rects:
            # X collision
            if tile.colliderect(self.rect.x + self.vel_x, self.rect.y, self.width, self.height) or \
                tile.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                #self.vel_x = 0
                if self.vel_x >= 0:
                    self.vel_x = tile.left - self.rect.right
                elif self.vel_x < 0:
                    self.vel_x = tile.right - self.rect.left
            # Y collision
            elif tile.colliderect(self.rect.x, self.rect.y + self.vel_y, self.width, self.height) or \
                tile.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                #if y velocity is positive (greater that 0) im going down (falling)
                #pygame.draw.rect(self.screen, (0,255,0), tile, 2)
                if self.vel_y >= 0:
                    self.vel_y = tile.top - self.rect.bottom
                    self.jumped = False
                elif self.vel_y < 0:
                    self.vel_y = tile.bottom - self.rect.top
                
    ################################################
    ################# ANIMATION ####################
    ################################################

    """
     -> A counter ticks each frame to simulate a cooldown.
     -> When the counter reaches the target value (anim_cooldown), it resets.
     -> If sprite_sheet has that many steps in it, adds one to the animation index. 
     -> Take that index, multiply it by the size of the sprite and get a 'coocky cutter chunk' (subsurface) of previously mentioned sprite_sheet to give to the sprite. 
    """
    def animate(self, sprite_sheet, steps, anim_cooldown):
        self.counter += 1
        if self.counter > anim_cooldown:
            self.counter = 0
            if self.index < steps-1:
                self.index += 1
            else:
                self.index = 0
            aux = sprite_sheet.subsurface(self.index * self.size[0], 0, self.size[0], self.size[1])
            if self.flipped:
                aux = pygame.transform.flip(aux, True, False)
            self.image = pygame.transform.scale(aux, (self.size[0]*3.5, self.size[1]*3.5))