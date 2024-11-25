from cards.card import Card
from random import shuffle

class Deck:
    def __init__(self, include_jokers=False):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = []
        
        for suit in self.suits:
            for rank in self.ranks:
                card = Card(rank, suit)
                self.cards.append(card)

        if include_jokers:
            self.cards.append(Card('Joker', 'Red'))
            self.cards.append(Card('Joker', 'Black'))

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            card = self.cards.pop()
            return card
        else:
            return None