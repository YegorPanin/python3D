import pygame
import pygame as pg
import numpy as np
from camera import camera
import sys
from controller import Controller

HEIGHT = 600
WIDTH = 800
BACKGROUND_COLOR = (0,0,0)
screen = pg.display.set_mode((WIDTH,HEIGHT))
FPS = 60
clock = pg.time.Clock()
cam = camera(screen)

def func(x, z):
    return np.sin(x) * np.cos(z)



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
    hum.rotate(0.001, 0.001)
    screen.fill(BACKGROUND_COLOR)

    cam.draw(hum,screen)

    Controller.listen_control(hum)
    pg.display.update()
    clock.tick(FPS)
