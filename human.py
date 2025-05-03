import math
from shapes import shape3D

class human_face(shape3D):
    """
    Класс для создания трехмерной, многополигональной (в виде каркаса)
    модели человеческого лица.

    Генерирует сетку вершин на основе сферических координат,
    деформированную для придания формы лица.
    """
    def __init__(self,
                 num_latitudes=15,  # Количество горизонтальных линий (широты)
                 num_longitudes=20, # Количество вертикальных линий (долготы)
                 head_radius_x=0.8, # Радиус головы по X (ширина)
                 head_radius_y=1.0, # Радиус головы по Y (высота)
                 head_radius_z=0.7, # Радиус головы по Z (глубина)
                 color=(200, 150, 120) # Телесный цвет по умолчанию
                ):
        """
        Инициализирует 3D модель лица.

        Args:
            num_latitudes (int): Уровень детализации по вертикали.
            num_longitudes (int): Уровень детализации по горизонтали.
            head_radius_x (float): Полуось эллипсоида головы по X.
            head_radius_y (float): Полуось эллипсоида головы по Y.
            head_radius_z (float): Полуось эллипсоида головы по Z.
            color (tuple): Цвет ребер в формате RGB (0-255).
        """
        if num_latitudes < 3 or num_longitudes < 4:
            raise ValueError("Недостаточное количество широт или долгот для создания сетки.")

        vertices = []
        edges = []
        vertex_map = {} # Словарь для хранения индекса вершины по (lat, lon)

        # Шаг 1: Генерация вершин на основе деформированной сферы/эллипсоида

        # Проходим по широтам (вертикальные углы, theta)
        # от 0 (верх) до pi (низ)
        for i in range(num_latitudes + 1):
            theta = math.pi * i / num_latitudes

            # Проходим по долготам (горизонтальные углы, phi)
            # от 0 до 2*pi (полный круг)
            # Мы идем до num_longitudes, так как последняя точка совпадает с первой
            for j in range(num_longitudes):
                phi = 2 * math.pi * j / num_longitudes

                # Базовые координаты на эллипсоиде
                base_x = head_radius_x * math.sin(theta) * math.cos(phi)
                base_y = head_radius_y * math.cos(theta) # Y - вертикальная ось
                base_z = head_radius_z * math.sin(theta) * math.sin(phi) # Z - глубина (вперед/назад)

                # --- Применение деформаций для придания формы лица ---
                # Это самая сложная часть, требующая "художественного" подхода
                # или сложных алгоритмов. Здесь приведена простая аппроксимация.

                x, y, z = base_x, base_y, base_z

                # Масштабирующий фактор для Z в зависимости от phi (делаем лицо более плоским спереди)
                # Передняя часть (phi около pi/2) должна иметь больший z
                z_scale = (math.sin(phi) + 1.1) / 2.1 # Увеличиваем z спереди
                # Небольшое сплющивание по бокам
                z_scale *= (1.0 - 0.3 * abs(math.cos(phi)))

                z *= z_scale

                # 1. Нос (выступ вперед в центре лицевой части)
                # Определяем область носа (примерно центр по высоте, спереди по долготе)
                if 0.35 * math.pi < theta < 0.65 * math.pi and abs(phi - math.pi / 2) < math.pi / 6:
                     # Добавляем выступ, максимальный в центре области носа
                     nose_factor = math.cos((theta - math.pi / 2) / (0.3 * math.pi) * math.pi/2) # По высоте
                     nose_factor *= math.cos((phi - math.pi / 2) / (math.pi / 6) * math.pi/2) # По ширине
                     z += 0.3 * head_radius_z * max(0, nose_factor) # Выступ носа

                # 2. Глазницы (небольшие впадины)
                # Левая глазница
                eye_left_theta, eye_left_phi = 0.4 * math.pi, 0.35 * math.pi
                dist_sq_left = ((theta - eye_left_theta)*2)**2 + (phi - eye_left_phi)**2
                if dist_sq_left < 0.1:
                    z -= 0.15 * head_radius_z * math.exp(-dist_sq_left * 20) # Впадина

                # Правая глазница (симметрично)
                eye_right_theta, eye_right_phi = 0.4 * math.pi, math.pi - 0.35 * math.pi
                dist_sq_right = ((theta - eye_right_theta)*2)**2 + (phi - eye_right_phi)**2
                if dist_sq_right < 0.1:
                    z -= 0.15 * head_radius_z * math.exp(-dist_sq_right * 20) # Впадина


                # 3. Рот/Подбородок (небольшие корректировки формы)
                # Слегка выдвигаем подбородок вперед
                if theta > 0.75 * math.pi and abs(phi - math.pi/2) < math.pi / 5:
                    chin_factor = (theta - 0.75 * math.pi) / (0.25 * math.pi)
                    z += 0.1 * head_radius_z * chin_factor


                # Добавляем вершину в список
                current_vertex_index = len(vertices)
                vertices.append((x, y, z))
                vertex_map[(i, j)] = current_vertex_index

        # Шаг 2: Генерация ребер для соединения вершин в сетку

        for i in range(num_latitudes):
            for j in range(num_longitudes):
                # Индексы текущей и соседних вершин
                current = vertex_map.get((i, j))
                right = vertex_map.get((i, (j + 1) % num_longitudes)) # Соседняя по долготе (с замыканием)
                down = vertex_map.get((i + 1, j))
                # down_right = vertex_map.get((i + 1, (j + 1) % num_longitudes)) # Для диагоналей/треугольников

                # Добавляем горизонтальные ребра (вдоль широт)
                if current is not None and right is not None:
                    edges.append((current, right))

                # Добавляем вертикальные ребра (вдоль долгот)
                # Пропускаем ребра на самом нижнем полюсе (они уже добавлены как горизонтальные для i=num_latitudes-1)
                if current is not None and down is not None:
                     edges.append((current, down))

                # Опционально: добавить диагональные ребра для триангуляции
                # if current is not None and down_right is not None:
                #    edges.append((current, down_right))
                # или
                # if right is not None and down is not None:
                #    edges.append((right, down))


        # Шаг 3: Инициализация базового класса shape3D
        super().__init__(vertices, edges, color=color)
        print(f"human_face created with {len(vertices)} vertices and {len(edges)} edges.")
        print(f"Parameters: latitudes={num_latitudes}, longitudes={num_longitudes}")

