import pygame
from numpy.ma.core import angle

import shapes
from camera import camera


class Controller:
    @staticmethod
    def listen_control(entity: shapes.shape3D):
        speed = 2
        angle = 0.1
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            entity.move(0,speed,0)
        if keys[pygame.K_a]:
            entity.move(-speed,0,0)
        if keys[pygame.K_s]:
            entity.move(0,-speed,0)
        if keys[pygame.K_d]:
            entity.move(speed,0,0)

        if keys[pygame.K_UP]:
            entity.rotate(angle, 0, 0)
        if keys[pygame.K_DOWN]:
            entity.rotate(-angle, 0, 0)
        if keys[pygame.K_LEFT]:
            entity.rotate(0, angle, 0)
        if keys[pygame.K_RIGHT]:
            entity.rotate(0, -angle, 0)


        if keys[pygame.K_PAGEUP]:
            entity.scale(1.1)
        if keys[pygame.K_PAGEDOWN]:
            entity.scale(0.9)

        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0]:
            pos = pygame.mouse.get_pos()
            camera.get_ray(pos)

