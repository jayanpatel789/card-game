"""
Command line interface running of the Higher or Lower game.
"""

from games.higherOrLower import HigherOrLower
from leaderboard.leaderboard import Leaderboard
import time

class HigherOrLowerCLI:
    def __init__(self):
        self.game = HigherOrLower()
        self.leaderboard = Leaderboard(db_path='HoL_leaderboard.db')

    def startSequence(self):
        print("Welcome to Higher Or Lower: EXTREME!")
        rules = input("If you'd like to see the rules, enter y. If not, click enter. ")
        if rules.lower() == 'y':
            self.showRules()
        self.name = input("\nWhat is your name? ")
        print(f"\nCool! Nice to meet you {self.name}")
        
    def showRules(self):
        rules = self.game.getRules()
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
            while True:
                print(f"\nThe current card is the {str(card0)}.")
                action = input("\nGuess Higher (h), Lower (l), Bank (b), or display current status (d): ").lower()
                if action not in ['h', 'l', 'b', 'd']:
                    print("Invalid input. Please enter 'h' for Higher, 'l' for Lower, or 'b' to Bank your points.")
                elif action == 'b':
                    print("You chose to bank your points!")
                    self.game.bankPoints()
                    self.game.display_state()
                elif action == 'd':
                    self.game.display_state()
                elif action == 'h':
                    print("You chose higher!")
                    break
                elif action == 'l':
                    print("You chose lower!")
                    break
            
            while True:
                print("\nDrawing card...")
                time.sleep(1) # Wait for 1 second
                print("...")
                time.sleep(1) # Wait for 1 second

                card1 = self.game.draw_card()
                if not card1:
                    print("Deck finished. New deck being shuffled. No jokers this time!")
                    print("Will now draw again...")
                    time.sleep(1)
                elif card1.rank == 'Joker':
                    print("You just drew a Joker! +1 Life")
                    print("Will now draw again...")
                    time.sleep(1)
                else:
                    break

            print(f"The next card drawn is the {str(card1)}.")
            print("\n...")

            guess = self.game.checkGuess(card0, card1, action)
            if guess:
                points_gained = self.game.correct()
                print(f"You were right!\n+{points_gained} points, +1 streak")
            else:
                points_lost = self.game.incorrect()
                print(f"\nTough luck, you were wrong!\n{points_lost} unbanked points lost, -1 life")

            # Current state
            self.game.display_state()

            # Assign last drawn card to base card
            card0 = card1

        print("Uh oh! You've run out of lives!")
        final_score, position = self.game.gameOver(self.leaderboard, self.name)
        print(f"Final score: {final_score}")
        if position == 1:
            print("NEW HIGH SCORE!")
        print(f"You have entered the leaderboard at {position}")
        print()
        self.leaderboard.display_leaderboard()
        
        self.play_again()

def main():
    game = HigherOrLowerCLI()
    game.play()

if __name__ == "__main__":
    main()









    