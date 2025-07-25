from engine import GameState

def get_next_moves(state: GameState) -> list[GameState]:
    next_moves = []
    for move in state.get_valid_moves():
        gs = state.copy()
        gs.make_move(move)
        next_moves.append(gs)
        gs.check_and_set_winner()
    return next_moves

def find_winner(gs: GameState, memo=None) -> int:
    # memorization to speed up runtime
    if memo is None:
        memo = {}
    if gs in memo:
        return memo[gs]

    # if winner already calculated, return winner
    if gs.winner != 0:
        memo[gs] = gs.winner
        return gs.winner

    # otherwise, check the children (following game states)
    next_moves = get_next_moves(gs)
    for child in next_moves:
        # if current player has possible winning move, then game state is current player's win
        if find_winner(child, memo) == gs.player_turn:
            gs.winner = gs.player_turn
            memo[gs] = gs.winner
            return gs.winner

    # if current player has no possible winning moves, then it's the other player's win
    gs.winner = 2 if gs.player_turn == 1 else 1
    memo[gs] = gs.winner
    return gs.winner

# This is how to use our code to find the winner of an empty board
board = GameState(4, 4, 4)
print(find_winner(board))