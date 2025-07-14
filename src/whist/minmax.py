# code to implemet alpha-beta pruning for mix-max
# which we will use to generate a dataset to learn a neural policy
from src.whist.game import WhistGame,Card
import numpy as np


def heuristic(game_state : WhistGame) -> int:
    print('heuristic called') 
    player_zero_wins = len([rec[2] for rec in game_state.trick_history if rec[2] == 0])
    player_one_wins = len([rec[2] for rec in game_state.trick_history if rec[2] == 1])
    print(f"wins: {player_zero_wins}, {player_one_wins}")
    return player_zero_wins - player_one_wins

def minmax(game_state : WhistGame, depth :int, alpha : int, beta: int, maximizingPlayer : bool) -> int:
    if depth == 0 or game_state.is_finished:
        return heuristic(game_state)

    print(game_state.player_hands)
    print(game_state.current_trick)

    if maximizingPlayer:
        value = -np.inf
        for next_move in WhistGame.legal_moves(game_state.current_hand, game_state.current_trick.lead_card if game_state.current_trick else None):
            next_state = WhistGame.apply_move(game_state,next_move)
            newMaximizingPlayer = maximizingPlayer if game_state.current_player == next_state.current_player else (not maximizingPlayer)
            value = max(value, minmax(next_state,depth-1,alpha,beta,newMaximizingPlayer))
            if value >= beta:
                break
            alpha = max(alpha,value)
        return value
    else:
        value = np.inf
        for next_move in WhistGame.legal_moves(game_state.current_hand, game_state.current_trick.lead_card if game_state.current_trick else None):
            next_state = WhistGame.apply_move(game_state,next_move)
            newMaximizingPlayer = maximizingPlayer if game_state.current_player == next_state.current_player else (not maximizingPlayer)
            value = min(value,minmax(next_state,depth-1,alpha,beta,newMaximizingPlayer))
            if value <= alpha:
                break
            beta = min(beta,value)
        return value
        

        
 
    
    


if __name__ == "__main__":
    whist = WhistGame()
    whist.player_hands[0] = set(Card.from_str(card) for card in 'CQ,CA,D6,HJ,HK'.split(','))
    whist.player_hands[1] = set(Card.from_str(card) for card in 'CK,CJ,C8,SJ,HA'.split(','))
   