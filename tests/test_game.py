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



def test_apply_move():
    state = WhistGame(
        current_player=0,
        player_hands=[set(),set()],
        

    )
    
