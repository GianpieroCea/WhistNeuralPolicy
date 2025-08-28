from itertools import product

from enum import IntEnum
from dataclasses import dataclass
from typing import List,TypeAlias,Optional,cast,Set



class Suit(IntEnum):
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
                raise ValueError(f'The string: {suit} does not represent a valid card suit')
            



class Value(IntEnum):
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

    @staticmethod
    def from_str(value : str) -> 'Value':
        if value.isdigit():
            return Value(int(value))
        else:
            match value:
                case 'J':
                    return Value.JACK
                case 'Q':
                    return Value.QUEEN
                case 'K':
                    return Value.KING
                case 'A':
                    return Value.ACE
                case _:
                    raise ValueError("The str: {str} does not represent a valid card value")
                

    def __lt__(self, other : 'Value') -> bool:
        return self.value < other.value






@dataclass(frozen=True)
class Card:
    suit : Suit
    value : Value

    def __repr__(self) -> str:
        return self.suit.__repr__()+self.value.__repr__()
    
    @staticmethod
    def from_str(card :str) -> 'Card':
        return Card(suit=Suit.from_str(card[:1]), value=Value.from_str(card[1:]))
    

    def __lt__(self, other : 'Card'):
        return self.suit <= other.suit and self.value <= other.value


@dataclass
class Trick:
    lead_card : Optional[Card]
    follow_card : Optional[Card]



DECK : List[Card] = [Card(*tup) for tup in product(Suit,Value)]

print(DECK)

Deal : TypeAlias = List[Card] # a deal of cards, ordered in lexicograhic order
Player: TypeAlias = int  # 0 or 1
