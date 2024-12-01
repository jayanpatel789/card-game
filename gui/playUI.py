from games.higherOrLower import HigherOrLower
from gui.leaderboardDialog import LeaderboardDialog
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import os

class PlayUI(QMainWindow):
    """
    Represents the gameplay UI for Higher or Lower: Point Rush. Handles user interactions,
    game state transitions, and integrates leaderboard functionality.
    """

    def __init__(self, leaderboard):
        """
        Initialises the gameplay screen UI, loading the UI file, game instance,
        and connecting buttons to their respective actions.

        Args:
            leaderboard (Leaderboard): The leaderboard instance to save scores and rankings.
        """
        super(PlayUI, self).__init__()
        self.dirpath = os.path.dirname(os.path.abspath(__file__))
        UIpath = os.path.join(self.dirpath, r"ui\play_screen.ui")
        print(UIpath)
        loadUi(UIpath, self)

        # Define stylesheets for UI elements
        self.enabled_button_style = "background-color: darkgreen; color: white;"
        self.disabled_button_style = "background-color: gray; color: darkgray;"
        self.enabled_label_style = "color: white"
        self.disabled_label_style = "color: darkgray"
        self.menu_button_green = "background-color: rgb(0,100,0); color: white"
        self.menu_button_blue = "background-color: rgb(0,85,255); color: white"
        self.menu_button_maroon = "background-color: maroon; color: white"

        # Initialise the game and state
        self.leaderboard = leaderboard
        self.game = HigherOrLower(self.leaderboard)  # Start a new game instance
        self.current_state = "START_GAME"  # Initial game state

        # Set initial values in the UI
        self.score_value.setText(str(self.game.score))
        self.streak_value.setText(str(self.game.streak))
        self.unbanked_points_value.setText(str(self.game.unbanked_points)) 
        self.lives_left_value.setText(str(self.game.STARTING_LIVES))

        # Connect buttons to respective functions
        self.restart_button.clicked.connect(self.restart_game)
        self.home_button.clicked.connect(self.quit_to_home)
        self.rules_button.clicked.connect(self.show_rules)
        self.leaderboard_button.clicked.connect(self.show_leaderboard)
        self.higher_button.clicked.connect(lambda: self.action("h"))
        self.lower_button.clicked.connect(lambda: self.action("l"))
        self.bank_button.clicked.connect(lambda: self.action("b"))
        self.next_button.clicked.connect(self.advance_state)

        # Initialise UI with starting message and button states
        self.display("Welcome! Click next to draw a card")
        self.next_button_state()

    ######## BUTTON STATE DEFINITIONS ###########
    """Management of button enable, disable and appearance"""

    def next_button_state(self):
        """Enable only the 'Next' button and disable all guessing buttons."""
        self.higher_button.setEnabled(False)
        self.higher_button.setStyleSheet(self.disabled_button_style)
        self.lower_button.setEnabled(False)
        self.lower_button.setStyleSheet(self.disabled_button_style)
        self.bank_button.setEnabled(False)
        self.bank_button.setStyleSheet(self.disabled_button_style)
        self.next_button.setEnabled(True)
        self.next_button.setStyleSheet(self.enabled_button_style)

        self.higher_lower_label.setStyleSheet(self.disabled_label_style)
        self.bank_label.setStyleSheet(self.disabled_label_style)

    def guess_button_state(self):
        """Enable only the 'Higher', 'Lower', and 'Bank' buttons, disabling 'Next'."""
        self.higher_button.setEnabled(True)
        self.higher_button.setStyleSheet(self.enabled_button_style)
        self.lower_button.setEnabled(True)
        self.lower_button.setStyleSheet(self.enabled_button_style)
        self.bank_button.setEnabled(True)
        self.bank_button.setStyleSheet(self.enabled_button_style)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet(self.disabled_button_style)

        self.higher_lower_label.setStyleSheet(self.enabled_label_style)
        self.bank_label.setStyleSheet(self.enabled_label_style)

    def disable_all_buttons(self):
        """Disable 'Next', 'Higher', 'Lower', and 'Bank' on the UI."""
        self.higher_button.setEnabled(False)
        self.higher_button.setStyleSheet(self.disabled_button_style)
        self.lower_button.setEnabled(False)
        self.lower_button.setStyleSheet(self.disabled_button_style)
        self.bank_button.setEnabled(False)
        self.bank_button.setStyleSheet(self.disabled_button_style)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet(self.disabled_button_style)

        self.higher_lower_label.setStyleSheet(self.disabled_label_style)
        self.bank_label.setStyleSheet(self.disabled_label_style)

    def menu_button_startgame(self):
        self.home_button.setText("Quit")
        self.restart_button.setText("Restart")

        self.home_button.setStyleSheet(self.menu_button_maroon)
        self.restart_button.setStyleSheet(self.menu_button_green)
        self.rules_button.setStyleSheet(self.menu_button_green)
        self.leaderboard_button.setStyleSheet(self.menu_button_green)

    def menu_button_endgame(self):
        self.home_button.setText("Home")
        self.restart_button.setText("Play Again")
        
        self.home_button.setStyleSheet(self.menu_button_maroon)
        self.restart_button.setStyleSheet(self.menu_button_blue)
        self.rules_button.setStyleSheet(self.menu_button_green)
        self.leaderboard_button.setStyleSheet(self.menu_button_green)
        
    ######## MENU FUNCTIONS ###########
    """
    Functionality for the menu buttons in GUI - home/quit, restart/play again,
    rules, and leaderboard.
    """

    def restart_game(self):
        """
        Restart the game by resetting the game state and updating the UI.
        """
        self.game = HigherOrLower(self.leaderboard)
        self.update_ui(no_deck=True)
        self.display("New game! Click next to draw")
        self.next_button_state()
        self.menu_button_startgame() # Menu buttons to start game appearance
        self.current_state = "START_GAME"

    def quit_to_home(self):
        """
        Quit to the home screen, if a return-to-home callback is defined.

        - Checks if a 'return_to_home' function exists.
        - If so, calls it to transition back to the home screen.
        """
        if hasattr(self, 'return_to_home') and self.return_to_home:
            self.return_to_home()  # Call the callback to return to home

    def show_rules(self):
        """
        Displays the game rules in a dialog window.

        - Initialises a game instance to retrieve the rules.
        - Creates a QDialog with a QLabel to show the rules text.
        - Applies custom styling to the text for better readability.
        """
        # Create a game instance to fetch the rules
        self.game = HigherOrLower(self.leaderboard)
        rules = self.game.getRules()

        # Create a QDialog for displaying the rules
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Rules")
        dialog.setGeometry(100, 100, 400, 600)  # Set the size of the dialog

        # Create a QLabel to display the rules and add it to the dialog
        layout = QVBoxLayout(dialog)
        label = QLabel(rules, dialog)
        layout.addWidget(label)

        # Apply custom styles to the QLabel
        label.setStyleSheet("color: white; font-size: 20px; font-family: Bodoni MT;")

        # Execute the dialog to show it on the screen
        dialog.exec_()

    def show_leaderboard(self):
        """
        Display the leaderboard in a custom dialog window.
        """
        dialog = LeaderboardDialog(self.leaderboard)  # Create the leaderboard dialog
        dialog.exec_()  # Display the dialog

    ############ GAME MANAGEMENT ##############
    """
    Methods managing the gameplay logic and its integration with the UI.

    Game States:
    1. "START_GAME":
        - The initial state of the game.
        - Draws the first card from the deck and sets up the game.
        - Handles special cases such as drawing a Joker as the first card.

    2. "WAIT_FOR_GUESS":
        - Waits for the player to make a guess or bank their points.
        - Enables the 'Higher', 'Lower', and 'Bank' buttons for user interaction.

    3. "DRAW_AFTER_GUESS":
        - Occurs after the player makes a guess.
        - Draws the next card from the deck and checks the player's guess.
        - Handles special cases such as drawing a Joker or an empty deck.

    4. "UPDATE_STATE":
        - Updates the game's score, streak, and remaining lives based on the result of the player's guess.
        - Checks if the game should continue or transition to the game-over state.

    5. "GAME_OVER":
        - The final state of the game.
        - Displays the player's final score and prompts them to save their score to the leaderboard.
        - Updates the UI to indicate that the game has ended and offers options to restart or return to the home screen.

    These states ensure that only one display message is required before the user needs to take action, controlling the
    flow of the game and the ease of interaction for the user.
    """

    def advance_state(self):
        """
        Determines the next game state and calls the appropriate method 
        based on the current state when the 'Next' button is clicked.
        """
        if self.current_state == "START_GAME":
            self.start_game()  # Begin the game by drawing the first card
        elif self.current_state == "WAIT_FOR_GUESS":
            self.display(f"The card is: {self.card0}")
            self.guess_button_state()  # Enable the guessing buttons
        elif self.current_state == "DRAW_AFTER_GUESS":
            self.draw_after_guess()  # Handle card drawing after a guess
        elif self.current_state == "UPDATE_STATE":
            self.update_state()  # Update the game based on the guess result
        elif self.current_state == "GAME_OVER":
            self.game_over()  # Handle the end-of-game scenario

    def start_game(self):
        """
        Starts the game by drawing the first card from the deck.
        Handles the special case where the first card is a Joker.
        """
        self.card0 = self.game.draw_card()  # Draw the first card

        if self.card0.rank == 'Joker':
            # Joker scenario: Add a life, maintain state, and allow redrawing
            self.display("You drew a Joker! +1 Life. Click next to draw again")
            self.update_ui()
            self.next_button_state()  # Enable the 'Next' button
            self.current_state = "START_GAME"
        else:
            # Normal card scenario: Display the card and enable guessing buttons
            self.display(f"The card is: {self.card0}")
            self.update_ui()
            self.guess_button_state()  # Enable guessing buttons
            self.current_state = "WAIT_FOR_GUESS"

    def action(self, signal):
        """
        Handles user actions for guessing 'Higher', 'Lower', or 'Banking' points.

        Args:
            signal (str): The action signal ('h' for Higher, 'l' for Lower, 'b' for Bank).
        """
        if signal == 'h':
            # Player guesses 'Higher'
            self.guess = signal
            self.display("You chose higher! Click next to draw")
            self.next_button_state()  # Enable the 'Next' button
            self.current_state = "DRAW_AFTER_GUESS"
        elif signal == 'l':
            # Player guesses 'Lower'
            self.guess = signal
            self.display("You chose lower! Click next to draw")
            self.next_button_state()
            self.current_state = "DRAW_AFTER_GUESS"
        else:
            # Player chooses to bank points
            if self.game.unbanked_points > 0:
                self.game.bankPoints()  # Bank the unbanked points
                self.update_ui()
                self.display("You banked! Click next to continue")
            else:
                # No points to bank
                self.display("No points to bank! Click next to continue")
            self.next_button_state()
            self.current_state = "WAIT_FOR_GUESS"

    def draw_after_guess(self):
        """
        Draws the next card after a player makes a guess.
        Checks the result of the guess and updates the game state accordingly.
        """
        self.card1 = self.game.draw_card()  # Draw the next card
        if not self.card1:
            # Handle case where the deck is empty
            self.display("New deck - no jokers this time! Click next to draw")
            self.next_button_state()
            self.current_state = "DRAW_AFTER_GUESS"
            return

        if self.card1.rank == 'Joker':
            # Joker scenario: Add a life and allow redrawing
            self.display("You drew a Joker! +1 Life. Click next to draw again")
            self.update_ui()
            self.current_state = "DRAW_AFTER_GUESS"
        else:
            # Normal card scenario: Check the player's guess
            self.update_ui()
            result = self.game.checkGuess(self.card0, self.card1, self.guess)
            if result:
                # Correct guess
                self.display(f"The next card is: {self.card1} - you were right!")
                self.current_state = "UPDATE_STATE"
            else:
                # Incorrect guess
                self.display(f"The next card is: {self.card1} - tough luck!")
                self.current_state = "UPDATE_STATE"

    def update_state(self):
        """
        Updates the game state based on whether the player's guess was correct or not.
        Handles scoring, streak updates, and checks for game over conditions.
        """
        if self.game.checkGuess(self.card0, self.card1, self.guess):
            # Correct guess: Award points and update streak
            points_gained = self.game.correct()
            self.display(f"+{points_gained} points! ({self.game.BASE_SCORE} + {(self.game.streak-1)*self.game.STREAK_MULTIPLIER} streak bonus)")
        else:
            # Incorrect guess: Deduct points and a life
            points_lost = self.game.incorrect()
            self.display(f"Lost {points_lost} unbanked points and 1 life.")
        self.update_ui()

        if self.game.lives <= 0:
            # If no lives remain, end the game
            self.current_state = "GAME_OVER"
        else:
            # Continue the game with the newly drawn card
            self.card0 = self.card1
            self.current_state = "WAIT_FOR_GUESS"

    def game_over(self):
        """
        Handles the game-over state by saving the player's score to the leaderboard.
        Displays the final score and updates the UI to reflect the end of the game.
        """
        self.display("Game Over! Calculating final score...")

        # Prompt the player to enter their name
        name, ok = QInputDialog.getText(self, "Game Over", "Enter your name:")
        if ok and name.strip():
            # Save the score to the leaderboard
            final_score, position = self.game.gameOver(name.strip())
            if position == 1:
                self.display(f"NEW HIGH SCORE! Final Score: {final_score}")
            else:
                self.display(f"Game Over! Final Score: {final_score}. Leaderboard Position: {position}")

            # Notify the player of the saved score
            QMessageBox.information(self, "Score Saved", f"Your score has been saved as '{name.strip()}'!")
        else:
            # Player chooses not to save their score
            self.display(f"Game Over! Final Score: {self.game.score}. Score not saved.")

        # Disable all buttons and prepare UI for replay or exit
        self.disable_all_buttons()
        self.menu_button_endgame()


