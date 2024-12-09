# Madeline Clausen
# 60633236
from collections import namedtuple
import socket_handling
import both_interfaces
import connectfour

def setup() -> tuple:
    """
    Handles the techincal stuff in the setting
    up of the game. Ensures a proper host and
    port are imported, attempts a server
    connection, gives the server the information
    it needs to start a game, including
    columns and rows.
    """
    while True:
        try:
            host = input('Enter a host: \n')
            port = int(input('Enter a port: \n'))
            print('Connecting to server...')
            if host == 'circinus-32.ics.uci.edu' and port == 4444:
                try:
                    game_connection = socket_handling.connect(host, port)
                except ConnectionRefusedError:
                    print('Unable to connect to server. Goodbye.')
                    return 0, 0
                while True:
                    username = input('Username: ')
                    if ' ' not in username:
                        try:
                            socket_handling.hello(game_connection, username)
                        except socket_handling.GameProtocolError:
                            print('Unable to connect. Goodbye.')
                        print('Welcome ' + username + '!')
                        print('You\'ll be red and we\'ll be yellow. Red always goes first!\n')
                        game = both_interfaces.setup()
                        both_interfaces.print_board(game)
                        board_request = 'AI_GAME {} {}'.format(connectfour.columns(game), connectfour.rows(game))
                        socket_handling.write_line(game_connection, board_request)
                        ready_or_not = socket_handling.read_line(game_connection)
                        if ready_or_not == 'READY':
                            return game_connection, game
                        else:
                            print('Not ready.')
                            break
                        
                    else:
                        print('Sorry, that isn\'t a valid username. Try again.')
            else:
                print('Sorry, I don\'t recognize that host and port. Try again.')
        except ValueError:
            print('Sorry, that isn\'t a valid port number. Try again.')
            
def read_server_response(game_connection: tuple, game: tuple) -> tuple:
    """
    The function takes the server's response and
    completes it's "play". The socket version of
    the game still utilizes the connectfour module.
    This function allows the server to interact with
    the game state. It's moves are added to the game
    so that the user can see the board with yellow's
    moves.
    """
    okay = socket_handling.read_line(game_connection)
    if okay == 'OKAY':
        move = socket_handling.read_line(game_connection).split()
        if move[0] == 'DROP':
            game = connectfour.drop(game, int(move[1])-1)
        else:
            game = connectfour.pop(game, int(move[1])-1)
        ready = socket_handling.read_line(game_connection)
        if ready == 'READY':
            return game, move
        else:
            if ready.startswith('WINNER'):
                both_interfaces.win(ready)
                socket_handling.end(game_connection)
                return 0, 0
    elif okay.startswith('WINNER'):
        both_interfaces.win(okay)
        socket_handling.end(game_connection)
        return 0, 0
    else:
        if okay == 'INVALID':
            ready = socket_handling.read_line(game_connection)
            if ready == 'READY':
                return game, okay
    return 0, 0

def run() -> None:
    """
    This is the main code that pulls the various
    functions together. It checks for a drop or
    pop input and reacts accordingly. It has lots
    of tests to capture an erronous input. Mostly,
    however, it deals with the user interface and
    what the client sees. 
    """
    game_over = False
    game_connection, game = setup()
    if game != 0:
        while not game_over:
            both_interfaces.print_whose_turn(game)
            if game.turn == 1: # RED
                while True:
                    drop_or_pop = input('Would you like to drop or pop? (Enter \'q\' to end game)\n')
                    try:
                        if drop_or_pop.lower() == 'drop':
                            move, game = both_interfaces.pick_a_column(game, 'drop')
                            socket_handling.write_line(game_connection, 'DROP {}'.format(move))
                            both_interfaces.print_board(game)
                            break
                        elif drop_or_pop.lower() == 'pop':
                            move, game = both_interfaces.pick_a_column(game, 'pop')
                            socket_handling.write_line(game_connection, 'POP {}'.format(move))
                            both_interfaces.print_board(game)
                            break
                        elif drop_or_pop.lower() == 'q':
                            both_interfaces.win('QUIT_GAME')
                            game_over = True
                            break
                        else:
                            print('Sorry, I didn\'t get that. Try again.\n')
                    except (connectfour.InvalidMoveError, ValueError):
                        print('Invalid move. Try again.\n')
            else: # YELLOW
                game, response = read_server_response(game_connection, game)
                if game == 0:
                    break
                elif response[0] == 'DROP' or response[0] == 'POP':
                    print()
                    print('|-----Server decided to {} at column {}-----|\n'.format(response[0].lower(), response[1]))
                else:
                    if response == 'INVALID':
                        print()
                        print('******Server didn\'t play due to invalid move. Try again.******\n')
                        
                both_interfaces.print_board(game)

if __name__ == '__main__':
    run()
