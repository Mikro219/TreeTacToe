from engine import GameState


def get_successors(state: GameState) -> list[GameState]:
    """

    """
    successors = []

    for move in state.get_valid_moves():
        gs = state.copy()
        gs.make_move(move)
        successors.append(gs)

    return successors

def find_winner(gs: GameState) -> int:
    """

    """
    next_moves = get_successors(gs)
    for child in next_moves:
        if not child.check_winner():
            if find_winner(child) == gs.player_turn:
                gs.winner = gs.player_turn
                return gs.winner
        if child.get_winner() == gs.player_turn:
            gs.winner = gs.player_turn
            return gs.winner

    if gs.get_winner() == 0:
        gs.winner = 2 if gs.player_turn == 1 else 1
    return gs.winner

def print_board(board: list[list[int]]) -> None:
    """
    from utils.py
    """
    symbol = {0: " ", 1: "O", 2: "X"}
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    for i in range(rows):
        row_str = " | ".join(symbol[cell] for cell in board[i])
        print(row_str)
        if i < rows - 1:
            print("-" * (4 * cols - 3))  # draws separator line

empty_board = GameState(3, 5, 4)
print(find_winner(empty_board))

# for n_state in a_list_td:
#     print("======================== vertex ============================")
#     print_board(n_state.board)
#     print(f"winner: {n_state.get_winner()}")
#     print("=================== vertex successors ======================")
#     for s_state in a_list_td[n_state]:
#         print_board(s_state.board)
#         print("=============================================================")
#     print("")