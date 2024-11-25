from cards.deck import Deck

class HigherOrLower:
    def __init__(self):
        # Initialise the deck
        self.deck = Deck()
        self.deck.shuffle()
        
        # Game variables
        self.lives = 3
        self.banked_points = 0
        self.unbanked_points = 0
        self.streak = 0
    
    def draw_card(self):
        self.card = self.deck.draw_card()
        if not self.card:
            print("Deck has been emptied.")
            return None
        elif self.card.rank == 'Joker':
            print("You just drew a Joker! +1 Lives")
            self.lives += 1
            self.draw_card()
        else:
            print(f"You just drew the {self.card}")
            return self.card
        
    