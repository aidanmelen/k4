from collections import namedtuple

import curses

Color = namedtuple('Color', ['name', 'id', 'r', 'g', 'b'])

WHITE = Color('WHITE', 10, 1000, 1000, 1000)
GRAY = Color('GRAY', 20, 298, 298, 298)
LIGHT_GRAY = Color('LIGHT_GRAY', 25, 470, 533, 596)
BLACK = Color('BLACK', 30, 0, 0, 0)
RED = Color('RED', 40, 913, 254, 105)
GREEN = Color('GREEN', 50, 98, 674, 113)
BLUE = Color('BLUE', 60, 125, 450, 776)
LIGHT_BLUE = Color('LIGHT_BLUE', 65, 541, 811, 972)
PINK = Color('PINK', 70, 988, 156, 988)
YELLOW = Color('YELLOW', 80, 988, 643, 156)
ORANGE = Color('ORANGE', 90, 968, 368, 121)
CYAN = Color('CYAN', 100, 384, 686, 682)
BRIGHT_CYAN = Color('BRIGHT_CYAN', 110, 165, 929, 925)


ColorPair = namedtuple('ColorPair', ['name', 'id', 'fg_color', 'bg_color'])

WHITE_ON_BLACK = ColorPair('WHITE_ON_BLACK', WHITE.id + BLACK.id, WHITE.id, BLACK.id)
BLACK_ON_WHITE = ColorPair('BLACK_ON_WHITE', BLACK.id + WHITE.id + 1, BLACK.id, WHITE.id)

GRAY_ON_BLACK = ColorPair('GRAY_ON_BLACK', GRAY.id + BLACK.id, GRAY.id, BLACK.id)
BLACK_ON_GRAY = ColorPair('BLACK_ON_GRAY', BLACK.id + GRAY.id + 1, BLACK.id, GRAY.id)

LIGHT_GRAY_ON_BLACK = ColorPair('LIGHT_GRAY_ON_BLACK', LIGHT_GRAY.id + BLACK.id, LIGHT_GRAY.id, BLACK.id)
BLACK_ON_LIGHT_GRAY = ColorPair('BLACK_ON_LIGHT_GRAY', BLACK.id + LIGHT_GRAY.id + 1, BLACK.id, LIGHT_GRAY.id)

RED_ON_BLACK = ColorPair('RED_ON_BLACK', RED.id + BLACK.id, RED.id, BLACK.id)
BLACK_ON_RED = ColorPair('BLACK_ON_RED', BLACK.id + RED.id + 1, BLACK.id, RED.id)

GREEN_ON_BLACK = ColorPair('GREEN_ON_BLACK', GREEN.id + BLACK.id, GREEN.id, BLACK.id)
BLACK_ON_GREEN = ColorPair('BLACK_ON_GREEN', BLACK.id + GREEN.id + 1, BLACK.id, GREEN.id)

BLUE_ON_BLACK = ColorPair('BLUE_ON_BLACK', BLUE.id + BLACK.id, BLUE.id, BLACK.id)
BLACK_ON_BLUE = ColorPair('BLACK_ON_BLUE', BLACK.id + BLUE.id + 1, BLACK.id, BLUE.id)

LIGHT_BLUE_ON_BLACK = ColorPair('LIGHT_BLUE_ON_BLACK', LIGHT_BLUE.id + BLACK.id, LIGHT_BLUE.id, BLACK.id)
BLACK_ON_LIGHT_BLUE = ColorPair('BLACK_ON_LIGHT_BLUE', BLACK.id + LIGHT_BLUE.id + 1,  BLACK.id, LIGHT_BLUE.id)

PINK_ON_BLACK = ColorPair('PINK_ON_BLACK', PINK.id + BLACK.id, PINK.id, BLACK.id)
BLACK_ON_PINK = ColorPair('BLACK_ON_PINK', BLACK.id + PINK.id + 1, BLACK.id, PINK.id)

YELLOW_ON_BLACK = ColorPair('YELLOW_ON_BLACK', YELLOW.id + BLACK.id, YELLOW.id, BLACK.id)
BLACK_ON_YELLOW = ColorPair('BLACK_ON_YELLOW', BLACK.id + YELLOW.id + 1, BLACK.id, YELLOW.id)

ORANGE_ON_BLACK = ColorPair('ORANGE_ON_BLACK', ORANGE.id + BLACK.id, ORANGE.id, BLACK.id)
BLACK_ON_ORANGE = ColorPair('BLACK_ON_ORANGE', BLACK.id + ORANGE.id + 1, BLACK.id, ORANGE.id)

CYAN_ON_BLACK = ColorPair('CYAN_ON_BLACK', CYAN.id + BLACK.id, CYAN.id, BLACK.id)
BLACK_ON_CYAN = ColorPair('BLACK_ON_CYAN', BLACK.id + CYAN.id + 1, BLACK.id, CYAN.id)

