from itertools import product
from typing import Tuple
from enum import StrEnum,Enum
from dataclasses import dataclass
from typing import List,TypeAlias,Optional,cast,Set
from random import shuffle


class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3


    def __repr__(self) -> str:
        match self.name:
            case 'CLUBS':
                return '♣'
            case 'DIAMONDS':
                return '♦'
            case 'HEARTS':
                return '♥'
            case 'SPADES':
                return '♠'
            case _:
                raise ValueError('Unrecongised suit')
            
    @staticmethod
    def from_str(suit : str) -> 'Suit':
        match suit:
            case 'C' | '♣':
                return Suit.CLUBS
            case 'D' | '♦':
                return Suit.DIAMONDS
            case 'H' | '♥':
                return Suit.HEARTS
            case 'S' | '♠':
                return Suit.SPADES
            case _:
                raise ValueError(f'Cannot parsea a valid suit from string: {suit} ')


class Value(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4 
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __repr__(self) -> str:
        match self.name:
            case 'TWO':
                return '2'
            case 'THREE':
                return '3'
            case 'FOUR':
                return '4'
            case 'FIVE':
                return '5'
            case 'SIX':
                return '6'
            case 'SEVEN':
                return '7'
            case 'EIGHT':
                return '8'
            case 'NINE':
                return '9'
            case 'TEN':
                return '10'
            case 'JACK':
                return 'J'
            case 'QUEEN':
                return 'Q'
            case 'KING':
                return 'K'
            case 'ACE':
                return 'A'
            case _:
                raise ValueError('Unrecongised suit')

    def __lt__(self, other : 'Value') -> bool:
        return self.value < other.value






@dataclass(frozen=True)
class Card:
    suit : Suit
    value : Value

    def __repr__(self) -> str:
        return self.suit.__repr__()+self.value.__repr__()


@dataclass
class Trick:
    lead_card : Optional[Card]
    follow_card : Optional[Card]



DECK : List[Card] = [Card(*tup) for tup in product(Suit,Value)]

print(DECK)

Deal : TypeAlias = Set[Card]
Player: TypeAlias = int  # 0 or 1


class WhistGame:
    def __init__(self, player_hands : List[Deal] = [set(),set()], trick_history : List[tuple[Card,Card,Player]] = [], current_player : Player = 0, deck : Deal = DECK, trump_suit : Optional[type['Suit']] = None):
        self.player_hands : List[Deal] = player_hands
        self.trick_history: List[tuple[Card,Card,Player]] = trick_history  #(lead,follow,winner)
        self.current_player: Player = current_player
        self.trump_suit : Optional[type['Suit']] = trump_suit
        self.current_trick : Optional[Trick] = None
        self.deck : List[Card] = DECK

    

    @property
    def current_hand(self) -> Deal:
        return self.player_hands[self.current_player]
    
    def deal(self) -> None:
        shuffle(self.deck)
        self.player_hands[0] = set(self.deck[:13])
        self.player_hands[1] = set(self.deck[13:26])

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
        
        same_suit = {card for card in hand if card.suit == lead_suit}

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
      




    
    def apply_move(self , card: Card) -> None:
        """_summary_

        Args:
            card (Card): The card played by current player

        """
        if self.current_trick is None:
            self.current_trick = Trick(None,None)

        self.player_hands[self.current_player].remove(card)

        if self.current_trick.lead_card is None:
            self.current_trick.lead_card = card
            self.current_player = 1 - self.current_player
        else:
            # current plyer is the follow
            self.current_trick.follow_card = card

            trick_winner : str = self.determine_winner(self.current_trick,self.trump_suit)

            if trick_winner == 'lead':
                # lost
                winner = 1 - self.current_player
            else:
                #won
                winner = self.current_player
            self.current_player = winner # the turn passes to whoever won the trick
            self.trick_history.append((self.current_trick.lead_card, self.current_trick.follow_card,winner))
            self.current_trick = None








    


    

