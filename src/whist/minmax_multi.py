# code to implemet alpha-beta pruning for mix-max
# which we will use to generate a dataset to learn a neural policy
from src.whist.game import WhistGame,Card
import numpy as np
from typing import Optional,List

def heuristic(game_state : WhistGame) -> int:
    print('heuristic called') 
    player_zero_wins = len([rec[2] for rec in game_state.trick_history if rec[2] == 0])
    player_one_wins = len([rec[2] for rec in game_state.trick_history if rec[2] == 1])
    print(f"wins: {player_zero_wins}, {player_one_wins}")
    return player_zero_wins - player_one_wins

def minmax_multi(game_state : WhistGame, depth :int, alpha : int, beta: int, target_player : int) -> tuple[int,Optional[Card]]:
    """Implements minmax with alpha-beta pruning

    Args:
        game_state (WhistGame): The current state of the game
        depth (int): how deep to run before static evaluation
        alpha (int): The alpha parameter
        beta (int): The beta parameter
        target_player (int): Which player does the heuristic favours

    Returns:
        tuple[int,Optional[Card]]: A pair, the value of the state and the best card to play from this state.None if 
        game is finished.
    """
    if depth == 0 or game_state.is_finished:
        print('heurstic called, depth:',depth,' and game state finished:',game_state.is_finished)
        return heuristic(game_state), None

    # print(sorted(game_state.player_hands[0]),sorted(game_state.player_hands[1]))
    # print(game_state.current_trick)
    print('hist:',game_state.trick_history)
    print('currhand:',game_state.current_hand)
    print('depth:',depth)
    print('curr_trick:',game_state.current_trick)
    print('#'*20)

    maximizingPlayer = (game_state.current_player == target_player)
    if maximizingPlayer:
        best_value : int = -np.inf
        best_cards : List[Card] = []
        
        for next_move in WhistGame.legal_moves(game_state.current_hand, game_state.current_trick.lead_card.suit if game_state.current_trick else None):
            next_state = WhistGame.apply_move(game_state, next_move)
            current_value, _ = minmax_multi(next_state, depth-1, alpha, beta, target_player )

            if current_value > best_value:
                best_value = current_value
                best_cards = [next_move]
            elif current_value == best_value:
                best_cards.append(next_move)

            if best_value >= beta:
                break
            alpha = max(alpha, best_value)
        return best_value, best_cards
    else:
        best_value : int = np.inf
        best_cards : List[Card] = []

        for next_move in WhistGame.legal_moves(game_state.current_hand, game_state.current_trick.lead_card.suit if game_state.current_trick else None):
            next_state = WhistGame.apply_move(game_state, next_move)
            current_value, _ = minmax_multi(next_state, depth-1, alpha, beta, target_player)

            if current_value < best_value:
                best_value = current_value
                best_cards = [next_move]
            elif current_value == best_value:
                best_cards.append(next_move)

            if best_value <= alpha:
                break
            beta = min(beta, best_value)
        return best_value, best_cards
        