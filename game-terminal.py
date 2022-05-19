import os
import time
import textwrap as tw
import random

# ------------------------------------------------------------------------------
# Environment Parameters

# Sets a var to the smaller of 80 characters or the user's terminal width.
print_width = min(80, os.get_terminal_size().columns)
# Set a var with the delay time between printing new lines.
scroll_delay = 0.06
# ------------------------------------------------------------------------------
# Game Parameters

# Map the difficulty levels 1-6 modulo 3 to the min and max random numbers
# for each level.
difficulty_dict = {1: {'min': 1, 'max': 10, 'guesses': 5},
                   2: {'min': 1, 'max': 100, 'guesses': 7},
                   0: {'min': -1000, 'max': 1000, 'guesses': 11}}
# ------------------------------------------------------------------------------


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


def y_n_query(input_prompt='Yes or No? ',
              error_prompt='Input of Yes or No required. '):
    """
    Prompts the user to answer Yes or No (Y or N), case insensitve.

    Args:
        input_prompt (str): The prompt to the user
        error_prompt (str): The prompt if the input is not accepted

    Returns:
        y_or_n (str): Returns 'yes' or 'no' depending on the user's input
    """
    y_or_n = input(input_prompt).lower()

    while y_or_n not in {'y', 'ye', 'ys', 'yes', 'n', 'no'}:
        y_or_n = input(error_prompt).lower()

    if y_or_n in {'n', 'no'}:
        y_or_n = 'no'
    else:
        y_or_n = 'yes'

    return y_or_n


def welcome():
    """Prints introductory text to the terminal."""
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
    """
    Prints instructions for the user to select game difficulty and solicits
    input.

    Returns:
        difficulty (int): An interger from 1-6 representing the user's
            chosen difficulty
        hard_mode (bool): A boolean indicating whether the user selected a hard
            difficulty
    """
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

    difficulty = int(difficulty)
    hard_mode = True if difficulty > 3 else False

    return difficulty, hard_mode


def pick_secret(difficulty):
    """
    Chooses the secret number within the constraints of the chosen
    difficulty level and initilizes the guesses_remaining variable. Prints
    conversation to the terminal.

    Args:
        difficulty (int): The integer output from the pick_difficulty()
        function.
    """
    wrap_scroll('Thinking...')

    min = difficulty_dict[difficulty % 3]['min']
    max = difficulty_dict[difficulty % 3]['max']
    secret = random.randrange(min, max + 1)
    guess_limit = difficulty_dict[difficulty % 3]['guesses']

    wrap_scroll('OK, I\'ve chosen a number!')
    wrap_scroll()

    return min, max, secret, guess_limit


def list_to_string(list, conj='and', oxford=False):
    """
    Handle conversion of lists into printable strings.

    Args:
        list (list): The list of items to convert to a string
        conj (str): The coordinating conjunction to be used between the
            final two items in the list
        oxford (bool): Indicate whether to use an oxford comma before the last
            item
    """
    oxford = ',' if oxford is True else ''

    list_len = len(list)

    if list_len == 0:
        str = ''
    elif list_len == 1:
        str = f'{list[0]}'
    elif list_len == 2:
        str = f'{list[0]} {conj} {list[1]}'
    else:
        for element in list:
            if list.index(element) == 0:
                str = f'{element}'
            elif list.index(element) < list_len - 1:
                str += f', {element}'
            else:
                str += f'{oxford} {conj} {element}'

    return str


def solicit_guess(min, max, guesses_remaining, hard_mode, prev_guess_list):
    guess = None
    while guess is None:
        wrap_scroll(f'Choose a number between {min} and {max}.')
        wrap_scroll(f'You have {guesses_remaining} guesses left.')
        if hard_mode is False and prev_guess_list != []:
            prev_guess_str = list_to_string(prev_guess_list, oxford=True)
            wrap_scroll(f'You have already guessed {prev_guess_str}')
        guess = input('> ')

        if guess not in (str(i) for i in range(min, max + 1)):
            guess = None
            wrap_scroll()
            wrap('Invalid input. Please try again.')
            h_div()
            time.sleep(1)
            wrap_scroll()

    guess = int(guess)
    guesses_remaining -= 1

    return guess, guesses_remaining


def check_guess(guess, secret, guess_limit, guesses_remaining):
    if guess == secret:
        turns = guess_limit - guesses_remaining
        wrap_scroll('Good guess!')
        wrap_scroll(f'It took you {turns} turns to guess my number, which was '
                    + f'{secret}.')
    elif guess < secret:
        wrap_scroll(f'Your guess, {guess}, is too low.')
    elif guess > secret:
        wrap_scroll(f'Your guess, {guess}, is too high.')


def main():
    welcome()
    while True:
        # Prompt user to set the difficulty, then choose the secret number.
        difficulty, hard_mode = pick_difficulty()
        min, max, secret, guess_limit = pick_secret(difficulty)

        # Initialize variables for this round.
        guesses_remaining = guess_limit
        guess = None
        prev_guess_list = []

        # Solicit guesses and compare to the secret number. Loop as needed.
        while guess != secret and guesses_remaining > 0:
            guess, guesses_remaining = solicit_guess(min, max,
                                                     guesses_remaining,
                                                     hard_mode, prev_guess_list)
            prev_guess_list.append(guess)
            prev_guess_list.sort()
            check_guess(guess, secret, guess_limit, guesses_remaining)

        # Handle guesses_remaining == 0 case.
        if guesses_remaining == 0:
            wrap_scroll('Good try! You ran out of turns to guess my number,'
                        + f'which was {secret}.')

        # Offer a new game.
        wrap_scroll('Would you like to play again?')
        wrap_scroll('Yes or No (Y/N):')
        play_again = y_n_query(input_prompt='> ',
                               error_prompt=wrap('Sorry, I need Yes or No to'
                                                 + ' continue.',
                                                 passthrough=True) + '\n> ')

        if play_again == 'no':
            break


if __name__ == "__main__":
    main()
