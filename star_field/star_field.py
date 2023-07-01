# Star Field
import argparse
import random

import pygame

from typing import List
from typing import Tuple

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 800
DEFAULT_SPEED = 5
DEFAULT_STARS = 5
COLOR_BLACK = (0, 0, 0)
COLOR_LIST = ["white", "red", "green", "blue", "cyan", "magenta",
              "yellow", "teal", "orange", "purple"]
BG_COLOR_NAMES = [
    "black", "red", "green", "blue", "cyan", "yellow", "magenta",
    "teal", "orange", "purple", "white", "gray",
]
BG_COLOR_DICT = {
    "white": (200, 200, 200), "red": (128, 0, 0), "green": (0, 128, 0),
    "blue": (0, 0, 128), "cyan": (0, 128, 128), "magenta": (128, 0, 128),
    "yellow": (128, 128, 0), "teal": (0, 140, 100), "orange": (128, 64, 0),
    "purple": (95, 0, 128), "black": (0, 0, 0), "gray": (90, 90, 90),
}
MODES = ["solid_color", "cycle_color"]


class StarColor:
    def __init__(self):
        self.total_num_color_shades = 8
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
        for _ in range(self.total_num_color_shades + 1):
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
                 star_color,
                 center_adjust_x: int,
                 center_adjust_y: int,
                 reverse: bool):
        self.reverse = reverse
        self.star_color = star_color
        self.color_number = random.randint(1, star_color.num_color_shades())
        self.screen_width = screen_width
        self.screen_height = screen_height
        if self.reverse:
            self.center_x = int(self.screen_width / 2) + center_adjust_x
            self.center_y = int(self.screen_height / 2) + center_adjust_y
            loc_list = self.make_location_list()
            self.x, self.y = random.choice(loc_list)
            speed = random.randint(110, 190)
            dx = (self.center_x - self.x) / speed
            dy = (self.center_y - self.y) / speed
            self.direction_x = dx
            self.direction_y = dy
            self.size = random.choice([1, 1, 1, 1.5, 2, 2, 2.5])
        else:
            self.x = int(self.screen_width / 2) + center_adjust_x
            self.y = int(self.screen_height / 2) + center_adjust_y
            dx, dy = random.choice(direction_list)
            self.direction_x = dx
            self.direction_y = dy
            self.size = random.randint(-3, -1)
            self.max_size = random.choice([1, 1, 1, 1, 2, 2])

    def draw_star(self) -> None:
        win = pygame.display.get_surface()
        color = self.star_color.get_color(self.color_number)
        pygame.draw.circle(win, color, (self.x, self.y), self.size)
        self.x += self.direction_x
        self.y += self.direction_y
        if self.reverse:
            self.size -= 0.007
        else:
            if self.size <= self.max_size:
                self.size += 0.07

    def cycle(self, count: int) -> None:
        if self.reverse:
            count += 10
        for _ in range(count):
            self.x += self.direction_x
            self.y += self.direction_y
            if self.reverse:
                self.size -= 0.07
            else:
                if self.size <= self.max_size:
                    self.size += 0.07

    def remove_star(self) -> bool:
        if self.reverse:
            if self.center_x - 5 <= self.x <= self.center_x + 5 and \
                    self.center_y - 5 <= self.y <= self.center_y + 5:
                return True
        else:
            if self.x <= -2 or self.x >= self.screen_width + 2:
                return True
            elif self.y <= -2 or self.y >= self.screen_height + 2:
                return True
            else:
                return False

    def make_location_list(self) -> List[Tuple[int, int]]:
        # for reverse mode
        loc_list = []
        for x in range(-5, self.screen_width + 5):
            loc_list.append((x, -5))
            loc_list.append((x, self.screen_height + 5))
        for y in range(-5, self.screen_height + 5):
            loc_list.append((self.screen_width + 5, y))
            loc_list.append((-5, y))
        return loc_list


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
                pygame.K_p: "p", pygame.K_n: "n", pygame.K_f: "f",
                pygame.K_d: "d", pygame.K_DOWN: "down",
                pygame.K_UP: "up", pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right", pygame.K_r: "r", pygame.K_b: "b"}
    for k in look_for.keys():
        if keys[k] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            return f"S {look_for[k]}"
        elif keys[k]:
            return look_for[k]
    else:
        return ""


