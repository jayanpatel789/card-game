"""
Command line interface running of the Higher or Lower game.
"""

from games.higherOrLower import HigherOrLower
import time

class HigherOrLowerCLI:
    def __init__(self):
        self.game = HigherOrLower()

    def startSequence(self):
        print("Welcome to Higher Or Lower: EXTREME!")
        rules = input("If you'd like to see the rules, enter y. If not, click enter. ")
        if rules.lower() == 'y':
            self.showRules()
        
    def showRules(self):
        rules = """
        Welcome to the Higher or Lower Game!

        Rules:
        1. You start with 3 lives.
        2. Your goal is to accumulate as many points as possible.
        3. A card will be drawn, and you must guess if the next card will be HIGHER or LOWER.
        - Ties do not count.
        4. If your guess is correct:
        - You earn points: 1 + streak bonus.
        - Your streak increases, and you earn additional points for maintaining it.
        5. If your guess is incorrect:
        - You lose a life.
        - All unbanked points are lost.
        - Your streak resets to 0.
        6. You can bank your unbanked points before guessing. Banked points are safe.
        7. If you draw a Joker:
        - You gain 1 extra life as a bonus!
        8. The deck starts shuffled. If all cards are drawn, the deck reshuffles automatically.
        9. The game ends when you lose all your lives.

        Good luck and enjoy the game!
        """

        print(rules)

    def play_again(self):
        replay = input("Would you like to play again? (y/n): ").lower()
        if replay == 'y':
            self.game = HigherOrLower()
            self.play()
        else:
            print("Thanks for playing! Goodbye!")

    def play(self):
        # Start sequence
        self.startSequence()

        print("\nLET'S PLAY!")

        # Draw first card in game
        card0 = self.game.draw_card()
        print(f"\nThe first card drawn was the {str(card0)}!")

        while self.game.lives > 0:

            print(f"\nThe current card is the {str(card0)}.")

            while True:
                action = input("\nGuess Higher (h), Lower (l), Bank (b), or display current status (d): ").lower()
                if action not in ['h', 'l', 'b', 'd']:
                    print("Invalid input. Please enter 'h' for Higher, 'l' for Lower, or 'b' to Bank your points.")
                elif action == 'b':
                    print("You chose to Bank your points!")
                    self.game.bankPoints()
                    self.game.display_state()
                elif action == 'd':
                    self.game.display_state()
                elif action == 'h':
                    print("You chose Higher!")
                    break
                elif action == 'l':
                    print("You chose Lower!")
                    break
            
            print("\nDrawing card...")
            time.sleep(1) # Wait for 1 second
            print("...")
            time.sleep(1) # Wait for 1 second
            card1 = self.game.draw_card()
            print(f"The next card drawn is the {str(card1)}.")

            guess = self.game.checkGuess(card0, card1, action)
            if guess:
                print("\nYou were right!")
                self.game.correct()
            else:
                print("\nTough luck! You were wrong")
                self.game.incorrect()

            # Current state
            self.game.display_state()

            # Assign last drawn card to base card
            card0 = card1

        print("You've run out of lives!")
        self.game.gameOver()
        self.play_again()

def main():
    game = HigherOrLowerCLI()
    game.play()

if __name__ == "__main__":
    main()









    