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
    """Clears the terminal and prints introductory text."""
    os.system('cls||clear')  # Clear screen
    wrap('Guess the Number!')
    time.sleep(0.6)
    print()
    print()
    wrap('How to play:')
    print()
    wrap('* The Computer will pick a secret number.')
    wrap('* You guess what number the computer chose.')
    wrap('* If your guess is too high or too low, Computer will give you a '
         + 'hint.')
    wrap('* See how many turns it takes you to win!')
    time.sleep(1)
    print()
    print()


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
        wrap('Pick a difficulty level and number range:')
        print()
        wrap('Easy (Show previous guesses)')
        wrap('   1. 1 - 10')
        wrap('   2. 1 - 100')
        wrap('   3. -1000 - 1000')
        print()
        wrap('Hard (Don\'t show guesses)')
        wrap('   4. 1 - 10')
        wrap('   5. 1 - 100')
        wrap('   6. -1000 - 1000')
        print()

        wrap('Enter the number 1-6 for your difficulty choice:')
        print()
        difficulty = input('> ')
        if difficulty not in (str(i) for i in range(1, 7)):
            difficulty = None
            print()
            wrap('Invalid input. Please try again.')
            time.sleep(1)
            os.system('cls||clear')  # Clear screen

    difficulty = int(difficulty)
    hard_mode = True if difficulty > 3 else False

    return difficulty, hard_mode


def pick_secret(difficulty):
    """
    Chooses the secret number within the constraints of the chosen
    difficulty level and initilizes the guesses_remaining variable. Clears
    screen in preparation for guesses.

    Args:
        difficulty (int): The integer output from the pick_difficulty()
        function.
    """
    min = difficulty_dict[difficulty % 3]['min']
    max = difficulty_dict[difficulty % 3]['max']
    secret = random.randrange(min, max + 1)
    guess_limit = difficulty_dict[difficulty % 3]['guesses']

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


def solicit_guess(min, max, secret, guesses_remaining, hard_mode, last_guess,
                  prev_guess_list):
    guess = None
    while guess is None:
        os.system('cls||clear')  # Clear screen

        if last_guess is not None:
            if last_guess < secret:
                wrap(f'Your guess, {last_guess}, is too low.')
                print()
            elif last_guess > secret:
                wrap(f'Your guess, {last_guess}, is too high.')
                print()

        wrap(f'Choose a number between {min} and {max}.')
        wrap(f'You have {guesses_remaining} guesses left.')
        if hard_mode is False and prev_guess_list != []:
            prev_guess_str = list_to_string(prev_guess_list, oxford=True)
            wrap(f'You have already guessed {prev_guess_str}.')
        print()
        guess = input('> ')

        if guess not in (str(i) for i in range(min, max + 1)):
            guess = None
            print()
            wrap('Invalid input. Please try again.')
            time.sleep(1)

    guess = int(guess)
    guesses_remaining -= 1

    return guess, guesses_remaining


def check_guess(guess, secret, guess_limit, guesses_remaining):
    turns = guess_limit - guesses_remaining
    if guess == secret:
        os.system('cls||clear')  # Clear screen
        wrap('Good guess!')
        wrap(f'It took you {turns} turns to guess my number, which was '
             + f'{secret}.')
        print()


def main():
    welcome()
    while True:
        # Prompt user to set the difficulty, then choose the secret number.
        difficulty, hard_mode = pick_difficulty()
        min, max, secret, guess_limit = pick_secret(difficulty)

        # Initialize variables for this round.
        guesses_remaining = guess_limit
        guess = None
        last_guess = None
        prev_guess_list = []

        # Solicit guesses and compare to the secret number. Loop as needed.
        while guess != secret and guesses_remaining > 0:
            guess, guesses_remaining = solicit_guess(min, max, secret,
                                                     guesses_remaining,
                                                     hard_mode, last_guess,
                                                     prev_guess_list)
            prev_guess_list.append(guess)
            prev_guess_list.sort()
            check_guess(guess, secret, guess_limit, guesses_remaining)
            last_guess = guess

        # Handle guesses_remaining == 0 case.
        if guesses_remaining == 0:
            wrap('Good try! You ran out of turns to guess my number, which was '
                 + f'{secret}.')
            print()

        # Offer a new game.
        wrap('Would you like to play again?')
        wrap('Yes or No (Y/N):')
        print()
        play_again = y_n_query(input_prompt='> ',
                               error_prompt=('\n'
                                            + wrap('Sorry, I need Yes or No to'
                                                   + ' continue.',
                                                   passthrough=True)
                                            + '\n\n> '))

        os.system('cls||clear')  # Clear screen
        if play_again == 'no':
            break


if __name__ == "__main__":
    main()
