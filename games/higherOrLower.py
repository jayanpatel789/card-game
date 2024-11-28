from cards.deck import Deck


class HigherOrLower:
    def __init__(self):
        # Initialise the deck
        self.deck = Deck(include_jokers=True)
        self.deck.shuffle()
        
        # Game variables
        self.lives = 3
        self.score = 0
        self.unbanked_points = 0
        self.streak = 0
    
    def display_state(self):
        print(f"\nScore: {self.score}, Unbanked points: {self.unbanked_points}, " + 
              f"Current streak: {self.streak}, Lives: {self.lives}")
        
    def getRules(self):
        rules = """
        Welcome to the Higher or Lower Game!\n
        Rules:
        1. You start with 3 lives.
        2. Your goal is to accumulate as high a score as possible.
        3. A card will be drawn, and you must guess if the next card will be HIGHER or LOWER or BANK.
        - Ties do not count.
        3a. BANK - You can bank your unbanked points before guessing. This adds your unbanked points
            to your score.
        4. If your guess is correct:
        - You earn points: 1 + streak * 2.
        - Your streak increments, meaning you earn additional points for maintaining it.
        5. If your guess is incorrect:
        - You lose a life.
        - All unbanked points are lost.
        - Your streak resets to 0.
        7. If you draw a Joker:
        - You gain 1 extra life as a bonus!
        8. The deck starts shuffled. If all cards are drawn, the deck reshuffles automatically.
        9. The game ends when you lose all your lives.\n
        Good luck and enjoy the game!
        """
        return rules
    
    def draw_card(self):
        # Draw card from the deck
        self.card = self.deck.draw_card()
        # If deck had been finished create new deck
        if not self.card:
            self.deck = Deck()
            self.deck.shuffle()
            return None
        # Else check if joker was drawn
        elif self.card.rank == 'Joker':
            self.lives += 1
            return self.card
        # Else return chosen card
        else:
            return self.card
        
    def checkGuess(self, card0, card1, guess):
        """
        Checks user guess.
            rtn True if correct
            rtn False if incorrect
        """
        if guess not in ['h', 'l']:
            raise ValueError('Invalid guess value used.')
        if guess == 'h':
            return card1 > card0
        else:
            return card1 < card0
        
    def incorrect(self):
        points_lost = self.unbanked_points
        self.unbanked_points = 0
        self.lives -= 1
        self.streak = 0
        return points_lost
    
    def correct(self):
        points = 1 + self.streak*2
        self.unbanked_points += points
        self.streak += 1
        return points
    
    def bankPoints(self):
        self.score += self.unbanked_points
        self.unbanked_points = 0
        self.streak = 0

    def gameOver(self, leaderboard, name):
        position = leaderboard.add_score(name, self.score)
        return self.score, position

def test():
    game = HigherOrLower()
    print(game.deck)

    for i in range(len(game.deck)):
        card = game.deck.draw_card()
        print(f"{i}: {card}")

if __name__ == "__main__":
    test()