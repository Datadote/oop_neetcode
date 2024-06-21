import pytest
from blackjack import Deck

def test_deck_init():
    deck = Deck()
    assert len(deck._cards) == 52, 'Deck not 52 cards'