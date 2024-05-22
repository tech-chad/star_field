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
MODES = ["solid_color", "cycle_color", "fade_color"]
FADE_STEPS = [(-1, -1, 0), (0, 1, 0), (0, 0, -1), (1, 0, 0), (0, -1, 0),
              (0, 0, 1), (0, 1, 0), (-1, 0, -1), (1, -1, 0), (0, 1, 1),
              (-1, 0, -1), (0, -1, 0), (1, 1, 1)]

FADE_GOAL = [(0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 255, 0),
             (255, 0, 0), (255, 0, 255), (255, 255, 255), (0, 255, 0),
             (255, 0, 0), (255, 255, 255), (0, 255, 0), (0, 0, 0),
             (255, 255, 255)]


class StarColor:
    def __init__(self) -> None:
        self.total_num_color_shades = 8
        self.color_dict = {"white": (255, 255, 255), "red": (255, 0, 0),
                           "green": (0, 255, 0), "blue": (0, 0, 255),
                           "cyan": (0, 255, 255), "magenta": (255, 0, 255),
                           "yellow": (255, 255, 0), "teal": (0, 255, 150),
                           "orange": (255, 128, 0), "purple": (190, 0, 255)}
        self.color = self.color_dict["white"]
        self.shade_list: List[Tuple[int, int, int]] = []
        self.make_shades()

    def get_color(self, color_number: int) -> Tuple[int, int, int]:
        if color_number > len(self.shade_list) - 1:
            color_number = len(self.shade_list) - 1
        return self.shade_list[color_number]

    def set_color_name(self, name: str) -> None:
        self.color = self.color_dict[name]
        self.make_shades()

    def set_color_rgb(self, red: int, green: int, blue: int) -> None:
        self.color = (red, green, blue)
        self.make_shades()

    def set_default_color(self) -> None:
        ...

    def num_color_shades(self) -> int:
        return self.total_num_color_shades

    def set_brightness(self, number: int) -> None:
        if number == 1:
            self.total_num_color_shades = 1
        elif number == 2:
            self.total_num_color_shades = 4
        elif number == 3:
            self.total_num_color_shades = 8
        elif number == 4:
            self.total_num_color_shades = 10
        elif number == 5:
            self.total_num_color_shades = 12
        self.make_shades()

    def make_shades(self) -> None:
        self.shade_list.clear()
        i = 0.0
        for _ in range(self.total_num_color_shades + 1):
            color = (int(self.color[0]-(self.color[0] * i)),
                     int(self.color[1]-(self.color[1] * i)),
                     int(self.color[2]-(self.color[2] * i)))
            self.shade_list.append(color)
            i += 0.075


class Star:
    def __init__(self,
                 screen_width: int,
                 screen_height: int,
                 direction_list: List[Tuple[int, int]],
                 star_color: StarColor,
                 center_adjust_x: int,
                 center_adjust_y: int,
                 reverse: bool) -> None:
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
            dx = (self.center_x - self.x) // speed
            dy = (self.center_y - self.y) // speed
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


def make_direction_list() -> List[Tuple[int, int]]:
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


