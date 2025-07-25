"""
This class is responsible for storing all the information about the current state of a tic-tac-toe game.
It is also responsible for determining the valid moves at the current state.
"""

DIRECTIONS = {
    "row": (0, 1),
    "col": (1, 0),
    "diag_main": (1, 1),
    "diag_anti": (1, -1),
}

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
        return self.is_symmetric(other) and self.player_turn == other.player_turn

    def __hash__(self):
        variants = [
            self.board,
            self._rotate_90(),
            self._rotate_180(),
            self._rotate_270(),
            self._reflect_horizontal(),
            self._reflect_vertical(),
            self._reflect_main_diagonal(),
            self._reflect_anti_diagonal()
        ]
        board_tuple = min(tuple(tuple(row) for row in variant) for variant in variants)
        return hash((board_tuple, self.player_turn))

    def is_symmetric(self, other) -> bool:
        """
        Optimization - part of the "Bonus Stuff" mentioned in the programming doc
        Helper function to reduce the number of game states to consider through symmetries

        (e.g. it doesn’t matter if Player 1’s first move is in the top left,
        top right, bottom left, or bottom right corner - they make for equivalent
        games)
        """
        if self.board == other.board:
            return True

        if self._rotate_180() == other.board:
            return True

        if (self._reflect_horizontal() == other.board or
            self._reflect_vertical() == other.board or
            self._reflect_main_diagonal() == other.board or
            self._reflect_anti_diagonal() == other.board):
            return True

        if self.rows == self.columns:
            if (self._rotate_90() == other.board or self._rotate_270() == other.board):
                return True

        return False

    def _rotate_90(self) -> list[list[int]]:
        return [list(col)[::-1] for col in zip(*self.board)]

    def _rotate_180(self) -> list[list[int]]:
        return [row[::-1] for row in self.board[::-1]]

    def _rotate_270(self) -> list[list[int]]:
        return [list(col) for col in zip(*self.board[::-1])]

    def _reflect_horizontal(self) -> list[list[int]]:
        return [row[::-1] for row in self.board]

    def _reflect_vertical(self) -> list[list[int]]:
        return self.board[::-1]

    def _reflect_main_diagonal(self) -> list[list[int]]:
        return [list(row) for row in zip(*self.board)]

    def _reflect_anti_diagonal(self) -> list[list[int]]:
        return [list(row)[::-1] for row in zip(*self.board[::-1])]

    def get_valid_moves(self) -> list[Move]:
        moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == 0:
                    moves.append(Move(i, j, self.player_turn))
        return moves

    def make_move(self, move: Move):
        """
        Precondition: <move> is a valid move on the board
        """
        self.board[move.row][move.col] = self.player_turn
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.moves_remaining -= 1
        self.num_of_pieces += 1

    def check_and_set_winner(self) -> bool:
        """
        Checks if anyone won the game
        Will modify self.winner if someone did win
        """
        for direction in DIRECTIONS.values():
            if self.check_consecutive(direction):
                return True

        if not self.moves_remaining:
            self.winner = 2
            return True

        return False

    def check_consecutive(self, direction: tuple[int, int]) -> bool:
        """
        Checks the board in the given <direction> for a win
        """
        dr, dc = direction
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] != 0 and self.has_k_consecutive(row, col, dr, dc):
                    self.winner = self.board[row][col]
                    return True

        return False

    def has_k_consecutive(self, row: int, col: int, dr: int, dc: int) -> bool:
        """
        Checks if there are k consecutive pieces of the same player's piece,
        starting at (row, col) in direction (dr, dc)
        """
        end_row = row + dr * (self.win_condition - 1)
        end_col = col + dc * (self.win_condition - 1)

        if not (0 <= end_row < self.rows and 0 <= end_col < self.columns):
            return False

        player = self.board[row][col]
        for i in range(1, self.win_condition):
            if self.board[row + dr * i][col + dc * i] != player:
                return False

        return True

    def copy(self) -> 'GameState':
        gs = GameState(self.rows, self.columns, self.win_condition)
        gs.board = [row[:] for row in self.board] # deep copy of board
        gs.winner = self.winner
        gs.player_turn = self.player_turn
        gs.moves_remaining = self.moves_remaining
        gs.num_of_pieces = self.num_of_pieces
        return gs