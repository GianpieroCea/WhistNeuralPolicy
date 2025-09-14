from src.whist.models.model import Card,Player,Suit,Trick,DECK,Deal,Value
from typing import Optional,List
from random import shuffle
from copy import deepcopy

import torch


class WhistGame:
    def __init__(self, player_hands : List[Deal] = [list(),list()], trick_history : List[tuple[Card,Card,Player]] = [], current_player : Player = 0, deck : List[Card] = DECK, trump_suit : Optional[Suit] = None):
        self.player_hands : List[Deal] = player_hands
        self.trick_history: List[tuple[Card, Card, Player]] = trick_history  #(lead,follow,winner)
        self.current_player: Player = current_player
        self.trump_suit : Optional[Suit] = trump_suit
        self.current_trick : Optional[Trick] = None
        self.deck : List[Card] = deck
        self.is_finished : bool = False
    
    def __str__(self) -> str:
        return f""""
        
        --------------------------\n

        \t Player 1 Hand: {print(self.player_hands)} - [{"x" if self.current_player == 0 else " "}]
        \t Player 2 Hand: {print(self.player_hands[1])} - [{"x" if self.current_player == 1 else " "}]


        ###
        \t Trick history: {self.trick_history}
        ###
    """

    @property
    def current_hand(self) -> Deal:
        return self.player_hands[self.current_player]
    
    def deal(self, size : int = 13) -> None:
        assert size <= 26
        shuffle(self.deck)
        self.player_hands[0] = sorted(self.deck[:size])
        self.player_hands[1] = sorted(self.deck[size:2*size])

    @staticmethod
    def legal_moves(hand : Deal, lead_suit : Optional[Suit]) -> Deal:
        """Return the legal moves given a lead suit

        Args:
            hand (Deal): The hand dealt
            lead_suit (Suit): The suit lead

        Returns:
            Deal: A filter hand. Note in trck taking if you have any
            cards of the same suit then you need to pick one of those, if 
            not there are no restrictions.
        """
        if lead_suit is None:
            return hand
        
        same_suit = sorted([card for card in hand if card.suit == lead_suit])

        return same_suit if same_suit else hand
    
    @staticmethod
    def _determine_winner_with_trump(trick : Trick, trump_suit : Suit)->str:
        if trick.follow_card.suit != trick.lead_card.suit:
            if trick.follow_card.suit == trump_suit:
                winner = 'follow'
            else:
                winner = 'lead'
        else:
            winner = 'follow' if trick.follow_card.value > trick.lead_card.value else 'lead'
        return winner

    @staticmethod
    def _determine_winner_no_trump(trick : Trick)->str:
        if trick.follow_card.suit != trick.lead_card.suit:
            winner = 'lead'
        else:
            winner = 'follow' if trick.follow_card.value > trick.lead_card.value else 'lead'
        return winner
    
    @staticmethod
    def determine_winner(trick : Trick, trump_suit : Optional[Suit]) -> str:
 
        if trump_suit:
            return WhistGame._determine_winner_with_trump(trick, trump_suit)
        else:
            return WhistGame._determine_winner_no_trump(trick)
    
    def encode_state(self, deck : List[Card]) -> torch.tensor:
        """Returns a numpy array representation of the whist game
        to be used in a nueral network 

        Returns:
            np.array: A unique vector representing the current game state
        """

        # the state will keep track of the following:
        deck_size = len(deck)
        # player zero's hand as multi hot vector - (CARD_DECK,)
        player_zero_cards = torch.zeros(deck_size)
        player_zero_indices = Card.get_indices_for_cards(cards=self.player_hands[0], deck=deck)
        player_zero_cards[player_zero_indices] = 1.0

        # player one's hand as multi hot vector - (CARD_DECK,)
        player_one_cards = torch.zeros(deck_size)
        player_one_indices = Card.get_indices_for_cards(cards=self.player_hands[1], deck=deck)
        player_one_cards[player_one_indices] = 1.0

        # 0/1 flag to represent current player - (1, )
        current_player = torch.array(self.current_player)

        # led card ( 0 vector if  current player leading) (CARD_DECK)
        led_card = torch.zeros(deck_size)
        if self.current_trick.lead_card is not None:
            led_card[Card.get_indices_for_cards(cards=[self.current_trick.lead_card], deck=deck)] = 1.0

        # trump suit (0 if no trump suit ,1,2,3,4 for C,D,H,S) (4)
        trump_suit = torch.zeros(4)
        if self.trump_suit:
            trump_suit[int(self.trump_suit)] = 1.0

        # create the state vecor by concatenating all these pieces together
        state = torch.cat(
            [
                player_zero_cards,
                player_one_cards,
                current_player,
                led_card,
                trump_suit
            ]
        )
        return state






    @staticmethod
    def apply_move(state : 'WhistGame' , card: Card) -> 'WhistGame':
        """_summary_

        Args:
            card (Card): The card played by current player

        """
        new_state = deepcopy(state)
        if new_state.current_trick is None:
            new_state.current_trick = Trick(None,None)


        if new_state.current_trick.lead_card is None:
            new_state.current_trick.lead_card = card
            new_state.player_hands[new_state.current_player].remove(card)
            new_state.current_player = 1 - new_state.current_player
        else:
            # current plyer is the follow
            assert card in WhistGame.legal_moves(new_state.current_hand,new_state.current_trick.lead_card.suit)
            new_state.current_trick.follow_card = card
            new_state.player_hands[new_state.current_player].remove(card)

            trick_winner : str = new_state.determine_winner(new_state.current_trick,new_state.trump_suit)

            if trick_winner == 'lead':
                # lost
                winner = 1 - new_state.current_player
            else:
                #won
                winner = new_state.current_player
            new_state.current_player = winner # the turn passes to whoever won the trick
            new_state.trick_history.append((new_state.current_trick.lead_card, new_state.current_trick.follow_card,winner))
            new_state.current_trick = None

            # check game is finished
            if len(new_state.player_hands[0]) == 0 and len(new_state.player_hands[1]) == 0:
                new_state.is_finished = True
        return new_state

            








    


    

