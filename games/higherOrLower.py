from cards.deck import Deck
from cards.card import Card

class HigherOrLower:
    def __init__(self):
        # Initialise the deck
        self.deck = Deck()
        self.deck.shuffle()
        
        # Game variables
        self.lives = 3
        self.score = 0
        self.unbanked_points = 0
        self.streak = 0
    
    def display_state(self):
        print(f"Score: {self.score}\nUnbanked points: {self.unbanked_points}\n" + 
              f"Remaining lives: {self.lives}")
    
    def draw_card(self):
        # Draw card from the deck
        self.card = self.deck.draw_card()
        # Check if card was actually taken
        if not self.card:
            print("Deck has been emptied.")
            return None
        # Else check if joker was drawn
        elif self.card.rank == 'Joker':
            print("You just drew a Joker! +1 Lives")
            self.lives += 1
            self.draw_card()
        # Else return chosen card
        else:
            print(f"The {self.card} was drawn.")
            return self.card
        
    def checkGuess(self, card0, card1, guess):
        """
        Checks user guess.
            rtn True if correct
            rtn False if incorrect
        """
        if guess not in ['higher', 'lower']:
            raise ValueError('Invalid guess value used.')
        if guess == 'higher':
            return card1 > card0
        else:
            return card1 < card0
        
    def incorrect(self):
        self.lives -= 1
        if self.lives == 0:
            self.gameOver()
        else:
            self.unbanked_points = 0
            self.streak = 0
        return
    
    def correct(self):
        self.streak += 1
        self.unbanked_points += 1 + self.streak*2
        return
    
    def bankPoints(self):
        self.score += self.unbanked_points
        self.unbanked_points
        self.streak = 0

    def gameOver(self):
        print(f"Game Over! Final Score: {self.score}")