BRIGHT_CYAN_ON_BLACK = ColorPair('BRIGHT_CYAN_ON_BLACK', BRIGHT_CYAN.id + BLACK.id, BRIGHT_CYAN.id, BLACK.id)
BLACK_ON_BRIGHT_CYAN = ColorPair('BLACK_ON_BRIGHT_CYAN', BLACK.id + BRIGHT_CYAN.id + 1, BLACK.id, BRIGHT_CYAN.id)


def init_custom_colors():
    curses.init_color(WHITE.id, WHITE.r, WHITE.g, WHITE.b)
    curses.init_color(GRAY.id, GRAY.r, GRAY.g, GRAY.b)
    curses.init_color(LIGHT_GRAY.id, LIGHT_GRAY.r, LIGHT_GRAY.g, LIGHT_GRAY.b)
    curses.init_color(BLACK.id, BLACK.r, BLACK.g, BLACK.b)
    curses.init_color(RED.id, RED.r, RED.g, RED.b)
    curses.init_color(GREEN.id, GREEN.r, GREEN.g, GREEN.b)
    curses.init_color(BLUE.id, BLUE.r, BLUE.g, BLUE.b)
    curses.init_color(LIGHT_BLUE.id, LIGHT_BLUE.r, LIGHT_BLUE.g, LIGHT_BLUE.b)
    curses.init_color(PINK.id, PINK.r, PINK.g, PINK.b)
    curses.init_color(YELLOW.id, YELLOW.r, YELLOW.g, YELLOW.b)
    curses.init_color(ORANGE.id, ORANGE.r, ORANGE.g, ORANGE.b)
    curses.init_color(CYAN.id, CYAN.r, CYAN.g, CYAN.b)
    curses.init_color(BRIGHT_CYAN.id, BRIGHT_CYAN.r, BRIGHT_CYAN.g, BRIGHT_CYAN.b)


def init_custom_color_pairs():
    curses.init_pair(BLACK.id, -1, BLACK.id)
    curses.init_pair(WHITE.id, -1, WHITE.id)

    curses.init_pair(WHITE_ON_BLACK.id, WHITE_ON_BLACK.fg_color, WHITE_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_WHITE.id, BLACK_ON_WHITE.fg_color, BLACK_ON_WHITE.bg_color)
    curses.init_pair(WHITE_ON_BLACK.id, WHITE_ON_BLACK.fg_color, WHITE_ON_BLACK.bg_color)
    curses.init_pair(GRAY_ON_BLACK.id, GRAY_ON_BLACK.fg_color, GRAY_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_GRAY.id, BLACK_ON_GRAY.fg_color, BLACK_ON_GRAY.bg_color)
    curses.init_pair(LIGHT_GRAY_ON_BLACK.id, LIGHT_GRAY_ON_BLACK.fg_color, LIGHT_GRAY_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_LIGHT_GRAY.id, BLACK_ON_LIGHT_GRAY.fg_color, BLACK_ON_LIGHT_GRAY.bg_color)
    curses.init_pair(RED_ON_BLACK.id, RED_ON_BLACK.fg_color, RED_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_RED.id, BLACK_ON_RED.fg_color, BLACK_ON_RED.bg_color)
    curses.init_pair(GREEN_ON_BLACK.id, GREEN_ON_BLACK.fg_color, GREEN_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_GREEN.id, BLACK_ON_GREEN.fg_color, BLACK_ON_GREEN.bg_color)
    curses.init_pair(BLUE_ON_BLACK.id, BLUE_ON_BLACK.fg_color, BLUE_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_BLUE.id, BLACK_ON_BLUE.fg_color, BLACK_ON_BLUE.bg_color)
    curses.init_pair(LIGHT_BLUE_ON_BLACK.id, LIGHT_BLUE_ON_BLACK.fg_color, LIGHT_BLUE_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_LIGHT_BLUE.id, BLACK_ON_LIGHT_BLUE.fg_color, BLACK_ON_LIGHT_BLUE.bg_color)
    curses.init_pair(PINK_ON_BLACK.id, PINK_ON_BLACK.fg_color, PINK_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_PINK.id, BLACK_ON_PINK.fg_color, BLACK_ON_PINK.bg_color)
    curses.init_pair(YELLOW_ON_BLACK.id, YELLOW_ON_BLACK.fg_color, YELLOW_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_YELLOW.id, BLACK_ON_YELLOW.fg_color, BLACK_ON_YELLOW.bg_color)
    curses.init_pair(ORANGE_ON_BLACK.id, ORANGE_ON_BLACK.fg_color, ORANGE_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_ORANGE.id, BLACK_ON_ORANGE.fg_color, BLACK_ON_ORANGE.bg_color)
    curses.init_pair(CYAN_ON_BLACK.id, CYAN_ON_BLACK.fg_color, CYAN_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_CYAN.id, BLACK_ON_CYAN.fg_color, BLACK_ON_CYAN.bg_color)
    curses.init_pair(BRIGHT_CYAN_ON_BLACK.id, BRIGHT_CYAN_ON_BLACK.fg_color, BRIGHT_CYAN_ON_BLACK.bg_color)
    curses.init_pair(BLACK_ON_BRIGHT_CYAN.id, BLACK_ON_BRIGHT_CYAN.fg_color, BLACK_ON_BRIGHT_CYAN.bg_color)