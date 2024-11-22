class Settings():
    def __init__(self):

        #constants
        self.GAME_FPS = 60
        self.gravity = 4
        
        #screen
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 500

        #ground
        self.ground_level = self.SCREEN_HEIGHT*9/60

        #player
        #size
        self.PLAYER_SIZE = 128
        self.PLAYER_WIDTH = 70
        self.PLAYER_HEIGHT = 145
        
        #initial position
        self.INI_PLAYER_POS_X = 200
        self.INI_PLAYER_POS_Y = self.SCREEN_HEIGHT - self.ground_level - self.PLAYER_HEIGHT

        #speed
        self.player_speed = 35

        #combat
        self.ini_char_health = 100
        self.ini_char_attack = 25
        self.ini_char_deffense = 5
        self.ini_char_evation = 5
        self.ini_char_crit_chance = 5
        self.ini_char_crit_damage = 8/10