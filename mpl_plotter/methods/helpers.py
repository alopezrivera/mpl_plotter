from math import ceil
from termcolor import colored


def base(x, base):
    return base*ceil(x/base)


def print_color(text, color):
    print(colored('{}'.format(text), color))
