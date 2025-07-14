from src.whist.game import WhistGame,Card
from src.whist.minmax import minmax 
import numpy as np

def test_hello(whist : WhistGame) -> None:
    whist.player_hands[0] = set(Card.from_str(card) for card in 'C2,C3,D6,HJ,HK'.split(','))
    whist.player_hands[1] = set(Card.from_str(card) for card in 'CK,CJ,C8,SJ,HA'.split(','))
    val = minmax(whist,10,-np.inf,np.inf,True)
    print(val)
