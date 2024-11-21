from card import Card

class Deck:
    def __init__(self, include_jokers=False):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = []
        
        for rank in self.ranks:
            for suit in self.suits:
                card = Card(rank, suit)
                self.cards.append(card)

        if include_jokers:
            self.cards.append(Card('Joker', 'Black'))
            self.cards.append(Card('Joker', 'Red'))