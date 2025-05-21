import pygame
from camera import Camera
import shapes


class Controller:
    @staticmethod
    def listen_control(entity):
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()  # Получаем относительное движение мыши
        dx, dy = mouse_rel
        sensitivity = 0.005  # Чувствительность мыши

        speed = 2
        angle = 0.05  # Угол вращения клавишами

        # Управление камерой
        if isinstance(entity, Camera):
            # Перемещение камеры клавишами
            move_dir = [0, 0, 0]
            if keys[pygame.K_w]:
                move_dir[2] = -speed
            if keys[pygame.K_s]:
                move_dir[2] = speed
            if keys[pygame.K_a]:
                move_dir[0] = -speed
            if keys[pygame.K_d]:
                move_dir[0] = speed
            if keys[pygame.K_SPACE]:
                move_dir[1] = -speed
            if keys[pygame.K_LSHIFT]:
                move_dir[1] = speed

            entity.move(*move_dir)

            # Поворот камеры с помощью мыши
            if dx != 0 or dy != 0:
                dyaw = -dx * sensitivity
                dpitch = -dy * sensitivity
                entity.rotate(dyaw, dpitch)

            # Альтернативно: поворот с клавиатуры
            if keys[pygame.K_UP]:
                entity.rotate(dyaw=0, dpitch=-angle)
            if keys[pygame.K_DOWN]:
                entity.rotate(dyaw=0, dpitch=angle)
            if keys[pygame.K_LEFT]:
                entity.rotate(dyaw=angle, dpitch=0)
            if keys[pygame.K_RIGHT]:
                entity.rotate(dyaw=-angle, dpitch=0)

        # Управление 3D-фигурами
        elif isinstance(entity, shapes.shape3D):
            if keys[pygame.K_w]:
                entity.move(0, speed, 0)
            if keys[pygame.K_s]:
                entity.move(0, -speed, 0)
            if keys[pygame.K_a]:
                entity.move(-speed, 0, 0)
            if keys[pygame.K_d]:
                entity.move(speed, 0, 0)

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

        else:
            print(f"Unsupported entity type: {type(entity)}")