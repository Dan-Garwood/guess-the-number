import os
import textwrap as tw


def h_div(width=print_width, nl_above=0, nl_below=0, passthrough=False):
    """
    Prints a series of dashes to produce a horizontal divider.

    Args:
        width (int): The number of '-' characters to print in the divider line;
            if using the default value, the print_width (int) variable must have
            been set with the desired value
        nl_above (int): The number of newline characters to print before the
            divider
        nl_below (int): The number of newline characters to print after the
            divider
        passthrough (bool): If False, calls the print function; if True,
            returns the text string without the print call
    """
    div_str = ('\n' * nl_above) + ('-' * width) + ('\n' * nl_below)

    if passthrough is False:
        print(div_str)
    else:
        return div_str


def wrap(str, width=print_width):
    """
    Wraps a text string to the desired width. If using the default value, the
    print_width (int) variable must have been set with the desired value.
    """
    wrapped = '\n'.join(tw.wrap(str, width=width, replace_whitespace=False))
    return wrapped


def init():
    """
    Performs preparatory actions, such as initializing variables, before
    performing the main loop.
    """
    # Sets print_width to the smaller of 70 characters or the user's terminal
    # width.
    global print_width
    print_width = min(70, os.get_terminal_size().columns)


def main():
    pass


if __name__ == "__main__":
    init()
    main()
