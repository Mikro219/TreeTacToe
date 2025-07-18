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


def create_game_tree(n: int, m: int, k: int) -> dict[GameState: list[GameState]]:
    """

    """
    a_list = {}
    queue = deque()
    queue.append(GameState(n, m, k))

    while queue:
        gs = queue.popleft()

        if gs in a_list:
            continue

        if gs.check_winner():
            a_list[gs] = []
            continue

        a_list[gs] = get_successors(gs)

        for next_gs in a_list[gs]:
            queue.append(next_gs)

    return a_list


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


graph = create_game_tree(3, 3, 3)

for n_state in graph:
    print("======================== vertex ============================")
    print_board(n_state.board)
    print(f"winner: {n_state.get_winner()}")
    print("=================== vertex successors ======================")
    for s_state in graph[n_state]:
        print_board(s_state.board)
        print("=============================================================")
    print("")