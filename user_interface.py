# Madeline Clausen
# 60633236
from collections import namedtuple
import both_interfaces
import connectfour
        
def run() -> None:
    """
    Main function for the game. Pulls all of the components
    together. The main roles it handles are checking for a
    winner and accepting an input of either drop, pop, or quit. 
    """
    game = both_interfaces.setup()
    both_interfaces.print_board(game)
    while True:
        both_interfaces.print_whose_turn(game)
        drop_or_pop = input('Would you like to drop or pop? (Enter \'q\' to end game)\n')
        try:
            if drop_or_pop.lower() in ('drop', 'pop'):
                move, game = both_interfaces.pick_a_column(game, drop_or_pop.lower())
                both_interfaces.print_board(game)
            elif drop_or_pop.lower() == 'q':
                both_interfaces.win('0_' + drop_or_pop.lower())
                break
            else:
                print('Sorry, I didn\'t get that. Try again.\n')
        except connectfour.InvalidMoveError:
            print('Invalid move. Try again.\n')
        both_interfaces.win('0_' + str(connectfour.winner(game)))
        if connectfour.winner(game) in (1, 2):
            break

if __name__ == '__main__':
    run()
