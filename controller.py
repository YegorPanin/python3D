import pygame
import numpy as np
from camera import Camera
import shapes  # Предполагается, что у вас есть модуль shapes с классом shape3D


class Controller:
    @staticmethod
    def listen_control(entity):
        """
        Обрабатывает пользовательский ввод для управления объектами (камера или shape3D).
        """
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()  # Относительное движение мыши
        dx, dy = mouse_rel
        sensitivity = 0.005  # Чувствительность мыши
        speed = 2.0          # Скорость движения
        rotate_speed = 0.05  # Скорость поворота

        # Управление камерой
        if isinstance(entity, Camera):
            move_dir = np.array([0.0, 0.0, 0.0])

            # Вертикальное движение (вверх / вниз)
            if keys[pygame.K_SPACE]:
                move_dir[1] += speed
            if keys[pygame.K_LSHIFT]:
                move_dir[1] -= speed

            # Боковое движение (влево / вправо)
            if keys[pygame.K_a]:
                move_dir[0] -= speed
            if keys[pygame.K_d]:
                move_dir[0] += speed

            # Горизонтальное движение вперёд / назад с учётом направления взгляда
            if keys[pygame.K_w] or keys[pygame.K_s]:
                yaw = entity.yaw
                forward_x = np.sin(yaw)
                forward_z = np.cos(yaw)

                if keys[pygame.K_w]:
                    move_dir[0] += forward_x * speed
                    move_dir[2] += forward_z * speed
                if keys[pygame.K_s]:
                    move_dir[0] -= forward_x * speed
                    move_dir[2] -= forward_z * speed

            # Применение движения
            entity.move(*move_dir)

            # Поворот камеры с помощью мыши
            if dx != 0 or dy != 0:
                # ИСПРАВЛЕНИЕ: изменили знак dx для правильного направления поворота
                dyaw = -dx * sensitivity
                dpitch = dy * sensitivity
                entity.rotate(dyaw, dpitch)

            # Альтернативный поворот клавишами
            if keys[pygame.K_UP]:
                entity.rotate(0, -rotate_speed)
            if keys[pygame.K_DOWN]:
                entity.rotate(0, rotate_speed)
            if keys[pygame.K_LEFT]:
                # ИСПРАВЛЕНИЕ: теперь LEFT уменьшает yaw (поворот влево)
                entity.rotate(-rotate_speed, 0)
            if keys[pygame.K_RIGHT]:
                # ИСПРАВЛЕНИЕ: теперь RIGHT увеличивает yaw (поворот вправо)
                entity.rotate(rotate_speed, 0)

        # Управление 3D-объектами (shape3D)
        elif hasattr(entity, 'move') and hasattr(entity, 'rotate') and hasattr(entity, 'scale'):
            # Перемещение
            if keys[pygame.K_w]:
                entity.move(0, speed, 0)
            if keys[pygame.K_s]:
                entity.move(0, -speed, 0)
            if keys[pygame.K_a]:
                entity.move(-speed, 0, 0)
            if keys[pygame.K_d]:
                entity.move(speed, 0, 0)

            # Поворот
            if keys[pygame.K_UP]:
                entity.rotate(rotate_speed, 0, 0)
            if keys[pygame.K_DOWN]:
                entity.rotate(-rotate_speed, 0, 0)
            if keys[pygame.K_LEFT]:
                entity.rotate(0, rotate_speed, 0)
            if keys[pygame.K_RIGHT]:
                entity.rotate(0, -rotate_speed, 0)

            # Масштабирование
            if keys[pygame.K_PAGEUP]:
                entity.scale(1.1)
            if keys[pygame.K_PAGEDOWN]:
                entity.scale(0.9)

        else:
            print(f"[Controller] Неизвестный тип объекта: {type(entity)}")