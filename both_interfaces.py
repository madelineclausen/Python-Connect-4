# Madeline Clausen
# 60633236
from collections import namedtuple
import connectfour

def setup() -> tuple:
    """
    Handles the initialization. Asks for columns and
    rows in order to create game board.
    """
    print('~WELCOME TO CONNECT FOUR~')
    while True:
        try:
            columns = int(input('Enter how many columns you would like to have: \n'))
            if 20 >= columns >= 4:
                break
            else:
                print('Invalid number of columns. Try again.')
        except ValueError:
            print('Not a number. Try again.')
    while True:
        try:
            rows = int(input('Enter how many rows you would like to have: \n'))
            if 20 >= rows >= 4:
                break
            else:
                print('Invalid number of rows. Try again.')
        except ValueError:
            print('Not a number. Try again.')
    return connectfour.new_game(columns, rows)

def print_whose_turn(game: tuple) -> None:
    """
    Prints a box to the shell informing whose turn
    it is. It's always red or yellow.
    """
    if game.turn == 1:
            whose_turn = 'RED'
    else:
        whose_turn = 'YELLOW'
    print(' ' + '*' * 18)
    print(' ' + '*' + '{:^16}'.format(whose_turn + '\'S TURN') + '*')
    print(' ' + '*' * 18)
    print()

    
def print_board(game: tuple) -> None:
    """
    Takes in the game state tuple, indicating through 0s, 1s,
    and 2s where players have gone. Those numbers are converted
    and a user-friendly game board is printed. Function is
    called after each play.
    """
    print()
    for length in range(connectfour.columns(game)):
        if len(str(length + 1)) == 2:
            print('{}'.format(length + 1), end=' ')
        else:
            print(' {:<2}'.format(length + 1), end='')
    print()
    for row in range(connectfour.rows(game)):
        for column in range(connectfour.columns(game)):
            if game.board[column][row] == 0:
                symbol = '.'
            elif game.board[column][row] == 1:
                symbol = 'R'
            else:
                if game.board[column][row] == 2:
                    symbol = 'Y'
            print(' {} '.format(symbol), end='')
        print()
    print()

def pick_a_column(game: tuple, drop_or_pop: str) -> None:
    """
    This module handles asking the user to choose a
    column to either drop or pop their piece and
    handles an errors that may arise.
    """
    while True:
        try:
            move = int(input('Enter a column to {} your piece:\n'.format(drop_or_pop)))
            if move <= connectfour.columns(game) and move > 0:
                if drop_or_pop == 'drop':
                    game = connectfour.drop(game, move-1)
                else:
                    game = connectfour.pop(game, move-1)
                return move, game
                break
            else:
                print('Sorry, I didn\'t get that. Try again.\n')
        except ValueError:
            print('Not a number. Try again.')

def win(message: str) -> None:
    """
    Handles the winning for either game
    version. It mostly just prints as
    the actual win detection is different
    in each version.
    """
    message_parts = message.split('_')
    if message_parts[1] == 'RED' or message_parts[1] == '1':
        print('RED WINS!!! GREAT GAME EVERYONE.')
    elif message_parts[1] == 'YELLOW' or message_parts[1] == '2':
        print('YELLOW WINS!!! GREAT GAME EVERYONE.')
    else:
        if message_parts[1] != '0':
            print('----- GAME ENDED -----')
