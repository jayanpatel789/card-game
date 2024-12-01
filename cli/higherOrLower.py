"""
Command line interface for running the Higher or Lower game.
"""

from games.higherOrLower import HigherOrLower
import time

class HigherOrLowerCLI:
    """
    A command line interface for the Higher or Lower game.

    This class provides methods to interact with the game, display rules,
    manage gameplay, and handle user input.
    """

    def __init__(self):
        """
        Initialises the CLI game by creating a new instance of the HigherOrLower game logic.
        """
        self.game = HigherOrLower()

    def startSequence(self):
        """
        Displays a welcome message, allows the user to view the rules, and asks for user's
        name for saving score later on.
        """
        print("Welcome to Higher Or Lower: Point Rush!")
        rules = input("If you'd like to see the rules, enter y. If not, click enter. ")
        if rules.lower() == 'y':
            self.showRules()
        self.name = input("\nWhat is your name? ")
        print(f"\nCool! Nice to meet you {self.name}")
        
    def showRules(self):
        """
        Retrieves and displays the rules of the game by calling the HigherOrLower game logic.
        """
        rules = self.game.getRules()
        print(rules)

    def play_again(self):
        """
        Prompts the player to decide whether to play again.
        If 'y' is chosen, the game restarts. Otherwise, the game ends with a goodbye message.
        """
        replay = input("Would you like to play again? (y/n): ").lower()
        if replay == 'y':
            # Reset the game and start over
            self.game = HigherOrLower()
            self.play()
        else:
            print("Thanks for playing! Goodbye!")

    def play(self):
        """
        Main gameplay loop for Higher or Lower. Handles user interaction,
        card drawing, guesses, and game state updates.
        """
        # Start the game sequence
        self.startSequence()
        print("\nLET'S PLAY!")

        # Draw the first card
        card0 = self.game.draw_card()
        print(f"\nThe first card drawn was the {str(card0)}!")

        # Gameplay continues while the player has lives
        while self.game.lives > 0:
            # Inner loop for user input and actions
            while True:
                print(f"\nThe current card is the {str(card0)}.")
                action = input("\nGuess Higher (h), Lower (l), Bank (b), or display current status (d): ").lower()
                if action not in ['h', 'l', 'b', 'd']:
                    print("Invalid input. Please enter 'h' for Higher, 'l' for Lower, or 'b' to Bank your points.")
                elif action == 'b':
                    # Bank current points
                    print("You chose to bank your points!")
                    self.game.bankPoints()
                    self.game.display_state()
                elif action == 'd':
                    # Display the current game state
                    self.game.display_state()
                elif action == 'h':
                    # Guess higher
                    print("You chose higher!")
                    break
                elif action == 'l':
                    # Guess lower
                    print("You chose lower!")
                    break
            
            # Loop for drawing the next card
            while True:
                print("\nDrawing card...")
                time.sleep(1)  # Wait for user-friendliness when reading
                print("...")
                time.sleep(1)

                card1 = self.game.draw_card()
                if not card1:
                    # Handle case where the deck is finished
                    print("Deck finished. New deck being shuffled. No jokers this time!")
                    print("Will now draw again...")
                    time.sleep(1)
                elif card1.rank == 'Joker':
                    # Handle Joker cards (add a life)
                    print("You just drew a Joker! +1 Life")
                    print("Will now draw again...")
                    time.sleep(1)
                else:
                    # Valid card drawn
                    break

            print(f"The next card drawn is the {str(card1)}.")
            print("\n...")

            # Check the player's guess
            guess = self.game.checkGuess(card0, card1, action)
            if guess:
                # Correct guess
                points_gained = self.game.correct()
                print(f"You were right!\n+{points_gained} points, +1 streak")
            else:
                # Incorrect guess
                points_lost = self.game.incorrect()
                print(f"\nTough luck, you were wrong!\n{points_lost} unbanked points lost, -1 life")

            # Display the current game state
            self.game.display_state()

            # Set the last drawn card as the new base card
            card0 = card1

        # Game over sequence when lives run out
        print("Uh oh! You've run out of lives!")
        final_score, position = self.game.gameOver(self.name)
        print(f"Final score: {final_score}")
        if position == 1:
            print("NEW HIGH SCORE!")
        print(f"You have entered the leaderboard at {position}")
        print()
        self.leaderboard.display_leaderboard()
        
        # Prompt to play again
        self.play_again()

def main():
    """
    Main entry point for the CLI version of the game.
    Creates an instance of HigherOrLowerCLI and starts the game.
    """
    game = HigherOrLowerCLI()
    game.play()

if __name__ == "__main__":
    main()
