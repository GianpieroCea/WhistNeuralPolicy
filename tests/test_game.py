from src.whist.game import WhistGame,Value,Suit,Card,Trick
import pytest

@pytest.fixture
def whist():
    whist = WhistGame()
    return whist

def test_deal(whist : WhistGame) -> None:
    print(whist.player_hands)
    print(type(whist.player_hands[0]))
    whist.deal()

    len(whist.deck) == 52
    len(whist.player_hands[0]) == 13
    len(whist.player_hands[1]) == 13
    print(type(whist.player_hands[0]))
    len((whist.player_hands[0]).difference(whist.player_hands[1])) == 0


def test_legal_moves() -> None:
    #TODO parametrize and add more tests
    legal_moves = WhistGame.legal_moves(hand={
        Card(Suit.CLUBS ,Value.EIGHT),
        Card(Suit.CLUBS ,Value.TWO),
        Card(Suit.SPADES ,Value.EIGHT),
        Card(Suit.DIAMONDS ,Value.EIGHT)}, lead_suit=Suit.CLUBS)
    
    assert legal_moves == {Card(Suit.CLUBS, Value.TWO),Card(Suit.CLUBS, Value.EIGHT)}


def test_determine_winner() -> None:
    test_trick = Trick(lead_card=Card(Suit.CLUBS, Value.TWO), follow_card=Card(Suit.CLUBS, Value.EIGHT))
    winner = WhistGame.determine_winner(test_trick,None)
    assert winner == 'follow'


    test_trick = Trick(lead_card=Card(Suit.CLUBS, Value.TWO), follow_card=Card(Suit.DIAMONDS, Value.EIGHT))
    winner = WhistGame.determine_winner(test_trick,None)
    assert winner == 'lead'

    test_trick = Trick(lead_card=Card(Suit.CLUBS, Value.TWO), follow_card=Card(Suit.DIAMONDS, Value.EIGHT))
    winner = WhistGame.determine_winner(test_trick,Suit.DIAMONDS)
    assert winner == 'follow'


    test_trick = Trick(lead_card=Card(Suit.DIAMONDS, Value.TWO), follow_card=Card(Suit.DIAMONDS, Value.EIGHT))
    winner = WhistGame.determine_winner(test_trick,Suit.DIAMONDS)
    assert winner == 'follow'


def test_apply_move(whist : WhistGame) -> None:
    whist.player_hands[0] = set(Card.from_str(card) for card in 'CQ,CA,D6,HJ,HK'.split(','))
    whist.player_hands[1] = set(Card.from_str(card) for card in 'CK,CJ,C8,SJ,HA'.split(','))
    whist.current_player = 0
    new_state = WhistGame.apply_move(whist,Card.from_str('HK'))
    assert new_state.is_finished == False
    assert new_state.current_player == 1
    assert len(new_state.player_hands[0]) == 4
    assert new_state.current_trick == Trick(Card(Suit.HEARTS,Value.KING),None)
    print(new_state.player_hands)
    new_state2 = WhistGame.apply_move(new_state,Card.from_str('HA'))
    assert new_state2.current_player == 1
    assert new_state2.trick_history == [(Card(Suit.HEARTS,Value.KING),Card(Suit.HEARTS,Value.ACE),1)]


    
    
# Objects classes, Suit,Value ,Card


def test_from_str_card() -> None:
    #check can initialise Card objects from string
    cards = [Card.from_str(card_str) for card_str in '♠2,♠K,♥A'.split(',')]
    print(cards[2])
    assert cards[0].value == Value.TWO and cards[0].suit == Suit.SPADES
    assert cards[1].value == Value.KING and cards[1].suit == Suit.SPADES
    assert cards[2].value == Value.ACE and cards[2].suit == Suit.HEARTS

    cards = [Card.from_str(card_str) for card_str in 'S2,SK,HA'.split(',')]
    print(cards[2])
    assert cards[0].value == Value.TWO and cards[0].suit == Suit.SPADES
    assert cards[1].value == Value.KING and cards[1].suit == Suit.SPADES
    assert cards[2].value == Value.ACE and cards[2].suit == Suit.HEARTS

