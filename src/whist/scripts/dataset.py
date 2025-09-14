# generate all the possible game states of MicroWhist
from whist.models.model import Card
from whist.game import WhistGame
from whist.minmax import minmax
import numpy as np
from typing import List,Tuple
from pathlib import Path
from itertools import combinations
import os

MICRO_DECK = map(Card.from_str, 'CK,CA,DK,DA,HQ,HK,HA,SQ,SK,SA'.split(','))

# list all possible starting hands
all_start_hands = [(list(deal), list(set(MICRO_DECK).difference(set(deal))))
                    for deal in list(combinations(MICRO_DECK, 5))]



data = []


def solve_game(whist : WhistGame) -> Tuple:
    history = []
    moves = []

    while not whist.is_finished:
        st = whist.encode_state()
        _, card = minmax(whist, 26 , -np.inf, np.inf, 0) 
        print(f"The cards chosen by player {whist.current_player} is {card}")
        whist = WhistGame.apply_move(whist, card)
        history.append(st)
        moves.append(card)
    st = whist.encode_state()
    history.append(st)
    moves.append(card)
    return moves, history


class GenerateDataset:
    """Class to create a dataset of optimal plays for Whist based on
    """
    def __init__(self, num_samples : int, batch_size: int, output_dir : str, deck : List[Card] = List(MICRO_DECK)):
        self.num_samples = num_samples
        self.batch_size = batch_size
        self.output_dir = Path(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        self.deck = deck

        
        for _ in range(num_samples):
            for starting_deal in all_start_hands:
                whist = WhistGame(deck=deck,player_hands=list(starting_deal))
                while not whist.is_finished:
                    st = whist.encode_state()
                    _, card = minmax(whist, 26 , -np.inf, np.inf, 0) 
                    print(f"The cards chosen by player {whist.current_player} is {card}")
                    whist = WhistGame.apply_move(whist, card)
                    history.append(st)
                    moves.append(card)
