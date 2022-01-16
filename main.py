import pygame
import sys
from random import randint

Background_color = (255, 255, 255)  # Цвет фона
Life_color = (0, 255, 0)  # Цвет клетки
Line_color = (0, 0, 0)  # Цвет линий
Line_width = 1  # Ширина линий


class Cell:
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.alive = alive
        self.neighbours = 0

    # Подсчет количества живых соседей
    def count_neighbours(self):
        count = 0
        # Ищем стартовую коодринату x
        if self.x > 0:
            start_x = self.x - 1
        else:
            start_x = 0
        for i in range(start_x, self.x + 1 + 1):  # Пробегаемся по x
            # Ищем стартовую коодринату y
            if self.y > 0:
                start_y = self.y - 1
            else:
                start_y = 0
            for j in range(start_y, self.y + 1 + 1):  # Пробегаемся по y
                if i == self.x and j == self.y:
                    continue
                # Проверяем выход за пределы
                if i >= CellsTable.x or j >= CellsTable.y:
                    continue
                # Считаем жиого соседа
                count += int(CellsTable.table[i][j].alive)
        self.neighbours = count
        return count

    # Проверяем выживаемость
    def dead(self):
        if self.neighbours > 3 or self.neighbours < 2:
            self.alive = False
        elif self.neighbours == 3:
            self.alive = True


class CellsTable:
    table = []
    x = 0
    y = 0

    def __init__(self, x, y):
        CellsTable.x = x
        CellsTable.y = y
        # Заполнение
        for i in range(x):
            cell_list = []
            for j in range(y):
                cell = Cell(i, j, randint(0, 1))
                cell_list.append(cell)
            CellsTable.table.append(cell_list)

    def recognize_dead(self):
        for row in CellsTable.table:
            for item in row:
                item.dead()

    def recalculate_neighbours(self):
        for row in CellsTable.table:
            for item in row:
                item.count_neighbours()


class Game:
    def __init__(self, width, height, cx, cy):
        self.width = width
        self.height = height
        self.x_width = int(width / cx)  # Ширина ячейки
        self.y_height = int(height / cy)  # Высота ячейки
        self.screen = pygame.display.set_mode([width, height])
        self.cells = CellsTable(cx, cy)

    # Показать жизнь на экране
    def show_life(self):
        # Рисуем линии сетки
        for i in range(self.cells.x + 1):
            pygame.draw.line(self.screen, Line_color, (0, i * self.y_height),
                             (self.cells.x * self.x_width, i * self.y_height),
                             Line_width)
            pygame.draw.line(self.screen, Line_color, (i * self.x_width, 0),
                             (i * self.x_width, self.cells.x * self.y_height),
                             Line_width)

        for row in self.cells.table:
            for item in row:
                x = item.x
                y = item.y
                if item.alive:
                    pygame.draw.rect(self.screen, Life_color,
                                     [x * self.x_width + (Line_width - 1),
                                      y * self.y_height + (Line_width - 1),
                                      self.x_width - Line_width, self.y_height - Line_width])


def main():
    pygame.display.set_caption("LifeGame")
    game = Game(500, 500, 20, 20)
    clock = pygame.time.Clock()
    while True:
        game.screen.fill(Background_color)
        clock.tick(1)  # Регулируем частоту кадров
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Проверяем выживаемость
        game.cells.recalculate_neighbours()
        game.cells.recognize_dead()
        game.show_life()
        pygame.display.flip()


if __name__ == "__main__":
    main()
