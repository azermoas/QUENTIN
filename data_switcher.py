import os
import sys
from curses import wrapper


def list_files(directory: str):
    """Return a list of non-hidden files in the given directory."""
    return [f for f in os.listdir(directory) if not f.startswith('.')]


def open_file(path: str):
    """Open a file using the system's default viewer."""
    if sys.platform.startswith('darwin'):
        os.system(f'open "{path}"')
    elif sys.platform.startswith('linux'):
        os.system(f'xdg-open "{path}"')
    elif sys.platform.startswith('win'):
        os.startfile(path)


def run_menu(stdscr, directory):
    curses = __import__('curses')
    curses.curs_set(0)
    files = list_files(directory)
    index = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for i, file in enumerate(files):
            if i == index:
                stdscr.addstr(i, 0, f"> {file}", curses.A_REVERSE)
            else:
                stdscr.addstr(i, 0, f"  {file}")

        key = stdscr.getch()
        if key in (curses.KEY_DOWN, ord('j')):
            index = (index + 1) % len(files)
        elif key in (curses.KEY_UP, ord('k')):
            index = (index - 1) % len(files)
        elif key in (curses.KEY_ENTER, 10, 13):
            open_file(os.path.join(directory, files[index]))
        elif key in (ord('q'), 27):
            break

        stdscr.refresh()


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    wrapper(run_menu, directory)


if __name__ == "__main__":
    main()
