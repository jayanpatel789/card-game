from cards.card import Card
from random import shuffle

class Deck:
    def __init__(self, include_jokers=False):
        self.ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = []
        
        for suit in self.suits:
            for rank in self.ranks:
                card = Card(rank, suit)
                self.cards.append(card)

        if include_jokers:
            self.cards.append(Card('Joker', 'Red'))
            self.cards.append(Card('Joker', 'Black'))

    def __str__(self):
        return f"Deck with {len(self.cards)} cards: {', '.join(str(card) for card in self.cards)}"

    def __repr__(self):
        return f"Deck({len(self.cards)} cards, top card: {str(self.cards[-1]) if self.cards else 'None'})"
    
    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            card = self.cards.pop()
            return card
        else:
            return None
        
def test():
    deck = Deck(include_jokers=True)
    for _ in range(15):
        card = deck.draw_card()
        print(f"Card: {card}")
    
    print()

    deck = Deck(include_jokers=True)
    deck.shuffle()
    for _ in range(15):
        card = deck.draw_card()
        print(f"Card: {card}")

if __name__ == "__main__":
    test()