import pygame
from Character import Character
from random import randint
from math import atan2, cos, sin

class Player(Character):
    def __init__(self, game):

        self.settings = game.settings
        self.width = self.settings.PLAYER_WIDTH
        self.height = self.settings.PLAYER_HEIGHT

        #Spritesheets
        attack_sheet = pygame.image.load("assets/player_spritesheets/Attack_2.png").convert_alpha()
        dead_sheet = pygame.image.load("assets/player_spritesheets/Dead.png").convert_alpha()
        hurt_sheet = pygame.image.load("assets/player_spritesheets/Hurt.png").convert_alpha()
        iddle_sheet = pygame.image.load("assets/player_spritesheets/Idle.png").convert_alpha()
        jump_sheet = pygame.image.load("assets/player_spritesheets/Jump.png").convert_alpha()
        run_sheet = pygame.image.load("assets/player_spritesheets/Run.png").convert_alpha()
        attack_anim_steps, dead_anim_steps, hurt_anim_steps, iddle_anim_steps, jump_amin_steps, run_anim_steps = 3, 4, 2, 6, 12, 8
        
        super().__init__(game, self.settings.INI_PLAYER_POS_X, self.settings.INI_PLAYER_POS_Y, self.width, self.height, self.settings.PLAYER_SIZE)

        self.attack_anim = self.load_images(attack_sheet, attack_anim_steps)
        self.dead_anim = self.load_images(dead_sheet, dead_anim_steps)
        self.hurt_anim = self.load_images(hurt_sheet, hurt_anim_steps)
        self.iddle_anim = self.load_images(iddle_sheet, iddle_anim_steps)
        self.jump_anim = self.load_images(jump_sheet, jump_amin_steps)
        self.run_anim = self.load_images(run_sheet, run_anim_steps)

        self.action = 0 # 0:iddle | 1:run | 2:jump | 3:attack | 4:hurt | 5:dead
        self.frame_index = 0
        self.image = self.iddle_anim[self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.flipped = False

        #for movement
        self.speed = game.settings.player_speed
        self.vert_vel = 0 #vertical velocity

        self.move_right = False
        self.move_left = False
        self.last_dir = 0 # -1=left, 1=right
        self.hor_vel = 0 #horizontal velocity
        self.stoped = False

        self.jump = False
        self.on_air = False

        #coin stuff (thing player throws)
        self.coin = pygame.Rect((self.rect.centerx, self.rect.centery),(10,10))
        self.coin_thrown = False
        self.coin_onair = False
        self.throw_force = 0

        self.x = float(self.rect.x)

        #DELETE
        self.atk_hb = pygame.Rect((0,0),(50,50))

    #--------------------------------------------------ANIMATION--------------------------------------------------#

    def update_anim(self):
        anim_cooldown = 75

        if not self.move_left and not self.move_right and not self.on_air and not self.attacking:
            self.update_action(0)

        #iddle
        self._control_next_frame_time_direction(self.iddle_anim, anim_cooldown)

        #run
        if self.action == 1:
            self._control_next_frame_time_direction(self.run_anim, anim_cooldown)

        #jump
        elif self.action == 2:
            self._control_next_frame_time_direction(self.jump_anim, anim_cooldown)

        #attack
        elif self.action == 3:
            self._control_next_frame_time_direction(self.attack_anim, anim_cooldown)

    def _control_next_frame_time_direction(self, anim, cooldown):

        try:
            #check direction
            if self.flipped:
                self.image = pygame.transform.flip(anim[self.frame_index], True, False)
            else:
                self.image = anim[self.frame_index]
        except IndexError:
            self.frame_index = 0
            if self.action == 3:
                self.attacking = False

        #calculate time and update
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        #reset when necesary
        if self.frame_index >= len(anim):
            self.frame_index = 0
            #stop attacking
            if self.action == 3:
                self.attacking = False

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #--------------------------------------------------MOVEMENT--------------------------------------------------#

    def control_movement(self, game_screen_width, gravity, ground_level, dt):

        dx = self._control_horizontal_movement(gravity)
        dy = self._control_vertical_movement(gravity)

        #confine player to screen
        if self.rect.left + (dx/4) < 0:
            dx = -self.rect.left
        if self.rect.right + (dx/4) > game_screen_width:
            dx = game_screen_width - self.rect.right
        if self.rect.bottom + (dy/4) > ground_level:
            self.vert_vel = 0
            self.on_air = False
            dy = ground_level - self.rect.bottom

        #update position
        self.x += dx * dt
        self.rect.x = self.x
        self.rect.y += dy * dt

        #update coin position while not being thrown
        if not self.coin_thrown:
            self.coin.centerx = self.rect.centerx
            self.coin.centery = self.rect.centery

    #----------------------------------Horizontal movement----------------------------------#
    def _control_horizontal_movement(self, gravity):
        dx = 0

        #horizontal movement
        if self.move_left:
            dx = -self.speed
            self.last_dir = -1
        if self.move_right:
            dx = self.speed
            self.last_dir = 1

        #slide check
        if not self.move_left and not self.move_right:
            if self.stoped:
                self.hor_vel = self.speed * self.last_dir
                self.stoped = False
            self.hor_vel -= gravity * 1.2 * self.last_dir
            dx = self.hor_vel
            if (dx < 0 and self.last_dir == 1) or (dx > 0 and self.last_dir == -1):
                dx = 0

        return dx
    
    #----------------------------------Vertical movement----------------------------------#
    def _control_vertical_movement(self, gravity):
        dy = 0

        #vertical movement
        if self.jump:
            self.vert_vel = -70
            self.on_air = True
            self.jump = False

        #gravity check
        self.vert_vel += gravity
        dy = self.vert_vel

        return dy

    #--------------------------------------------------COMBAT--------------------------------------------------#

    def control_attack(self, enemy):
        
        if self.attack:
            attack_hitbox = self._create_attack_hitbox()
            
            #DELETE
            self.atk_hb = attack_hitbox

            #detect collision between hitbox and enemy, do necesary calculations, and apply damage
            if attack_hitbox.colliderect(enemy.rect):

                dmg = self._calculate_dagame_dealt(enemy)

                #check and apply damage
                if dmg > 0:
                    enemy.health -= dmg
                else:
                    enemy.health -= 1

                enemy.control_stats()
                
            self.attack = False

        #DELETE
        else:
            self.atk_hb = pygame.Rect((0,0),(50,50))

    def _create_attack_hitbox(self):
        #get mouse position to determine which side the attack hitbox is facing
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] < self.rect.y:
            attack_hitbox = pygame.Rect(self.rect.centerx - self.height, self.rect.y - self.width, self.height*2, self.width)
        else:
            if mouse_pos[0] > self.rect.centerx:
                attack_hitbox = pygame.Rect(self.rect.x + self.width, self.rect.y, self.width + self.width/3, self.height)
            else:
                attack_hitbox = pygame.Rect(self.rect.x - self.width - self.width/3, self.rect.y, self.width + self.width/3, self.height)

        return attack_hitbox
    
    def _calculate_dagame_dealt(self, enemy):
        dmg = self.attack_strenght
        if randint(1, 100) > enemy.evation: #check for enemy evasion
            if randint(1, 100) <= self.crit_chance: #check for critical hit
                dmg += dmg*self.crit_damage #apply critical damage if posible
            dmg -= enemy.defense #apply enemy defense
            
        return dmg

