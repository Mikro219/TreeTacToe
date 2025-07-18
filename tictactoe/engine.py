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
    moves_remaining: int    # available moves remaining
    num_of_pieces: int      # number of pieces on the board (used for backtracking later)

    def __init__(self, n: int, m: int, k: int):
        self.board = [[0 for _ in range(m)] for _ in range(n)]
        self.rows = n
        self.columns = m
        self.win_condition = k
        self.winner = 0
        self.player_turn = 1
        self.moves_remaining = n * m
        self.num_of_pieces = 0

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return self.board == other.board and self.player_turn == other.player_turn

    def __hash__(self):
        board_tuple = tuple(tuple(row) for row in self.board)
        return hash((board_tuple, self.player_turn))

    def get_valid_moves(self) -> list[Move]:
        """
        Return all valid moves for the board
        """
        moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == 0:
                    moves.append(Move(i, j, self.player_turn))
        return moves

    def make_move(self, move: Move) -> bool:
        """
        Make a valid move on the board
        """
        if move.row < 0 or move.row >= self.rows:
            return False

        if move.col < 0 or move.col >= self.columns:
            return False

        if self.board[move.row][move.col] != 0:
            return False

        self.board[move.row][move.col] = self.player_turn
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.moves_remaining -= 1
        self.num_of_pieces += 1

        return True

    def is_terminal(self) -> bool:
        """
        Return True if the game is over, False otherwise
        """
        return self.winner != 0

    def get_winner(self) -> int:
        """
        Returns which player won the game
        """
        return self.winner

    def check_winner(self) -> bool:
        """
        Checks if anyone won the game
        Will modify self.winner if someone did win
        """
        if self.check_rows() or self.check_cols() or self.check_diagonals():
            return True

        if not self.moves_remaining:
            self.winner = 2
            return True

        return False

    def check_consecutive(self, direction: str, row: int, col: int) -> bool:
        """
        Checks if player <player> has k consecutive pieces in <direction> at (row, col)
        """
        if direction == "row":
            for i in range(self.win_condition):
                if self.board[row][col] != self.board[row][col + i]:
                    return False

        elif direction == "column":
            for i in range(self.win_condition):
                if self.board[row][col] != self.board[row + i][col]:
                    return False

        elif direction == "diagonal-lr":
            for i in range(self.win_condition):
                if self.board[row][col] != self.board[row + i][col + i]:
                    return False

        elif direction == "diagonal-rl":
            for i in range(self.win_condition):
                if self.board[row][col] != self.board[row + i][col - i]:
                    return False

        return True

    def check_rows(self) -> bool:
        """
        Checks all rows to see if there is a winner
        """
        for i in range(self.rows):
            for j in range(self.columns-self.win_condition+1):
                if self.board[i][j] != 0 and self.check_consecutive("row", i, j):
                    self.winner = self.board[i][j]
                    return True
        return False

    def check_cols(self) -> bool:
        """
        Checks all cols to see if there is a winner
        """
        for i in range(self.columns):
            for j in range(self.rows-self.win_condition+1):
                if self.board[j][i] != 0 and self.check_consecutive("column", j, i):
                    self.winner = self.board[j][i]
                    return True
        return False

    def check_diagonals(self) -> bool:
        """
        Checks all diagonals to see if there is a winner
        """
        # left-to-right diagonals
        for i in range(self.rows-self.win_condition+1):
            for j in range(self.columns-self.win_condition+1):
                if self.board[i][j] != 0 and self.check_consecutive("diagonal-lr", i, j):
                    self.winner = self.board[i][j]
                    return True

        # right-to-left diagonals
        for i in range(self.rows-self.win_condition+1):
            for j in range(self.win_condition-1, self.columns):
                if self.board[i][j] != 0 and self.check_consecutive("diagonal-rl", i, j):
                    self.winner = self.board[i][j]
                    return True

        return False

    def copy(self) -> 'GameState':
        """
        Make a copy of the board
        """
        gs = GameState(self.rows, self.columns, self.win_condition)
        gs.board = [row[:] for row in self.board] # deep copy of board
        gs.winner = self.winner
        gs.player_turn = self.player_turn
        gs.moves_remaining = self.moves_remaining
        gs.num_of_pieces = self.num_of_pieces
        return gs