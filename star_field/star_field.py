# Star Field
import random

import pygame

from typing import List
from typing import Tuple

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 800
COLOR_BLACK = (0, 0, 0)
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

    def num_color_shades(self) -> int:
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
    def __init__(self,
                 screen_width: int,
                 screen_height: int,
                 direction_list: List[Tuple[int, int]],
                 star_color):
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
        self.color_number = random.randint(1, star_color.num_color_shades()) - 1
        self.size = random.randint(-3, -1)
        self.max_size = random.choice([1, 1, 1, 1, 2, 2])

    def draw_star(self) -> None:
        win = pygame.display.get_surface()
        color = self.star_color.get_color(self.color_number)
        pygame.draw.circle(win, color, (self.x, self.y), self.size)
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
                for _ in range(6):
                    path_list.append((x, y))
    return path_list


def get_key_pressed() -> str:
    keys = pygame.key.get_pressed()
    look_for = {pygame.K_q: "q", pygame.K_m: "m", pygame.K_0: "0",
                pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
                pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6",
                pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9",
                pygame.K_p: "p", pygame.K_n: "n", pygame.K_f: "f"}
    for k in look_for.keys():
        if keys[k] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            return f"S {look_for[k]}"
        elif keys[k]:
            return look_for[k]
    else:
        return ""


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
    color_mode = 0
    cycle_count = 2000
    cycle_color = 0
    pause = False

    stars = []
    for _ in range(10):
        s = Star(width, height, direction_list, star_colors)
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
                    s = Star(width, height, direction_list, star_colors)
                    s.cycle(10)
                    stars.append(s)
                continue
            elif event.type == pygame.KEYDOWN:
                key_pressed = get_key_pressed()
                if key_pressed in ["q" or "S q"]:
                    run = False
                elif key_pressed == "p":
                    pause = not pause
                elif pause:
                    continue
                elif key_pressed in ["S 0", "S 1", "S 2", "S 3", "S 4", "S 5",
                                     "S 6", "S 7", "S 8", "S 9"]:
                    num_of_stars = int(key_pressed[-1])
                elif key_pressed in ["0", "1", "2", "3", "4", "5", "6",
                                     "7", "8", "9"]:
                    speed_number = int(key_pressed)
                elif key_pressed == "S f":
                    if full_screen:
                        stars.clear()
                        full_screen = False
                        pygame.quit()
                        pygame.init()
                        win = pygame.display.set_mode((DEFAULT_WIDTH,
                                                       DEFAULT_HEIGHT),
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
                        s = Star(width, height, direction_list, star_colors)
                        s.cycle(10)
                        stars.append(s)
                    continue
                elif key_pressed == "n" and MODES[color_mode] == "solid_color":
                    if color_number < len(COLOR_LIST) - 1:
                        color_number += 1
                    else:
                        color_number = 0
                    star_colors.set_color_name(COLOR_LIST[color_number])
                elif key_pressed == "m":
                    if color_mode < len(MODES) - 1:
                        color_mode += 1
                    else:
                        color_mode = 0
                    if MODES[color_mode] == "cycle_color":
                        star_colors.set_color_name(COLOR_LIST[cycle_color])
                    elif MODES[color_mode] == "solid_color":
                        star_colors.set_color_name(COLOR_LIST[color_number])

        if MODES[color_mode] == "cycle_color" and cycle_count <= 0 and not pause:
            if cycle_color < len(COLOR_LIST) - 1:
                cycle_color += 1
            else:
                cycle_color = 0
            star_colors.set_color_name(COLOR_LIST[cycle_color])
            cycle_count = 2000
        elif MODES[color_mode] == "cycle_color" and not pause:
            cycle_count -= 1
        if not pause:
            win.fill(COLOR_BLACK)
            for star in stars:
                star.draw_star()
                if star.remove_star():
                    stars.pop(stars.index(star))
            pygame.display.flip()
        if len(stars) <= number_list[num_of_stars]:
            for _ in range(2):
                s = Star(width, height, direction_list, star_colors)
                stars.append(s)

        clock.tick(number_list[speed_number])


def main() -> None:
    pygame.init()
    win = pygame.display.set_mode(
        (DEFAULT_WIDTH, DEFAULT_HEIGHT),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("Star Field")
    star_field_loop(win)


if __name__ == "__main__":
    main()
