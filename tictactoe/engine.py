"""
This class is responsible for storing all the information about the current state of a tic-tac-toe game.
It is also responsible for determining the valid moves at the current state.
"""

DIRECTIONS = {
    "row": (0, 1),
    "col": (1, 0),
    "diag_lr": (1, 1),
    "diag_rl": (1, -1),
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
        return self.board == other.board and self.player_turn == other.player_turn

    def __hash__(self):
        board_tuple = tuple(tuple(row) for row in self.board)
        return hash((board_tuple, self.player_turn))

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