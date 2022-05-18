import os
import time
import textwrap as tw

# Sets a var to the smaller of 80 characters or the user's terminal width.
print_width = min(80, os.get_terminal_size().columns)


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


def wrap(str, width=print_width, passthrough=False):
    """
    Wraps a text string to the desired width. If using the default value, the
    print_width (int) variable must have been set with the desired value.

    Args:
        str: The string to wrap
        width (int): The maximum number of characters to allow per line; if
            using the default value, the print_width (int) variable must
            have been set with the desired value
        passthrough (bool): If False, calls the print function; if True, returns
            the text string without the print call
    """
    wrapped = '\n'.join(tw.wrap(str, width=width, replace_whitespace=False))

    if passthrough is False:
        print(wrapped)
    else:
        return wrapped


# Set a var with the delay time between printing new lines.
scroll_delay = 0.06


def h_div_scroll(width=print_width, nl_above=0, nl_below=0,
                 delay=scroll_delay):
    """
    Performs the h_div() function, then performs a time.sleep() delay.

    Args:
        width (int): The number of '-' characters to print in the divider
            line; if using the default value, the print_width (int)
            variable must have been set with the desired value
        nl_above (int): The number of newline characters to print before the
            divider
        nl_below (int): The number of newline characters to print after the
            divider
        delay (float or int): The time in seconds to delay before allowing
            the script to continue executing; if using the default value,
            the scroll_delay (float) variable must have been set with the
            desired value
    """
    h_div(width=width, nl_above=nl_above, nl_below=nl_below)
    time.sleep(delay)


def wrap_scroll(str='', width=print_width, delay=scroll_delay):
    """
    Applies the wrap() function to a string, then performs a time.sleep()
    delay.

    Args:
        str: The string to wrap and print
        width (int): The maximum number of characters to allow per line; if
            using the default value, the print_width (int) variable must
            have been set with the desired value
        delay (float or int): The time in seconds to delay before allowing
            the script to continue executing; if using the default value,
            the scroll_delay (float) variable must have been set with the
            desired value
    """
    wrap(str, width=width)
    time.sleep(delay)


def welcome():
    h_div(nl_above=2, nl_below=1)
    wrap_scroll('Guess the Number!')
    wrap_scroll()
    wrap_scroll()
    wrap_scroll('How to play:')
    wrap_scroll()
    wrap_scroll('* The Computer will pick a secret number.')
    wrap_scroll('* You guess what number the computer chose.')
    wrap_scroll('* If your guess is too high or too low, Computer will '
                'give you a hint.')
    wrap_scroll('* See how many turns it takes you to win!')
    wrap_scroll()
    wrap_scroll()


def pick_difficulty():
    difficulty = None
    while difficulty is None:
        wrap_scroll('Pick a difficulty level and number range:')
        wrap_scroll()
        wrap_scroll('Easy (Show previous guesses)')
        wrap_scroll('   1. 1 - 10')
        wrap_scroll('   2. 1 - 100')
        wrap_scroll('   3. -1000 - 1000')
        wrap_scroll()
        wrap_scroll('Hard (Don\'t show guesses)')
        wrap_scroll('   4. 1 - 10')
        wrap_scroll('   5. 1 - 100')
        wrap_scroll('   6. -1000 - 1000')
        wrap_scroll()

        wrap_scroll('Enter the number 1-6 for your difficulty choice:')
        difficulty = input('> ')
        if difficulty not in (str(i) for i in range(1, 7)):
            difficulty = None
            wrap_scroll()
            wrap('Invalid input. Please try again.')
            h_div()
            time.sleep(1)
            wrap_scroll()

    return difficulty


def main():
    welcome()
    while True:
        difficulty = pick_difficulty()


        break


if __name__ == "__main__":
    main()
