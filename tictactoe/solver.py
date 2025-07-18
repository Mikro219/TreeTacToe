from engine import GameState
from collections import deque


def get_successors(state: GameState) -> list[GameState]:
    """

    """
    successors = []

    for move in state.get_valid_moves():
        gs = state.copy()
        gs.make_move(move)
        successors.append(gs)

    return successors


def create_game_tree(n: int, m: int, k: int) -> (dict[GameState: list[GameState]], dict[GameState: list[GameState]], list[GameState], GameState):
    """
    Note: add storing leaves and returning
    """
    a_list_td = {}
    a_list_bu = {}
    leaves = []
    queue = deque()
    empty_board = GameState(n, m, k)
    queue.append(empty_board)

    while queue:
        gs = queue.popleft()

        if gs not in leaves and gs.check_winner():
            leaves.append(gs)

        if gs in a_list_td:
            continue

        if gs.check_winner():
            a_list_td[gs] = []
            continue

        a_list_td[gs] = get_successors(gs)

        for next_gs in a_list_td[gs]:
            queue.append(next_gs)

            if next_gs in a_list_bu:
                continue

            a_list_bu.setdefault(next_gs, []).append(gs)

    return a_list_td, a_list_bu, leaves, empty_board


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

a_list_td, a_list_bu, leaves, empty_board = create_game_tree(3, 3, 3)

# for n_state in a_list_td:
#     print("======================== vertex ============================")
#     print_board(n_state.board)
#     print(f"winner: {n_state.get_winner()}")
#     print("=================== vertex successors ======================")
#     for s_state in a_list_td[n_state]:
#         print_board(s_state.board)
#         print("=============================================================")
#     print("")

def label_winners(a_list_td: dict[GameState: list[GameState]], a_list_bu: dict[GameState: list[GameState]], leaves: list[GameState]):
    """
    Bottom-up approach of labelling board winners
    """

    # Create queue
    queue = deque()
    for leaf in leaves:
        for parent in a_list_bu[leaf]:
            queue.append(parent)

    while queue:
        gs = queue.popleft()

        # check the children of the parent to determine winner
        for child in a_list_td[gs]:
            if child.get_winner() == gs.player_turn:
                gs.winner = gs.player_turn
                break
        if gs.get_winner() == 0:
            gs.winner = 2 if gs.player_turn == 1 else 1

        if gs not in a_list_bu:
            continue

        for parent in a_list_bu[gs]:
            queue.append(parent)

def get_board_winner(empty_board: GameState) -> int:
    """
    Returns the board winner
    """
    return empty_board.winner

label_winners(a_list_td, a_list_bu, leaves)

print(get_board_winner(empty_board))