########## HELPER FUNCTIONS ##############

    def update_ui(self, no_deck=False):
        """
        Refresh the UI elements to match the current game state.
        
        Args:
            no_card (bool): If a deck has not yet been initialised.
        """
        self.score_value.setText(str(self.game.score))
        self.unbanked_points_value.setText(str(self.game.unbanked_points))
        self.streak_value.setText(str(self.game.streak))
        self.lives_left_value.setText(str(self.game.lives))

        if not no_deck:
            # If a deck has been initialised
            if self.game.card:
                # Update the card image if a card is available
                card_image_path = self.get_card_image_path(self.game.card)
                self.card_image.setPixmap(QPixmap(card_image_path))
            else:
                # Clear the card image if no card is available
                self.card_image.clear()
        else:
            # If there is no deck initialised, clear the image
            self.card_image.clear()

    def get_card_image_path(self, card):
        """
        Generate the file path for the given card's image.
        
        Args:
            card (Card): The card object for which the image path is needed.
        Returns:
            str: The path to the card's image file.
        """
        filename = card.getImageName()
        card_path = os.path.join(self.dirpath, fr"card-images\{filename}")
        return card_path

    def display(self, text):
        """
        Update the main display line in the GUI with the given text.
        
        Args:
            text (str): The message to display.
        """
        self.display_line.setText(text)
