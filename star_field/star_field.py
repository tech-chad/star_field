# Star Field
import random

import pygame

from typing import List
from typing import Tuple

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 800
COLOR_BLACK = (0, 0, 0)


class StarColor:
    def __init__(self):
        self.total_num_color_shades = 12
        self.color_white = (255, 255, 255)
        self.shade_list = []
        self.make_shades()

    def get_color(self, color_number: int) -> Tuple[int, int, int]:
        return self.shade_list[color_number]

    def set_color_name(self, name: str) -> None:
        ...

    def set_color_rgb(self, red: int, green: int, blue: int) -> None:
        ...

    def set_default_color(self) -> None:
        ...

    def return_num_color_shades(self) -> int:
        return self.total_num_color_shades

    def make_shades(self) -> None:
        self.shade_list.clear()
        i = 0
        for _ in range(self.total_num_color_shades):
            color = (self.color_white[0]-(self.color_white[0] * i),
                     self.color_white[1]-(self.color_white[1] * i),
                     self.color_white[2]-(self.color_white[2] * i))
            self.shade_list.append(color)
            i += 0.05


class Star:
    def __init__(self, win: pygame.Surface,
                 screen_width: int,
                 screen_height: int,
                 direction_list: List[Tuple[int, int]],
                 star_color):
        self.win = win
        self.screen_width = screen_width
        self.screen_height = screen_height
        x_half = int(self.screen_width / 2)
        y_half = int(self.screen_height / 2)
        self.x = random.randint(x_half - 2, x_half + 2)
        self.y = random.randint(y_half - 2, y_half + 2)
        dx, dy = random.choice(direction_list)
        self.direction_x = dx
        self.direction_y = dy
        self.star_color = star_color
        self.color_number = random.randint(1, star_color.return_num_color_shades()) - 1
        self.size = random.randint(-3, -1)
        self.max_size = random.choice([1, 1, 1, 1, 2, 2])

    def draw_star(self) -> None:
        color = self.star_color.get_color(self.color_number)
        pygame.draw.circle(self.win, color, (self.x, self.y), self.size)
        self.x += self.direction_x
        self.y += self.direction_y
        if self.size <= self.max_size:
            self.size += 0.07

    def cycle(self, count: int) -> None:
        for _ in range(count):
            self.x += self.direction_x
            self.y += self.direction_y
            if self.size <= self.max_size:
                self.size += 0.05

    def remove_star(self) -> bool:
        if self.x <= -30 or self.x >= self.screen_width + 30:
            return True
        elif self.y <= -30 or self.y >= self.screen_height + 30:
            return True
        else:
            return False


def make_direction_list():
    a = [i for i in range(-6, 7, 1)]
    path_list = []
    for x in a:
        for y in a:
            if x == 0 and y == 0:
                continue
            elif x == y or abs(x) == abs(y):
                path_list.append((x, y))
            elif x == 0 or y == 0:
                path_list.append((x, y))
            else:
                path_list.append((x, y))
                path_list.append((x, y))
                path_list.append((x, y))
                path_list.append((x, y))
                path_list.append((x, y))
                path_list.append((x, y))
    return path_list


def star_field_loop(win: pygame.Surface) -> None:
    direction_list = make_direction_list()
    star_colors = StarColor()
    clock = pygame.time.Clock()
    win.fill(color=COLOR_BLACK)
    pygame.display.update()

    stars = []
    for _ in range(30):
        s = Star(win, DEFAULT_WIDTH, DEFAULT_HEIGHT, direction_list, star_colors)
        s.cycle(10)
        stars.append(s)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill(COLOR_BLACK)
        clock.tick(100)
        for star in stars:
            star.draw_star()
            if star.remove_star():
                stars.pop(stars.index(star))
        if len(stars) <= 100:
            for _ in range(20):
                s = Star(win, DEFAULT_WIDTH, DEFAULT_HEIGHT, direction_list, star_colors)
                stars.append(s)
        pygame.display.update()


def main() -> None:
    pygame.init()
    win = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
    pygame.display.set_caption("Star Field")
    star_field_loop(win)


if __name__ == "__main__":
    main()