def star_field_loop(win: pygame.Surface, args: argparse.Namespace) -> None:
    pygame.key.set_repeat()
    width, height = pygame.display.get_window_size()

    # if args.full_screen:
    #     width, height = pygame.display.get_window_size()
    # else:
    #     width = DEFAULT_WIDTH
    #     height = DEFAULT_HEIGHT
    number_list = [i for i in range(220, 39, -20)]
    num_of_stars = DEFAULT_STARS
    speed_number = DEFAULT_SPEED
    direction_list = make_direction_list()
    star_colors = StarColor()
    star_colors.set_color_name(args.color)
    clock = pygame.time.Clock()
    color_number = 0
    color_mode = 0
    cycle_count = 2000
    cycle_color = 0
    center_adjust_x = 0
    center_adjust_y = 0
    random_center_adjust = False
    pause = False
    bg_color_number = BG_COLOR_NAMES.index(args.background)
    win.fill(color=BG_COLOR_DICT[BG_COLOR_NAMES[bg_color_number]])
    pygame.display.update()
    stars = []
    for _ in range(10):
        s = Star(width,
                 height,
                 direction_list,
                 star_colors,
                 center_adjust_x,
                 center_adjust_y,
                 args.reverse,)
        s.cycle(10)
        stars.append(s)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.WINDOWRESIZED:
                width, height = pygame.display.get_window_size()
                center_adjust_y = center_adjust_x = 0
                stars.clear()
                for _ in range(10):
                    s = Star(width,
                             height,
                             direction_list,
                             star_colors,
                             center_adjust_x,
                             center_adjust_y,
                             args.reverse,)
                    s.cycle(10)
                    stars.append(s)
                continue
            elif event.type == pygame.KEYDOWN:
                if args.screensaver:
                    run = False
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
                elif key_pressed == "f":  # toggle back to window mode only
                    if args.full_screen:
                        args.full_screen = False
                        pygame.display.toggle_fullscreen()
                        pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT),
                                                pygame.RESIZABLE)
                        width, height = pygame.display.get_window_size()
                        center_adjust_y = center_adjust_x = 0
                        stars.clear()
                        for _ in range(10):
                            s = Star(width,
                                     height,
                                     direction_list,
                                     star_colors,
                                     center_adjust_x,
                                     center_adjust_y,
                                     args.reverse,)
                            s.cycle(10)
                            stars.append(s)
                elif key_pressed == "d":
                    # reset to default
                    num_of_stars = DEFAULT_STARS
                    speed_number = DEFAULT_SPEED
                    color_number = 0
                    star_colors.set_color_name(COLOR_LIST[color_number])
                    color_mode = 0
                    cycle_count = 2000
                    cycle_color = 0
                    center_adjust_y = center_adjust_x = 0
                    random_center_adjust = False
                    bg_color_number = 0
                    if args.reverse:
                        args.reverse = False
                        stars.clear()
                        for _ in range(10):
                            s = Star(width,
                                     height,
                                     direction_list,
                                     star_colors,
                                     center_adjust_x,
                                     center_adjust_y,
                                     args.reverse,)
                            s.cycle(10)
                            stars.append(s)
                elif key_pressed == "S r":
                    args.reverse = not args.reverse
                    stars.clear()
                    for _ in range(10):
                        s = Star(width,
                                 height,
                                 direction_list,
                                 star_colors,
                                 center_adjust_x,
                                 center_adjust_y,
                                 args.reverse, )
                        s.cycle(10)
                        stars.append(s)
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
                elif key_pressed == "r":
                    if random_center_adjust:
                        random_center_adjust = False
                        center_adjust_y = center_adjust_x = 0
                    else:
                        random_center_adjust = True
                elif key_pressed == "b":
                    if bg_color_number == len(BG_COLOR_NAMES) - 1:
                        bg_color_number = 0
                    else:
                        bg_color_number += 1
                elif key_pressed == "up" and not random_center_adjust:
                    if center_adjust_y > -(height // 2 - 25):
                        center_adjust_y -= 20
                elif key_pressed == "down" and not random_center_adjust:
                    if center_adjust_y < height // 2 - 25:
                        center_adjust_y += 20
                elif key_pressed == "left" and not random_center_adjust:
                    if center_adjust_x > -(width // 2 - 25):
                        center_adjust_x -= 20
                elif key_pressed == "right" and not random_center_adjust:
                    if center_adjust_x < width // 2 - 25:
                        center_adjust_x += 20
        if random_center_adjust:
            random_change = random.choice(["N", "U", "D", "L", "R"])
            if random_change == "U":
                if center_adjust_y > -(height // 2 - 25):
                    center_adjust_y -= 4
            elif random_change == "D":
                if center_adjust_y < height // 2 - 25:
                    center_adjust_y += 4
            elif random_change == "L":
                if center_adjust_x > -(width // 2 - 25):
                    center_adjust_x -= 4
            elif random_change == "R":
                if center_adjust_x < width // 2 - 25:
                    center_adjust_x += 4
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
            remove_list = []
            win.fill(color=BG_COLOR_DICT[BG_COLOR_NAMES[bg_color_number]])
            for star in stars:
                star.draw_star()
                if star.remove_star():
                    remove_list.append(star)
            pygame.display.flip()
            for remove in remove_list:
                stars.pop(stars.index(remove))
        if len(stars) <= number_list[num_of_stars]:
            for _ in range(2):
                s = Star(width,
                         height,
                         direction_list,
                         star_colors,
                         center_adjust_x,
                         center_adjust_y,
                         args.reverse,)
                stars.append(s)

        clock.tick(number_list[speed_number])


def argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--screensaver", action="store_true",
                        help="Screensaver mode. Any key will exit.")
    parser.add_argument("-f", "--full_screen", action="store_true",
                        help="Full screen mode. Use 'f' to switch back to "
                             "window mode.")
    parser.add_argument("-R", "--reverse", action="store_true",
                        help="Star go in reverse.")
    parser.add_argument("--color", choices=COLOR_LIST, default="white",
                        help="Set the color of the stars")
    parser.add_argument("--background", choices=BG_COLOR_NAMES, default="black",
                        help="Set background color.")
    return parser.parse_args()


def main() -> None:
    args = argument_parser()
    pygame.init()
    if args.full_screen:
        win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,)
    else:
        win = pygame.display.set_mode(
            (DEFAULT_WIDTH, DEFAULT_HEIGHT),
            pygame.RESIZABLE,
        )
    pygame.display.set_caption("Star Field")
    star_field_loop(win, args)


if __name__ == "__main__":
    main()