class StarField:
    def __init__(self, win: pygame.Surface, args: argparse.Namespace) -> None:
        pygame.key.set_repeat()  # could be moved to the main function
        self.win = win
        self.args = args
        self.key_pressed = ""
        self.num_of_stars = DEFAULT_STARS
        self.speed_number = DEFAULT_SPEED
        self.direction_list = make_direction_list()
        self.star_colors = StarColor()
        self.color_number = 0
        if self.args.fade:
            self.color_mode = 2
        else:
            self.color_mode = 0
        self.fade_color = (255, 255, 255)
        self.fade_color_step = 0
        self.fade_color_time = 5
        self.cycle_count = 2000
        self.cycle_color = 0
        self.center_adjust_x = 0
        self.center_adjust_y = 0
        self.random_center_adjust = False
        self.bg_color_number = BG_COLOR_NAMES.index(self.args.background)
        self.width, self.height = pygame.display.get_window_size()
        self.stars: List[Star] = []
        self.run = True
        self.pause = False

    def main_loop(self) -> None:
        number_list = [i for i in range(220, 39, -20)]  # for number of star
        self.star_colors.set_brightness(self.args.brightness)
        if MODES[self.color_mode] == "fade_color":
            self.star_colors.set_color_rgb(*self.fade_color)
        else:
            self.star_colors.set_color_name(self.args.color)
        clock = pygame.time.Clock()
        self.win.fill(color=BG_COLOR_DICT[BG_COLOR_NAMES[self.bg_color_number]])
        pygame.display.update()
        self.load_stars(10, True)
        while self.run:
            self.events()
            if self.random_center_adjust:
                random_change = random.choice(["N", "U", "D", "L", "R"])
                if random_change == "U":
                    if self.center_adjust_y > -(self.height // 2 - 25):
                        self.center_adjust_y -= 4
                elif random_change == "D":
                    if self.center_adjust_y < self.height // 2 - 25:
                        self.center_adjust_y += 4
                elif random_change == "L":
                    if self.center_adjust_x > -(self.width // 2 - 25):
                        self.center_adjust_x -= 4
                elif random_change == "R":
                    if self.center_adjust_x < self.width // 2 - 25:
                        self.center_adjust_x += 4
            if (MODES[self.color_mode] == "cycle_color" and
                    self.cycle_count <= 0 and not self.pause):

                if self.cycle_color < len(COLOR_LIST) - 1:
                    self.cycle_color += 1
                else:
                    self.cycle_color = 0
                self.star_colors.set_color_name(COLOR_LIST[self.cycle_color])
                self.cycle_count = 2000
            elif MODES[self.color_mode] == "cycle_color" and not self.pause:
                self.cycle_count -= 1
            elif MODES[self.color_mode] == "fade_color" and not self.pause:
                if self.fade_color_time == 0:
                    self.next_fade_color()
                    self.star_colors.set_color_rgb(*self.fade_color)
                    self.fade_color_time = 5
                else:
                    self.fade_color_time -= 1
            if not self.pause:
                remove_list = []
                self.win.fill(
                    color=BG_COLOR_DICT[BG_COLOR_NAMES[self.bg_color_number]])
                for star in self.stars:
                    star.draw_star()
                    if star.remove_star():
                        remove_list.append(star)
                pygame.display.flip()
                for remove in remove_list:
                    self.stars.pop(self.stars.index(remove))
            if len(self.stars) <= number_list[self.num_of_stars]:
                self.load_stars(2, False)
            clock.tick(number_list[self.speed_number])

    def load_stars(self, number: int, cycle: bool) -> None:
        for _ in range(number):
            s = Star(self.width,
                     self.height,
                     self.direction_list,
                     self.star_colors,
                     self.center_adjust_x,
                     self.center_adjust_y,
                     self.args.reverse)
            if cycle:
                s.cycle(10)
            self.stars.append(s)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.WINDOWRESIZED:
                self.width, self.height = pygame.display.get_window_size()
                self.center_adjust_y = self.center_adjust_x = 0
                self.stars.clear()
                self.load_stars(10, True)
                continue
            elif event.type == pygame.KEYDOWN:
                if self.args.screensaver:
                    self.run = False
                self.get_key_pressed()
                if self.key_pressed in ["q" or "S q"]:
                    self.run = False
                elif self.key_pressed == "p":
                    self.pause = not self.pause
                elif self.pause:
                    continue
                self.process_key_press()

    def process_key_press(self) -> None:
        if self.key_pressed in ["S 0", "S 1", "S 2", "S 3", "S 4", "S 5",
                                "S 6", "S 7", "S 8", "S 9"]:
            self.num_of_stars = int(self.key_pressed[-1])
        elif self.key_pressed in ["0", "1", "2", "3", "4", "5", "6",
                                  "7", "8", "9"]:
            self.speed_number = int(self.key_pressed)
        elif self.key_pressed == "f":  # toggle back to window mode only
            if self.args.full_screen:
                self.args.full_screen = False
                pygame.display.toggle_fullscreen()
                pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT),
                                        pygame.RESIZABLE)
                self.width, self.height = pygame.display.get_window_size()
                self.center_adjust_y = self.center_adjust_x = 0
                self.stars.clear()
                self.load_stars(10, True)
        elif self.key_pressed == "d":
            # reset to default
            self.num_of_stars = DEFAULT_STARS
            self.speed_number = DEFAULT_SPEED
            self.color_number = 0
            self.color_mode = 0
            self.cycle_count = 2000
            self.cycle_color = 0
            self.center_adjust_y = self.center_adjust_x = 0
            self.random_center_adjust = False
            self.bg_color_number = 0
            self.args.brightness = 3
            self.star_colors.set_color_name(COLOR_LIST[self.color_number])
            self.star_colors.set_brightness(self.args.brightness)
            if self.args.reverse:
                self.args.reverse = False
                self.stars.clear()
                self.load_stars(10, True)
        elif self.key_pressed == "S r":
            self.args.reverse = not self.args.reverse
            self.stars.clear()
            self.load_stars(10, True)
        elif self.key_pressed == "n" and MODES[self.color_mode] == "solid_color":
            if self.color_number < len(COLOR_LIST) - 1:
                self.color_number += 1
            else:
                self.color_number = 0
            self.star_colors.set_color_name(COLOR_LIST[self.color_number])
        elif self.key_pressed == "m":
            if self.color_mode < len(MODES) - 1:
                self.color_mode += 1
            else:
                self.color_mode = 0
            if MODES[self.color_mode] == "cycle_color":
                self.star_colors.set_color_name(COLOR_LIST[self.cycle_color])
            elif MODES[self.color_mode] == "solid_color":
                self.star_colors.set_color_name(COLOR_LIST[self.color_number])
        elif self.key_pressed == "r":
            if self.random_center_adjust:
                self.random_center_adjust = False
                self.center_adjust_y = self.center_adjust_x = 0
            else:
                self.random_center_adjust = True
        elif self.key_pressed == "b":
            if self.bg_color_number == len(BG_COLOR_NAMES) - 1:
                self.bg_color_number = 0
            else:
                self.bg_color_number += 1
        elif self.key_pressed == "up" and not self.random_center_adjust:
            if self.center_adjust_y > -(self.height // 2 - 25):
                self.center_adjust_y -= 20
        elif self.key_pressed == "down" and not self.random_center_adjust:
            if self.center_adjust_y < self.height // 2 - 25:
                self.center_adjust_y += 20
        elif self.key_pressed == "left" and not self.random_center_adjust:
            if self.center_adjust_x > -(self.width // 2 - 25):
                self.center_adjust_x -= 20
        elif self.key_pressed == "right" and not self.random_center_adjust:
            if self.center_adjust_x < self.width // 2 - 25:
                self.center_adjust_x += 20

    def get_key_pressed(self) -> None:
        self.key_pressed = ""
        keys = pygame.key.get_pressed()
        look_for = {pygame.K_q: "q", pygame.K_m: "m", pygame.K_0: "0",
                    pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
                    pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6",
                    pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9",
                    pygame.K_p: "p", pygame.K_n: "n", pygame.K_f: "f",
                    pygame.K_d: "d", pygame.K_DOWN: "down",
                    pygame.K_UP: "up", pygame.K_LEFT: "left",
                    pygame.K_RIGHT: "right", pygame.K_r: "r", pygame.K_b: "b",
                    pygame.K_a: "a"}
        for k in look_for.keys():
            if keys[k] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                self.key_pressed = f"S {look_for[k]}"
                break
            elif keys[k]:
                self.key_pressed = look_for[k]
                break

    def next_fade_color(self) -> None:
        r, g, b = self.fade_color
        dr, dg, db = FADE_STEPS[self.fade_color_step]
        self.fade_color = (r + dr, g + dg, b + db)
        if self.fade_color == FADE_GOAL[self.fade_color_step]:
            if self.fade_color_step >= len(FADE_STEPS) - 1:
                self.fade_color_step = 0
            else:
                self.fade_color_step += 1


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
    parser.add_argument("--brightness", choices=range(1, 6), type=int,
                        default=3,
                        help="Set the star brightness 1-Brightest, 3-Default, "
                             "5-Dimmest")
    parser.add_argument("--fade", action="store_true",
                        help="Fade through the colors")
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
    star_field = StarField(win, args)
    star_field.main_loop()


if __name__ == "__main__":
    main()
