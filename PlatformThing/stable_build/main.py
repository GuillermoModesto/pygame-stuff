import pygame
from World import World
from Knight import Knight
from Camera import *
# PERFORMANCE STUFF -----------------
from debug import *
from psutil import Process, cpu_percent
from os import getpid
# PERFORMANCE STUFF -----------------

pygame.init()

screen = pygame.display.set_mode((900, 700)) #screen_width, screen_height
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()
dt = clock.tick(60)/1000

# PERFORMANCE STUFF -----------------
"""
Frame Rate: Aim for 60 FPS, acceptable above 30 FPS.
CPU Usage: Target below 50%, acceptable in the 20-40% range.
Memory Usage: Target below 500 MB, typical range 100-300 MB.
"""
cpu_usage = cpu_percent(interval=None)
max_cpu_usage = cpu_usage
cpu_update_interval = 1
cpu_update_accumulator = 0.
# PERFORMANCE STUFF -----------------

tile_size = 50
world = World(tile_size, screen) # tile size and main screen
world_limit_x = len(world.data[0]) * tile_size
world_limit_y = len(world.data) * tile_size
#150, screen.get_height() - 300, screen, world.rects
player = Knight(450, screen.get_height() - 230, screen, world.rects) 
camera = Camera(player, screen.get_width(), screen.get_height())

run = True
while run:

    world.display(camera.offset.x, camera.offset.y)
    player.update(camera.offset.x, camera.offset.y, world_limit_x)
    camera.scroll(0, world_limit_x, 0, world_limit_y)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                player.sprinting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                player.sprinting = False"""

    dt = clock.tick(60)/1000
    # PERFORMANCE STUFF -----------------
    debug(f"FPS:{clock.get_fps():.2f}", x=810) #FPS
    debug(f"Memory usage:{Process(getpid()).memory_info().rss / 1024 ** 2:.2f} MB", y=29, x=693) #MEMORY
    # Accumulate elapsed time for CPU usage update
    cpu_update_accumulator += dt
    if cpu_update_accumulator >= cpu_update_interval:
        cpu_usage = cpu_percent(interval=None)
        cpu_update_accumulator -= cpu_update_interval
    if cpu_usage > max_cpu_usage:
        max_cpu_usage = cpu_usage
    debug(f"CPU usage:{cpu_usage}%", y=50, x=682)
    debug(f" MAX:{max_cpu_usage}%", y=51, x=812)
    # PERFORMANCE STUFF -----------------
    pygame.display.update()

pygame.quit()