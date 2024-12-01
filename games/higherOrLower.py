from cards.deck import Deck
from leaderboard.leaderboard import Leaderboard

class HigherOrLower:
    """
    Represents the logic for the Higher or Lower game, including card drawing,
    scorekeeping, and game state management.
    """

    def __init__(self, leaderboard=None):
        """
        Initialises the game with a shuffled deck, game constants, variables, and leaderboard.

        Args:
            leaderboard (Leaderboard, optional): Custom leaderboard instance.
                                                 If None, a default leaderboard is created.
        """
        # Initialise the deck with jokers and shuffle it
        self.deck = Deck(include_jokers=True)
        self.deck.shuffle()

        # Game constants
        self.STARTING_LIVES = 3  # Initial number of lives
        self.BASE_SCORE = 2      # Points for a correct guess
        self.STREAK_MULTIPLIER = 2  # Bonus multiplier for streaks

        # Game variables
        self.lives = self.STARTING_LIVES  # Player's remaining lives
        self.score = 0                   # Banked points
        self.unbanked_points = 0         # Points at risk (unbanked)
        self.streak = 0                  # Consecutive correct guesses

        # Initialise the leaderboard
        if not leaderboard:
            leaderboard = Leaderboard(db_path='leaderboard.db')  # Default leaderboard
        else:
            self.leaderboard = leaderboard

    def display_state(self):
        """
        Displays the current state of the game, including score, unbanked points,
        streak, and remaining lives.
        """
        print(f"\nScore: {self.score}, Unbanked points: {self.unbanked_points}, " + 
              f"Current streak: {self.streak}, Lives: {self.lives}")
        
    def getRules(self):
        """
        Returns a string containing the game rules and instructions.

        Returns:
            str: The rules and instructions for the Higher or Lower game.
        """
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
        """
        Draws a card from the deck. Automatically creates and shuffles a new deck
        if the current deck is empty. Grants an extra life if a Joker is drawn.

        Returns:
            Card: The drawn card or None if the deck was empty.
        """
        self.card = self.deck.draw_card()
        if not self.card:
            # If the deck is empty, create and shuffle a new deck
            self.deck = Deck()
            self.deck.shuffle()
            return None
        elif self.card.rank == 'Joker':
            # If a Joker is drawn, add a life
            self.lives += 1
            return self.card
        else:
            # Return the drawn card
            return self.card
        
    def checkGuess(self, card0, card1, guess):
        """
        Checks whether the player's guess (Higher or Lower) is correct.

        Args:
            card0 (Card): The current card.
            card1 (Card): The next card drawn.
            guess (str): Player's guess ('h' for Higher, 'l' for Lower).
        Returns:
            bool: True if the guess is correct, False otherwise.
        Raises:
            ValueError: If the guess is not 'h' or 'l'.
        """
        if guess not in ['h', 'l']:
            raise ValueError('Invalid guess value used.')
        if guess == 'h':
            return card1 > card0
        else:
            return card1 < card0
        
    def incorrect(self):
        """
        Handles the scenario when the player's guess is incorrect.

        Returns:
            int: The number of unbanked points lost.
        """
        points_lost = self.unbanked_points
        self.unbanked_points = 0  # Reset unbanked points
        self.lives -= 1           # Deduct a life
        self.streak = 0           # Reset the streak
        return points_lost
    
    def correct(self):
        """
        Handles the scenario when the player's guess is correct.

        Returns:
            int: The number of points earned from the correct guess.
        """
        points = self.BASE_SCORE + self.streak * self.STREAK_MULTIPLIER
        self.unbanked_points += points  # Add points to unbanked
        self.streak += 1                # Increase the streak
        return points
    
    def bankPoints(self):
        """
        Banks the unbanked points, adding them to the total score.
        Resets unbanked points and streak to zero.
        """
        self.score += self.unbanked_points
        self.unbanked_points = 0
        self.streak = 0

    def gameOver(self, name):
        """
        Handles the end of the game. Adds the player's score to the leaderboard.

        Args:
            name (str): The player's name.
        Returns:
            tuple: The final score and the leaderboard position.
        """
        position = self.leaderboard.add_score(name, self.score)
        return self.score, position

def test():
    """
    A test function to test the functionality of the HigherOrLower class.
    """
    pass

if __name__ == "__main__":
    test()
