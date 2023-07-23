#!/usr/bin/python3

import argparse
import inspect
import os
import subprocess
import time
import curses


def r(*path):
    """
    Takes a relative path from the directory of this python file and returns the absolute path.
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *path)


def run_in_dir(directory, callable):
    cwd = os.getcwd()
    os.chdir(directory)
    result = callable()
    os.chdir(cwd)
    return result


keybinds = {
    "navigate_right": [curses.KEY_RIGHT, ord("l")],
    "navigate_left": [curses.KEY_LEFT, ord("h")],
    "navigate_down": [curses.KEY_DOWN, ord("j")],
    "navigate_up": [curses.KEY_UP, ord("k")],
    "paint": [ord("p"), ord(" ")],
    "select_brush": ord("s"),
}


keymap = {}
for function, keys in keybinds.items():
    if not (type(keys) is list):
        keys = [keys]
    for key in keys:
        keymap[key] = function



def main():
    def curses_wrapped(screen: curses.window):
        # screen.keypad(True)

        cursor_y, cursor_x = 0, 0
        brush = "X"

        # Setup curses
        image_height, image_width = 20, 80
        # Add 1 to the heights of the actual windows to be able to paint out the last cell
        frame_window = curses.newwin(image_height + 3, image_width + 2, 2, 2)
        image_window = curses.newwin(image_height, image_width, 3, 3)
        image_window.keypad(True)
        # curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # image_window.addstr("hm: " + str(curses.can_change_color()))
        # image_window.addstr("ja", curses.color_pair(1))
        frame_window.addstr(0, 0, "+" + ("-" * image_width) + "+")
        for _ in range(image_height):
            frame_window.addstr("|" + (" " * image_width) + "|")
        frame_window.addstr("+" + ("-" * image_width) + "+")
        frame_window.refresh()

        while True:
            image_window.move(cursor_y, cursor_x)
            # curses.setsyx(cursor_y, cursor_x)
            image_window.refresh()

            key = image_window.getch()
            try:
                function = keymap[key]
            except:
                continue

            match function:
                case "navigate_right":
                    cursor_x += 1
                case "navigate_left":
                    cursor_x -= 1
                case "navigate_down":
                    cursor_y += 1
                case "navigate_up":
                    cursor_y -= 1
                case "select_brush":
                    brush = image_window.getkey()
                case "paint":
                    # cursor_y += 1
                    image_window.addstr(brush)
                case _:
                    # This should not be possible
                    pass


            # ch = image_window.getch()

            # image_window.addstr(str(curses.KEY_RIGHT) + ", " + str(ch) + ", " + str(type(ch)))
            

    
    curses.wrapper(curses_wrapped)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    for parameter in inspect.signature(main).parameters:
        argument_parser.add_argument(parameter)
    arguments = argument_parser.parse_args()
    main(**vars(arguments))
