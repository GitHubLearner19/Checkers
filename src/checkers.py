"""
Checkers game
"""

import re
import minimax
import time

# Checkers class

class Checkers:
    DEFAULTPIECES = [
        ' r r r r', 
        'r r r r ', 
        ' r r r r',
        '        ',
        '        ',
        'b b b b ',
        ' b b b b',
        'b b b b '
    ]
    DEFAULTTURN = 'b'

    def __init__(self, pieces=DEFAULTPIECES, turn=DEFAULTTURN):
        self.pieces = []
        for linenum in range(8):
            self.pieces.append(list(pieces[linenum]))
        self.turn = turn
    
    def notation_to_coords(self, notation):
        """
        converts move as string to move as tuple (returns empty tuple if there is an error)
        """
        letters = 'abcdefgh'
        nums = '12345678'
        move = []
        count = 0

        while count + 1 < len(notation):
            if notation[count] in letters and notation[count + 1] in nums:
                move.append((letters.index(notation[count]), nums.index(notation[count + 1])))
                count += 3
            else:
                move = []
                break
        
        return tuple(move)

    def copy(self):
        return Checkers(self.pieces[:], self.turn)
    
    def make_move(self, move, log=False):
        """
        applies a move to the board and prints along the way if log=True
        """
        count = 0
        if log: print("moving...\n")
        piecetype = self.pieces[move[0][0]][move[0][1]]
        while count + 2 <= len(move):
            self.pieces[move[count][0]][move[count][1]] = ' '
            if abs(move[count + 1][0] - move[count][0]) == 2:
                jumpedpiece = ((move[count][0] + move[count + 1][0]) // 2, (move[count][1] + move[count + 1][1]) // 2)
                self.pieces[jumpedpiece[0]][jumpedpiece[1]] = ' '
            if move[count + 1][0] == 0 or move[count + 1][0] == 7:
                piecetype = piecetype.upper()
            self.pieces[move[count + 1][0]][move[count + 1][1]] = piecetype
            if log:
                self.print_board()
            count += 1

        if log:
            print("move completed\n")

        self.turn = self.opposite(self.turn)

    def get_piece_squares(self, piecetype):
        """
        returns a list of all of the squares with pieces (piece_type=raw string)
        """
        squares = []
        piecesstr = ''
        for linenum in range(8):
            piecesstr += ''.join(self.pieces[linenum])
        selectedpieces = re.finditer(piecetype, piecesstr)
        for piece in selectedpieces:
            index = piece.start()
            squares.append((index // 8, index % 8))
        return squares
    
    def opposite(self, piecetype):
        return 'b' if piecetype == 'r' else 'r'

    def get_jumps(self, square, piecetype):
        """
        returns all of the jumps from a specific square
        """
        jumps = []

        dir = -1 if piecetype.lower() == 'b' else 1
        startrow = (square[0] - 2 * dir) if piecetype.isupper() else (square[0] + 2 * dir)

        def append_jumps(finalsquare):
            """
            appends all of jumps along the path including 'finalsquare' to 'jumps' list
            """
            nextboard = self.copy()
            nextboard.make_move((square, finalsquare))
            nextboard.turn = self.opposite(nextboard.turn)
            nextjumps = nextboard.get_jumps(finalsquare, piecetype)
            if len(nextjumps) == 0: 
                jumps.append((square, finalsquare))
            else:
                for jump in nextjumps:
                    jumps.append((square, finalsquare) + jump[1:])

        for jumprow in range(startrow, square[0] + 3 * dir, 4 * dir):
            if jumprow >= 0 and jumprow < 8:
                middlerow = (jumprow + square[0]) // 2
                if square[1] - 2 >= 0 and self.pieces[middlerow][square[1] - 1].lower() == self.opposite(self.turn) and self.pieces[jumprow][square[1] - 2] == ' ':
                    finalsquare = (jumprow, square[1] - 2)
                    append_jumps(finalsquare)
                if square[1] + 2 < 8 and self.pieces[middlerow][square[1] + 1].lower() == self.opposite(self.turn) and self.pieces[jumprow][square[1] + 2] == ' ':
                    finalsquare = (jumprow, square[1] + 2)
                    append_jumps(finalsquare)
                    

        return jumps
    
    def get_moves(self):
        """
        returns list of moves in the form of a tuple of tuples where the first tuple is the start square and the last tuple is the end square
        e.g. ((1, 0), (2, 1))
        """
        pawns = []
        kings = []

        if self.turn == 'r':
            pawns = self.get_piece_squares(r'r')
            kings = self.get_piece_squares(r'R')
        else:
            pawns = self.get_piece_squares(r'b')
            kings = self.get_piece_squares(r'B')

        dir = -1 if self.turn == 'b' else 1
        moves = []

        # get jump moves

        for square in pawns:
            moves += self.get_jumps(square, self.turn)
        
        for square in kings:
            moves += self.get_jumps(square, self.turn.upper())

        # get sliding (normal) moves

        if len(moves) == 0:
            for square in pawns:
                sliderow = square[0] + dir
                if sliderow >= 0 and sliderow < 8:
                    if square[1] - 1 >= 0 and self.pieces[sliderow][square[1] - 1] == ' ':
                        moves.append((square, (sliderow, square[1] - 1)))
                    if square[1] + 1 < 8 and self.pieces[sliderow][square[1] + 1] == ' ':
                        moves.append((square, (sliderow, square[1] + 1)))

            for square in kings:
                for sliderow in range(square[0] - dir, square[0] + 2 * dir, 2 * dir):
                    if sliderow >= 0 and sliderow < 8:
                        if square[1] - 1 >= 0 and self.pieces[sliderow][square[1] - 1] == ' ':
                            moves.append((square, (sliderow, square[1] - 1)))
                        if square[1] + 1 < 8 and self.pieces[sliderow][square[1] + 1] == ' ':
                            moves.append((square, (sliderow, square[1] + 1)))

        return moves

    def game_over(self):
        return len(self.get_moves()) == 0

    def print_board(self):
        """
        prints board so that it faces the current player
        """
        notation = 'abcdefgh'
        if self.turn == 'b':
            print('  1 2 3 4 5 6 7 8')
            for linenum in range(8): 
                print(notation[linenum], end='')
                for c in self.pieces[linenum]:
                    print('|' + c, end='')
                print('|')
        else:
            print('  8 7 6 5 4 3 2 1')
            for linenum in range(7, -1, -1):
                print(notation[linenum], end='')
                for index in range(7, -1, -1):
                    print("|" + self.pieces[linenum][index], end='')
                print('|')
        print()



def main():
    checkers = Checkers()
    print()
    checkers.print_board()
    print('Enter moves in the form [row1][column1]-[row2][column2]-... for each square the checker lands (e.g. \'f1-d3-b5\' for double jump)\n')
    
    while not checkers.game_over():
        move = checkers.notation_to_coords(input('Move: '))
        if move in checkers.get_moves():
            checkers.make_move(move, log=True)
            checkers.print_board()
            print('Calculating...')
            time.sleep(1)
            print('...')
            time.sleep(1)
            print('...')
            time.sleep(1)
            print('...')
            time.sleep(1)
            checkers.make_move(minimax.best_move(checkers, 4), log=True)
        else:
            print('Invalid input. Try again\n')
        
        checkers.print_board()

    print('Game Over')



if __name__ == '__main__':
  main()

