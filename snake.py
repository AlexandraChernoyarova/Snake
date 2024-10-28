import random
import pygame

# Размеры игрового поля
FIELD_WIDTH = 640
FIELD_HEIGHT = 480

# Размер ячейки
CELL_SIZE = 20

# Количество ячеек по горизонтали и вертикали
HORIZONTAL_CELLS = FIELD_WIDTH // CELL_SIZE
VERTICAL_CELLS = FIELD_HEIGHT // CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс для игрового объекта
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, x, y):
        """
        Инициализация объекта.

        Args:
            x (int): Координата x.
            y (int): Координата y.
        """
        self.x = x
        self.y = y

    def draw(self, screen):
        raise NotImplementedError("Метод draw() должен быть переопределен в подклассах.")


# Класс для яблока
class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, x, y):
        """
        Инициализация яблока.

        Args:
            x (int): Координата x.
            y (int): Координата y.
        """
        super().__init__(x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Класс для змейки
class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = "right"
        self.body = [(x, y)]
        self.growing = False

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.body[0]

        if self.direction == "right":
            head_x += 1
        elif self.direction == "left":
            head_x -= 1
        elif self.direction == "up":
            head_y -= 1
        elif self.direction == "down":
            head_y += 1

        # Проверка на столкновение с границей
        if head_x < 0:
            head_x = HORIZONTAL_CELLS - 1
        elif head_x >= HORIZONTAL_CELLS:
            head_x = 0
        if head_y < 0:
            head_y = VERTICAL_CELLS - 1
        elif head_y >= VERTICAL_CELLS:
            head_y = 0

        # Добавление новой головы
        self.body.insert(0, (head_x, head_y))

        # Удаление хвоста, если змейка не растет
        if not self.growing:
            self.body.pop()

        self.growing = False

    def change_direction(self, new_direction):
        """Изменение направления движения змейки."""
        if new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction
        elif new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction

    def grow(self):
        """Увеличение длины змейки на один сегмент."""
        self.growing = True

    def check_collision(self):
        """Проверка на столкновение змейки с самой собой."""
        head_x, head_y = self.body[0]
        for i in range(1, len(self.body)):
            x, y = self.body[i]
            if head_x == x and head_y == y:
                return True
        return False

    def draw(self, screen):
        for x, y in self.body:
            pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def main():
    """Основной цикл игры."""

    # Инициализация Pygame
    pygame.init()

    # Создание окна
    screen = pygame.display.set_mode((FIELD_WIDTH, FIELD_HEIGHT))

    # Название окна
    pygame.display.set_caption("Змейка")

    # Создание змейки и яблока
    snake = Snake(HORIZONTAL_CELLS // 2, VERTICAL_CELLS // 2)
    apple = Apple(random.randint(0, HORIZONTAL_CELLS - 1), random.randint(0, VERTICAL_CELLS - 1))

    # Основной цикл игры
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("up")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("right")

        # Движение змейки
        snake.move()

        # Проверка на столкновение змейки с яблоком
        if snake.body[0] == (apple.x, apple.y):
            snake.grow()
            apple.x = random.randint(0, HORIZONTAL_CELLS - 1)
            apple.y = random.randint(0, VERTICAL_CELLS - 1)

        # Проверка на столкновение змейки с самой собой
        if snake.check_collision():
            running = False

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

        # Задержка
        pygame.time.delay(100)

    # Выход из Pygame
    pygame.quit()

# Запуск игры
if __name__ == "__main__":
    main()
