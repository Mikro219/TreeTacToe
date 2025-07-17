"""
This class is responsible for storing all the information about the current state of a tic-tac-toe game. It will also
be responsible for determining the valid moves at the current state. It will also keep a move log.
"""

class Move:
    pass

class GameState:

    board: list[list[int]]  # current tic-tac-toe board
    rows: int               # number of rows
    columns: int            # number of columns
    win_condition: int      # needed length to win
    is_terminal : bool      # is the game over?
    is_player1_turn: bool   # is it player1's turn?
    move_log = list[Move]   # list of moves from start

    def __init__(self, n: int, m: int, k: int):
        self.board = [[0 for _ in range(m)] for _ in range(n)]
        self.rows = n
        self.columns = m
        self.win_condition = k
        self.is_player1_turn = True
        self.move_log = []

    def get_valid_moves(self):
        pass

    def make_move(self, move: Move):
        pass

    def check_win(self):
        pass