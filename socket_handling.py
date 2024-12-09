# Madeline Clausen
# 60633236
from collections import namedtuple
import socket

GameConnection = namedtuple('GameConnection', ['socket', 'input', 'output'])

class GameProtocolError(Exception):
    """
    During the "setup" of the network,
    if the server can't run through the
    hello sequence and get a READY response,
    then a GameProtocolError is raised.
    """
    pass

def connect(host: str, port: int) -> GameConnection:
    """
    Given a host and port, a connection
    is attempted. Input and output is setup.
    """
    game_socket = socket.socket()
    game_socket.connect((host, port))
    game_input = game_socket.makefile('r')
    game_output = game_socket.makefile('w')
        
    return GameConnection(
    socket = game_socket,
    input = game_input,
    output = game_output)

    

def hello(connection: GameConnection, username: str) -> bool:
    """
    After a connection is given, the hello
    sequence will start writing to the protocol.
    This function also ensures that the server
    responds back correctly.
    """

    write_line(connection, f'I32CFSP_HELLO {username}')

    response = read_line(connection)
    if response.startswith('WELCOME'):
        return True

def end(connection: GameConnection) -> None:
    """
    The end function closes all the server
    connections.
    """
    connection.input.close()
    connection.output.close()
    connection.socket.close()

def read_line(connection: GameConnection) -> str:
    """
    Returns what the server said. It reads
    a line from it.
    """
    line = connection.input.readline()[:-1]
    return line

def write_line(connection: GameConnection, line: str) -> None:
    """
    Takes a client command and sends it
    to the server.
    """
    connection.output.write(line + '\r\n')
    connection.output.flush()
