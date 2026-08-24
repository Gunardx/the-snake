from random import randint

import pygame

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """
    Общий класс для объектов игры.
    Задает расположение по умолчанию по центру экрана.
    """

    def __init__(self,
                 body_color: tuple | None = None,
                 position=BOARD_CENTER
                 ) -> None:
        self.body_color: tuple | None = body_color
        self.position: tuple = position

    def draw(self):
        """Метод для последующего переопределения дочерними классами."""
        pass


class Apple(GameObject):
    """
    Яблоко. Расположение определяется случайно
    с помощью метода randomize_position.
    """

    def __init__(self,
                 body_color: tuple = APPLE_COLOR,
                 position: tuple = BOARD_CENTER
                 ) -> None:
        super().__init__(body_color, position)
        self.body_color: tuple = body_color
        self.position: tuple = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Метод случайного определения координат яблока на игровом поле."""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (position_x, position_y)
        return self.position

    def draw(self) -> None:
        """Отрисовка модели яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Змейка. Тело змейки это атрибут self.positions.
    Начинает движение вправо. Метод move определяет следующее
    расположение головы исходя из направления движения
    и заменяет старый кортеж - новым.
    """

    def __init__(self,
                 body_color: tuple = SNAKE_COLOR,
                 position: tuple = BOARD_CENTER
                 ) -> None:
        super().__init__(body_color, position)
        self.length: int = 1
        self.positions: list[tuple] = [position]
        self.direction: tuple = RIGHT
        self.next_direction: tuple | None = None
        self.body_color: tuple = body_color
        self.last: tuple | None = None

    def get_head_position(self) -> tuple:
        """Метод возвращает координаты головы."""
        head_position = self.positions[0]
        return head_position

    def move(self) -> None:
        """
        Метод движения змейки. Если направление RIGHT,
        то новое значение кортежа next_head_position вычисляется на основе
        текущей позиции головы и размера клетки.
        И уже этот новый кортеж вставляется в начало списка позиций.
        Затем переменной self.last присваивается последний элемент списка
        self.positions и запускается проверка соответствия длины позиций
        к длине атрибута self.length. Дальнейшие ветки условия повторяют
        ту же логику для направлений LEFT, UP и DOWN.
        """
        current_head_position = self.get_head_position()
        if self.direction == RIGHT:
            next_head_position = (
                (current_head_position[0] + GRID_SIZE),
                current_head_position[1]
            )
            self.positions.insert(0, next_head_position)
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

        elif self.direction == LEFT:
            next_head_position = (
                (current_head_position[0] - GRID_SIZE),
                current_head_position[1]
            )
            self.positions.insert(0, next_head_position)
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

        elif self.direction == UP:
            next_head_position = (
                current_head_position[0],
                (current_head_position[1] - GRID_SIZE)
            )
            self.positions.insert(0, next_head_position)
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

        elif self.direction == DOWN:
            next_head_position = (
                current_head_position[0],
                (current_head_position[1] + GRID_SIZE)
            )
            self.positions.insert(0, next_head_position)
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

        # Выход за правую и левую границы
        if self.positions[0][0] > (SCREEN_WIDTH - GRID_SIZE):
            self.positions[0] = (0, self.positions[0][1])
        if self.positions[0][0] < 0:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE,
                                 self.positions[0][1])
        # Выход за верхнюю и нижнюю границы
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
        self.length = 1
        self.positions = [BOARD_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self) -> None:
        """Отрисовка модели змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake) -> None:
    """Функция обработки действий."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)

    # Основная логика
    running = True
    while running:
        clock.tick(SPEED)

        # Обработка действий
        handle_keys(snake)
        # Обновление направления движения змейки
        snake.update_direction()
        # Движение змейки, модификация списка координат
        snake.move()
        # Проверка поедания яблока змейкой
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = (apple.randomize_position())
        # Проверка столкновения головы змейки со своим телом
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Отрисовка
        snake.draw()
        apple.draw()
        # Обновление экрана
        pygame.display.update()
        # Ограничение частоты кадров
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
