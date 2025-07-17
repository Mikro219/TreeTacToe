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
    player_turn: int        # the current player turn
    moves_remaining: int         # available moves remaining
    move_log = list[Move]   # list of moves from start

    def __init__(self, n: int, m: int, k: int):
        self.board = [[0 for _ in range(m)] for _ in range(n)]
        self.rows = n
        self.columns = m
        self.win_condition = k
        self.winner = 0
        self.player_turn = 1
        self.moves_remaining = n * m
        self.move_log = []

    def get_valid_moves(self) -> list[Move]:
        """

        """
        moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == 0:
                    moves.append(Move(i, j, self.player_turn))
        return moves

    def make_move(self, move: Move) -> bool:
        """

        """
        if move.row < 0 or move.row >= self.rows:
            return False

        if move.col < 0 or move.col >= self.columns:
            return False

        if self.board[move.row][move.col] != 0:
            return False

        self.board[move.row][move.col] = self.player_turn
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.move_log.append(move)
        self.moves_remaining -= 1

        return True

    def is_terminal(self) -> bool:
        """

        """
        return self.winner != 0

    def get_winner(self) -> int:
        """

        """
        pass

    def copy(self) -> 'GameState':
        """

        """
        pass
