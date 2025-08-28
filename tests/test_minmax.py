from src.whist.game import WhistGame,Card
from src.whist.minmax_multi import minmax_multi 
from src.whist.minmax import minmax
import numpy as np

def test_alphabetaminmax_multi(whist : WhistGame) -> None:
    best_moves = []
    whist.player_hands[0] = sorted(list(Card.from_str(card) for card in 'CJ,CQ,D6,HJ,HK'.split(',')))
    whist.player_hands[1] = sorted(list(Card.from_str(card) for card in 'CK,CA,C8,SJ,HA'.split(',')))
    while(not whist.is_finished):
        val,moves = minmax_multi(whist,10,-np.inf,np.inf,0)
        best_moves.append(moves[0])        
        whist = WhistGame.apply_move(whist,moves[0])
    print(val)
    print(best_moves)
    assert best_moves == list(map(lambda x: Card.from_str(x),["♦6", "♣8", "♣J", "♣K", "♣A", "♣Q", "♠J", "♥J", "♥A", "♥K"]))


def test_alphabetaminmax(whist : WhistGame) -> None:

    whist.player_hands[0] = sorted(list(Card.from_str(card) for card in 'CJ,CQ,D6,HJ,HK'.split(',')))
    whist.player_hands[1] = sorted(list(Card.from_str(card) for card in 'CK,CA,C8,SJ,HA'.split(',')))
 
    while not whist.is_finished:
        val,card = minmax(whist,26,-np.inf,np.inf,0) 
        print(f"The cards chosen by player {whist.current_player} is {card}")
        whist = WhistGame.apply_move(whist,card)

    print(val)

def test_alphabetaminmax2(whist : WhistGame) -> None:

    whist.deal(size=6)
 
    while not whist.is_finished:
        val,card = minmax(whist,26,-np.inf,np.inf,0) 
        print(f"The cards chosen by player {whist.current_player} is {card}")
        whist = WhistGame.apply_move(whist,card)

    print(val)
