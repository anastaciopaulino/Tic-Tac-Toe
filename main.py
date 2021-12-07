import socket 
import threading
from typing import Counter

class TicTacToe():

    def __init__(self):
        self.board = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winer = None
        self.game_over = False

        self.counter = 0
    
    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(host, port)
        server.listen(1)

        client, addr = server.accept()

        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client, )).start()
        server.close()
    
    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'O'
        self.opponent = 'O'

        threading.Thread(target=self.handle_connection, args=(client, )).start()

    def handle_connection(self, client):
        while not self.game_over:
            if self.turn == self.you:
                move = input('Enter a move (row, colum): ')
                if self.check_valid_move(move.split(',')):
                    self.apply_move(move.split(','), self.you)
                    self.turn = self.opponent
                    client.send(move.encode('utf-8'))

                else:
                    print("Invalid move!")
            
            else:

                data = cliente.recv(1024)
                if not data:
                    break
                
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
        client.close()
    
    def apply_move(self, move, player):
        if self.game_over:
            return
        
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()

        if self.check_if_won():
            if self.winner == self.you:
                print('You win!')
                exit()
            
            elif self.winner == self.opponent:
                print('You lose!')
                exit()
        
        else:
            if self.counter == 9:
                print('It is tie')
                exit()