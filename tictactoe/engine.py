"""
This class is responsible for storing all the information about the current state of a tic-tac-toe game. It will also
be responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class Move:

    row: int     # row of the move
    col: int     # column of the move
    player: int  # 1 for player1, and 2 for player2

    def __init__(self, row: int, col: int, player: int):
        self.row = row
        self.col = col
        self.player = player


class GameState:

    board: list[list[int]]  # current tic-tac-toe board
    rows: int               # number of rows
    columns: int            # number of columns
    win_condition: int      # needed length to win
    winner: int             # the winner of the game
    is_player1_turn: bool   # is it player1's turn?
    move_log = list[Move]   # list of moves from start

    def __init__(self, n: int, m: int, k: int):
        self.board = [[0 for _ in range(m)] for _ in range(n)]
        self.rows = n
        self.columns = m
        self.win_condition = k
        self.winner = 0
        self.is_player1_turn = True
        self.move_log = []

    def get_valid_moves(self) -> list[Move]:
        """

        """
        pass

    def make_move(self, move: Move) -> bool:
        """

        """
        pass

    def is_terminal(self) -> bool:
        """

        """
        pass

    def get_winner(self) -> int:
        """

        """
        pass

    def copy(self) -> 'GameState':
        """

        """
        pass
