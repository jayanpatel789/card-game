from cards.deck import Deck
from leaderboard.leaderboard import Leaderboard


class HigherOrLower:
    def __init__(self, leaderboard=None):
        # Initialise the deck
        self.deck = Deck(include_jokers=True)
        self.deck.shuffle()

        # GAME constants
        self.STARTING_LIVES = 3
        self.BASE_SCORE = 2
        self.STREAK_MULTIPLIER = 2
        
        # Game variables
        self.lives = self.STARTING_LIVES
        self.score = 0
        self.unbanked_points = 0
        self.streak = 0

        # Leaderboard
        if not leaderboard:
            leaderboard = Leaderboard(db_path='leaderboard.db')
        else:
            self.leaderboard = leaderboard
    
    def display_state(self):
        print(f"\nScore: {self.score}, Unbanked points: {self.unbanked_points}, " + 
              f"Current streak: {self.streak}, Lives: {self.lives}")
        
    def getRules(self):
        rules = f"""
        Welcome to Higher or Lower: Point Rush!
        Try to get the highest score possible!

        Key Terms:
        - Score (a.k.a. banked points): Points you have safely saved. These cannot be lost.
        - Unbanked Points: Points you earn from correct guesses. These are at risk until you bank them.
        You want the highest SCORE!

        Rules:
        1. You start with {self.STARTING_LIVES} lives.
        2. After a card is drawn, you have three options:
           - Click HIGHER if you think the next card will be higher.
           - Click LOWER if you think the next card will be lower.
           - Click BANK to add your unbanked points to your total score and secure them.
           - For higher and lower, ties do not count.
        3. BANK:
           - Banking adds unbanked points to your total score.
           - Banking resets your streak to 0.
        4. If your guess is correct:
           - Earn unbanked points: {self.BASE_SCORE} + (streak * {self.STREAK_MULTIPLIER}).
           - Your streak increases by 1.
        5. If your guess is incorrect:
           - Lose 1 life.
           - All unbanked points are lost.
           - Your streak resets to 0.
        6. Drawing a Joker:
           - Gain 1 extra life as a bonus!
        7. When the deck runs out, it reshuffles automatically.
        8. The game ends when you lose all your lives.

        Tips:
        - Bank your points strategically to avoid losing them!
        - Build streaks for higher rewards.

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
        points = self.BASE_SCORE + self.streak*self.STREAK_MULTIPLIER
        self.unbanked_points += points
        self.streak += 1
        return points
    
    def bankPoints(self):
        self.score += self.unbanked_points
        self.unbanked_points = 0
        self.streak = 0

    def gameOver(self, name):
        position = self.leaderboard.add_score(name, self.score)
        return self.score, position

def test():
    game = HigherOrLower()
    print(game.deck)

    for i in range(len(game.deck)):
        card = game.deck.draw_card()
        print(f"{i}: {card}")

if __name__ == "__main__":
    test()