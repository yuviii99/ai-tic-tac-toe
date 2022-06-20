import random

class TicTacToe:
    def __init__(self):
        self.board = []
    
    def create_board(self):
        for i in range(3):
                row = []
                for j in range(3):
                    row.append('-')
                self.board.append(row)
    
    def get_random_first_player(self):
        return random.randint(0, 1)

    def fix_spot(self, row, column, player):
        self.board[row][column] = player

    def is_player_win(self, player):
        win = None

        n = 3

        # check for rows
        for i in range(n):
            win=True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # check for columns
        for i in range(n):
            win=True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win
        
        # check for diagonals
        for i in range(n):
            win = True
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        for i in range(n):
            win = True
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        
        return False

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True
    
    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start(self):
        self.create_board()

        player = 'X' if self.get_random_first_player == 1 else 'O'
        
        while True:
            print(f"Player {player} Turn!")
            self.show_board()

            row, col = list(map( int, input("Enter row and column to fix the spot: ")))
            print()

            self.fix_spot(row-1, col-1, player)

            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            if self.is_board_filled():
                print("Game Draw!")
                break

            player = self.swap_player_turn(player)

        print()
        self.show_board()