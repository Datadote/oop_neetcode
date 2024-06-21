""" OOP design of blackjack """
import enum
import random
from abc import ABC, abstractmethod
from typing import List

class Suit(enum.Enum):
    HEARTS = 'hearts'
    SPADES = 'spades'
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'

class Card:
    def __init__(self, val: int, suit: enum.Enum):
        self._suit = Suit(suit)
        self._val = val

    def get_suit(self):
        return self._suit

    def get_value(self):
        return self._val

    def print(self):
        print(self._val, self._suit)

class Hand:
    def __init__(self):
        self._score = 0
        self._cards = []

    def add_card(self, card: Card):
        self._cards.append(card)
        if card.get_value() == 1:
            if self._score + 11 <= 21:
                self._score += 11
                self._cards[-1].val = 11
            else:
                self._score += 1
        else:
            self._score += card.get_value()

    def get_score(self):
        return self._score

    def get_cards(self):
        return self._cards

    def print(self):
        for card in self._cards:
            card.print()

class Deck:
    def __init__(self):
        self._cards: List[Card] = []
        self.init_deck()

    def init_deck(self):
        # 52 cards, 4 suits, 1-9, 1 = ace, 10, jack, q, k
        for suit in Suit:
            for val in range(1, 10):
                self._cards.append(Card(val, suit))
            for _ in range(4):
                self._cards.append(Card(val, suit))

    def shuffle_deck(self):
        for idx1 in range(len(self._cards)):
            idx2 = random.randint(0, len(self._cards) - 1)
            self._cards[idx1], self._cards[idx2] = self._cards[idx2], self._cards[idx1]

    def draw(self) -> Card:
        assert len(self._cards) > 0, 'Not enough cards'
        return self._cards.pop()

    def print(self):
        for card in self._cards:
            card.print()

class Human(ABC):
    def __init__(self, hand: Hand):
        self._hand = hand

    def get_hand(self):
        return self._hand

    def clear_hand(self):
        self._hand = Hand()

    def add_card(self, card: Card):
        self._hand.add_card(card)

    @abstractmethod
    def make_move(self) -> bool:
        pass

class Dealer(Human):
    """ Dealer sees opponents card and plays until win or bust"""
    def __init__(self, hand: Hand, target_score: int = 17):
        super().__init__(hand)
        self._target_score = target_score

    def update_target_score(self, target_score: int):
        self._target_score = target_score

    def make_move(self) -> bool:
        """ Should player or dealer make a move"""
        return self.get_hand().get_score() < self._target_score

class Player(Human):
    def __init__(self, hand: Hand, balance: int):
        super().__init__(hand)
        self._balance = balance
        self._bet = 0

    def get_balance(self) -> int:
        return self._balance

    def place_bet(self, amt: int):
        """ Why does this return amount? """
        if amt > self._balance:
            raise ValueError('Insufficient funds')
        self._balance -= amt
        self._bet = amt

    def get_bet(self) -> int:
        return self._bet

    def receive_winnings(self, winnings: int):
        self._balance += winnings

    def make_move(self) -> bool:
        if self.get_hand().get_score() > 21:
            return False
        move = input('Draw card? [y/n] ')
        return move == 'y'

class Game:
    def __init__(self, player: Player, dealer: Dealer, deck: Deck):
        self._player = player
        self._dealer = dealer
        self._deck = deck
        self._win_score = 21

    def play(self):
        print(f'**Player balance: {self._player.get_balance()}')
        start_game = True
        while self._player.get_balance() > 0 and start_game:
            self._deck.shuffle_deck()
            bet = self.get_player_bet()
            self._player.place_bet(bet)
            self.deal_init_cards()

            # Player plays
            while True:
                if self._player.make_move():
                    card = self._deck.draw()
                    print('Player draws', card.get_suit(), card.get_value())
                    self._player.add_card(card)
                    print('Player score: ', self._player.get_hand().get_score())

                    if self._player.get_hand().get_score() > self._win_score:
                        print('Player busts!')
                        self.clean_up()
                        return
                else:
                    break

            # Dealer plays
            self._dealer.update_target_score(self._player.get_hand().get_score())
            print('Dealer has: ')
            self._dealer.get_hand().print()
            while self._dealer.make_move():
                print('****')
                card = self._deck.draw()
                print('Dealer draws', card.get_suit(), card.get_value())
                self._dealer.add_card(card)
                dealer_score = self._dealer.get_hand().get_score()
                print('Dealer score: ', dealer_score)
            dealer_score = self._dealer.get_hand().get_score()
            if dealer_score > self._win_score:
                print('Dealer busts! Player wins')
                self._player.receive_winnings(self._player.get_bet() * 2)
            elif dealer_score == self._dealer.get_target_score():
                print('Draw')
                self._player.receive_winnings(self._player.get_bet())
            else:
                print('Dealer wins. Player Loses')
            self.clean_up()
            if self._player.get_balance() > 0:
                print(f'**Player balance: {self._player.get_balance()}')
                start_game = input('Play again? [y/n]') == 'y'
            else:
                print("Not enough money, can't play again")
                start_game = False
        print(f'**Player final balance: {self._player.get_balance()}')

    def get_player_bet(self) -> int:
        print(f'balance: {self._player.get_balance()}')
        amt = int(input('Enter a bet: '))
        return amt

    def deal_init_cards(self):
        for _ in range(2):
            self._dealer.add_card(self._deck.draw())
            self._player.add_card(self._deck.draw())
        print('Player hands: ')
        self._player.get_hand().print()
        # dealer only shows 1 card
        dealer_card = self._dealer.get_hand().get_cards()[0]
        print("Dealer's first card: ")
        dealer_card.print()

    def clean_up(self):
        self._deck = Deck()
        self._dealer.clear_hand()
        self._player.clear_hand()
