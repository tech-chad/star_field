# Star Field
import random

import pygame

from typing import List
from typing import Tuple

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 800
COLOR_BLACK = (0, 0, 0)
COLOR_MODE = ["solid"]
COLOR_LIST = ["white", "red", "green", "blue", "cyan", "magenta",
              "yellow", "teal", "orange", "purple"]
MODES = ["solid_color", "cycle_color"]


class StarColor:
    def __init__(self):
        self.total_num_color_shades = 12
        self.color_dict = {"white": (255, 255, 255), "red": (255, 0, 0),
                           "green": (0, 255, 0), "blue": (0, 0, 255),
                           "cyan": (0, 255, 255), "magenta": (255, 0, 255),
                           "yellow": (255, 255, 0), "teal": (0, 255, 150),
                           "orange": (255, 128, 0), "purple": (190, 0, 255)}
        self.color = self.color_dict["white"]
        self.shade_list = []
        self.make_shades()

    def get_color(self, color_number: int) -> Tuple[int, int, int]:
        return self.shade_list[color_number]

    def set_color_name(self, name: str) -> None:
        self.color = self.color_dict[name]
        self.make_shades()

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
            color = (self.color[0]-(self.color[0] * i),
                     self.color[1]-(self.color[1] * i),
                     self.color[2]-(self.color[2] * i))
            self.shade_list.append(color)
            i += 0.075


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
    pygame.key.set_repeat()
    full_screen = False
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    number_list = [i for i in range(220, 39, -20)]
    num_of_stars = 5
    speed_number = 5
    direction_list = make_direction_list()
    star_colors = StarColor()
    clock = pygame.time.Clock()
    win.fill(color=COLOR_BLACK)
    pygame.display.update()
    color_number = 0
    shift_l = pygame.K_LSHIFT
    shift_r = pygame.K_RSHIFT
    color_mode = 0
    cycle_count = 2000
    cycle_color = 0

    stars = []
    for _ in range(10):
        s = Star(win, width, height, direction_list, star_colors)
        s.cycle(10)
        stars.append(s)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.WINDOWRESIZED:
                width, height = pygame.display.get_window_size()
                stars.clear()
                for _ in range(10):
                    s = Star(win, width, height, direction_list, star_colors)
                    s.cycle(10)
                    stars.append(s)
                continue
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    run = False
                elif keys[pygame.K_0] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 0
                elif keys[pygame.K_1] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 1
                elif keys[pygame.K_2] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 2
                elif keys[pygame.K_3] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 3
                elif keys[pygame.K_4] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 4
                elif keys[pygame.K_5] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 5
                elif keys[pygame.K_6] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 6
                elif keys[pygame.K_7] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 7
                elif keys[pygame.K_8] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 8
                elif keys[pygame.K_9] and (keys[shift_l] or keys[shift_r]):
                    num_of_stars = 9
                elif keys[pygame.K_0]:
                    speed_number = 0
                elif keys[pygame.K_1]:
                    speed_number = 1
                elif keys[pygame.K_2]:
                    speed_number = 2
                elif keys[pygame.K_3]:
                    speed_number = 3
                elif keys[pygame.K_4]:
                    speed_number = 4
                elif keys[pygame.K_5]:
                    speed_number = 5
                elif keys[pygame.K_6]:
                    speed_number = 6
                elif keys[pygame.K_7]:
                    speed_number = 7
                elif keys[pygame.K_8]:
                    speed_number = 8
                elif keys[pygame.K_9]:
                    speed_number = 9
                elif keys[pygame.K_f] and (keys[shift_l] or keys[shift_r]):
                    if full_screen:
                        stars.clear()
                        full_screen = False
                        pygame.quit()
                        pygame.init()
                        win = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT),
                                                      pygame.RESIZABLE)
                        width = DEFAULT_WIDTH
                        height = DEFAULT_HEIGHT
                        pygame.display.set_caption("Star Field")
                    else:
                        stars.clear()
                        full_screen = True
                        pygame.quit()
                        pygame.init()
                        win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        width, height = pygame.display.get_window_size()
                        pygame.display.set_caption("Star Field")
                    for _ in range(20):
                        s = Star(win, width, height, direction_list, star_colors)
                        s.cycle(10)
                        stars.append(s)
                    continue
                elif keys[pygame.K_n] and MODES[color_mode] == "solid_color":
                    if color_number < len(COLOR_LIST) - 1:
                        color_number += 1
                    else:
                        color_number = 0
                    star_colors.set_color_name(COLOR_LIST[color_number])
                elif keys[pygame.K_m]:
                    if color_mode < len(MODES) - 1:
                        color_mode += 1
                    else:
                        color_mode = 0
                    if MODES[color_mode] == "cycle_color":
                        star_colors.set_color_name(COLOR_LIST[cycle_color])
                    elif MODES[color_mode] == "solid_color":
                        star_colors.set_color_name(COLOR_LIST[color_number])
        if MODES[color_mode] == "cycle_color" and cycle_count <= 0:
            if cycle_color < len(COLOR_LIST) - 1:
                cycle_color += 1
            else:
                cycle_color = 0
            star_colors.set_color_name(COLOR_LIST[cycle_color])
            cycle_count = 2000
        elif MODES[color_mode] == "cycle_color":
            cycle_count -= 1
        win.fill(COLOR_BLACK)
        for star in stars:
            star.draw_star()
            if star.remove_star():
                stars.pop(stars.index(star))
        if len(stars) <= number_list[num_of_stars]:
            for _ in range(2):
                s = Star(win, width, height, direction_list, star_colors)
                stars.append(s)
        pygame.display.update()
        clock.tick(number_list[speed_number])


def main() -> None:
    pygame.init()
    win = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Star Field")
    star_field_loop(win)


if __name__ == "__main__":
    main()
