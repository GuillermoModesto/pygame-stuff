import pygame

class Camera:
    def __init__(self, player, screen_width, screen_height):
        self.player = player
        self.offset = pygame.math.Vector2(0,0)
        self.offset_float = pygame.math.Vector2(0,0)
        self.screen_width, self.screen_height = screen_width, screen_height
        self.CONST = pygame.math.Vector2(-self.screen_width / 2 + player.rect.x / 4, -player.rect.y) 

    def scroll(self, left_border, right_border, top_border, bottom_border):
        self.offset_float.x += (self.player.rect.x - self.offset_float.x + self.CONST.x)
        self.offset_float.y += (self.player.rect.y - self.offset_float.y + self.CONST.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)
        self.offset.x = max(left_border, self.offset.x)
        self.offset.x = min(self.offset.x, right_border - self.screen_width)
        self.offset.y = max(top_border, self.offset.y)
        self.offset.y = min(self.offset.y, bottom_border - self.screen_height)