#--------------------------------------------------COIN STUFF--------------------------------------------------#

    def control_throw(self, enemy, gravity, ground_level):
        if self.coin_onair:
            self._throw_coin(gravity, ground_level)
        if self.coin.colliderect(enemy.rect):
            self.coin_onair = False

    def _throw_coin(self, gravity, ground_level):

        #initial values 
        if self.coin_thrown:
            self.throw_force = 50
            self.initial_player_x = self.rect.centerx
            self.initial_player_y = self.rect.centery
            #angle between player and cursor
            self.angle = atan2(pygame.mouse.get_pos()[1] - self.initial_player_y,
                               pygame.mouse.get_pos()[0] - self.initial_player_x)
            #create clock and give it an initial tick
            self.timer = pygame.time.Clock()
            self.time = self.timer.tick()
            self.coin_thrown = False

        #calculate time between first and actual tick in miliseconds
        self.timer.tick()

        #add previous elapsed time to total time
        self.time += self.timer.get_time() / 50

        if self.coin.bottom <= ground_level:
            #projectile motion equations
            self.coin.centerx = (self.initial_player_x + self.throw_force * cos(self.angle) * self.time)
            self.coin.centery = (self.initial_player_y + self.throw_force * sin(self.angle) * self.time + 0.5 * gravity * (self.time) ** 2)
        else: #no entra en esta rama y no se por qué
            self.coin_onair = False

#--------------------------------------------------DISPLAY--------------------------------------------------#

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(self.image, (self.rect.x - 105, self.rect.y - 120))