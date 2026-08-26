from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """
    Общий класс для объектов игры.

    Задает расположение по умолчанию по центру экрана.
    """

    def __init__(self,
                 body_color: tuple
                 ) -> None:
        self.body_color: tuple = body_color

    def draw(self):
        """Метод для последующего переопределения дочерними классами."""
        raise NotImplementedError(
            f'Метод draw() не реализован в классе {type(self).__name__}')


class Apple(GameObject):
    """
    Яблоко.

    Расположение определяется случайно
    c помощью метода randomize_position.
    """

    def __init__(self,
                 body_color: tuple = APPLE_COLOR,
                 occupied_positions: list | None = None
                 ) -> None:
        super().__init__(body_color)
        self.body_color: tuple = body_color
        self.occupied_positions = occupied_positions or []
        self.randomize_position()

    def randomize_position(self) -> None:
        """Метод случайного определения координат яблока на игровом поле."""
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                        )
            if position not in self.occupied_positions:
                self.position = position
                break

    def draw(self) -> None:
        """Отрисовка модели яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Змейка.

    Тело змейки это атрибут self.positions.
    Начинает движение вправо. Метод move определяет следующее
    расположение головы исходя из направления движения
    и заменяет старый кортеж - новым.
    """

    def __init__(self,
                 body_color: tuple = SNAKE_COLOR,
                 ) -> None:
        super().__init__(body_color)
        self.reset()

    def get_head_position(self) -> tuple[int, int]:
        """Метод возвращает координаты головы."""
        return self.positions[0]

    def insert_head(self, next_head_position: tuple[int, int]) -> None:
        """
        Метод вставляет новую позицию головы змейки в
        начало списка self.positions, затем сохраняет координаты
        хвоста и проводит проверку длинны
        """
        self.positions.insert(0, next_head_position)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def move(self) -> None:
        """
        Метод движения змейки. Текущая позиция головы и направление
        распаковываются. Новая координата x вычисляется путем
        умножения направления на размер клетки и прибавления к
        текущей позиции головы.
        Затем вызывается метод формирования новой головы self.insert_head.
        Далее проверки выхода змейки за пределы поля.
        """
        head_x, head_y = self.get_head_position()
        d_x, d_y = self.direction
        new_x = head_x + d_x * GRID_SIZE
        new_y = head_y + d_y * GRID_SIZE
        new_position = (new_x, new_y)
        self.insert_head(new_position)
        # Выход за пределы границ
        if self.positions[0][0] > (SCREEN_WIDTH - GRID_SIZE):
            self.positions[0] = (0, self.positions[0][1])
        if self.positions[0][0] < 0:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE,
                                 self.positions[0][1])
        if self.positions[0][1] > (SCREEN_HEIGHT - GRID_SIZE):
            self.positions[0] = (self.positions[0][0], 0)
        if self.positions[0][1] < 0:
            self.positions[0] = (self.positions[0][0],
                                 SCREEN_HEIGHT - GRID_SIZE)

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Метод сбрасывает позицию и размер змейки"""
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [BOARD_CENTER]
        self.direction: tuple[int, int] = RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.last: tuple[int, int] | None = None

    def draw(self) -> None:
        """Отрисовка модели змейки."""
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            
        # Отрисовка головы
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def handle_keys(game_object: Snake) -> None:
    """Функция обработки действий."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция."""
    # Инициализация PyGame:
    pg.init()

    # Создание экземпляров классов
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)

    # Основная логика
    running = True
    while running:
        # Обработка действий
        handle_keys(snake)
        # Обновление направления движения змейки
        snake.update_direction()
        # Движение змейки, модификация списка координат
        snake.move()
        # Поддержка актуальных позиций змейки для яблока
        apple.occupied_positions = snake.positions.copy()
        # Проверка поедания яблока змейкой
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Проверка столкновения головы змейки со своим телом
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Отрисовка
        snake.draw()
        apple.draw()
        # Обновление экрана
        pg.display.update()
        # Ограничение частоты кадров
        clock.tick(SPEED)

    pg.quit()


if __name__ == '__main__':
    main()
