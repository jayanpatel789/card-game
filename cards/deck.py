from cards.card import Card
from random import shuffle

class Deck:
    """
    Represents a standard deck of playing cards with an option to include Jokers.

    Attributes:
        ranks (list): List of card ranks as strings (e.g., '1' for Ace, '2' to '10', '11' for Jack, '12' for Queen, '13' for King).
        suits (list): List of card suits (e.g., 'Hearts', 'Diamonds', 'Clubs', 'Spades').
        cards (list): List of Card objects that make up the deck.
    """

    def __init__(self, include_jokers=False):
        """
        Initialises the deck with 52 cards by default and optionally includes Jokers.

        Args:
            include_jokers (bool): If True, adds two Joker cards (one Red, one Black) to the deck.
        """
        self.RANKS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        self.SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = []
        
        # Generate cards for each suit and rank
        for suit in self.SUITS:
            for rank in self.RANKS:
                card = Card(rank, suit)
                self.cards.append(card)

        # Add Jokers if specified
        if include_jokers:
            self.cards.append(Card('Joker', 'Red'))
            self.cards.append(Card('Joker', 'Black'))

    def __str__(self):
        """
        Provides a human-readable string representation of the deck.

        Returns:
            str: A summary of the number of cards and a list of the cards in the deck.
        """
        return f"Deck with {len(self.cards)} cards: {', '.join(str(card) for card in self.cards)}"

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the deck.

        Returns:
            str: A summary of the deck size and the top card (if any).
        """
        return f"Deck({len(self.cards)} cards, top card: {str(self.cards[-1]) if self.cards else 'None'})"
    
    def __len__(self):
        """
        Returns the number of cards currently in the deck.

        Returns:
            int: The total number of cards in the deck.
        """
        return len(self.cards)

    def shuffle(self):
        """
        Shuffles the cards in the deck using a random shuffling algorithm.
        """
        shuffle(self.cards)

    def draw_card(self):
        """
        Removes and returns the top card from the deck.

        Returns:
            Card: The top card from the deck, or None if the deck is empty.
        """
        if len(self.cards) > 0:
            card = self.cards.pop()
            return card
        else:
            return None
        
def test():
    """
    Test function to test the functionality of the Deck class.
    """
    pass

if __name__ == "__main__":
    test()
