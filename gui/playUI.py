from games.higherOrLower import HigherOrLower
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import sys
import os
import time

class PlayUI(QMainWindow):
    def __init__(self):
        super(PlayUI, self).__init__()
        self.dirpath = os.path.dirname(os.path.abspath(__file__))
        UIpath = os.path.join(self.dirpath, r"ui\play_screen.ui")
        print(UIpath)
        loadUi(UIpath, self)

        # Define stylesheets
        self.enabled_button_style = "background-color: darkgreen; color: white;"
        self.disabled_button_style = "background-color: gray; color: darkgray;"
        self.enabled_label_style = "color: white"
        self.disabled_label_style = "color: darkgray"

        # Initialise game and state
        self.game = HigherOrLower()  # Start new game instance
        self.current_state = "START_GAME"

        # Connect buttons
        self.restart_button.clicked.connect(self.restart_game)
        self.home_button.clicked.connect(self.quit_to_home)

        self.higher_button.clicked.connect(lambda: self.action("h"))
        self.lower_button.clicked.connect(lambda: self.action("l"))
        self.bank_button.clicked.connect(lambda: self.action("b"))
        self.next_button.clicked.connect(self.advance_state)

        # Widget initialisation
        self.display("Welcome! Click next to draw a card")
        self.next_button_state()

    ######## BUTTON STATE DEFINITIONS ###########
    
    def next_button_state(self):
        """Enable only next button."""
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
        """Enable only the guess and bank buttons."""
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
        """Disable all buttons."""
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

    ######## MENU FUNCTIONS ###########
    def restart_game(self):
        """Restart the game by resetting the state."""
        self.game = HigherOrLower()  # Reset the game instance
        self.update_ui(no_card=True)  # Update the UI with the new game state
        self.display("Game restarted! Click next to draw")
        self.next_button_state()
        self.current_state = "START_GAME"
    
    def quit_to_home(self):
        if hasattr(self, 'return_to_home') and self.return_to_home:
            self.return_to_home()  # Call the callback to return to home
    
    ############ GAME MANAGEMENT ##############
    def advance_state(self):
        """Control the next game state after next button clicked"""
        if self.current_state == "START_GAME":
            self.start_game()
        elif self.current_state == "WAIT_FOR_GUESS":
            self.display(f"The card is: {self.card0}")
            self.guess_button_state()
        elif self.current_state == "DRAW_AFTER_GUESS":
            self.draw_after_guess()
        elif self.current_state == "UPDATE_STATE":
            self.update_state()
        elif self.current_state == "GAME_OVER":
            self.game_over()
    
    def start_game(self):
        """Start the game by drawing the first card."""
        self.card0 = self.game.draw_card()

        if self.card0.rank == 'Joker':
            self.display("You drew a Joker! +1 Life. Click next to draw again")
            self.update_ui()
            self.next_button_state()
            self.current_state = "START_GAME"
        else:
            self.display(f"The card is: {self.card0}")
            self.update_ui()
            self.guess_button_state()
            self.current_state = "WAIT_FOR_GUESS"

    def action(self, signal):
        if signal == 'h':
            self.guess = signal
            self.display("You chose higher! Click next to draw")
            self.next_button_state()
            self.current_state = "DRAW_AFTER_GUESS"
        elif signal == 'l':
            self.guess = signal
            self.display("You chose lower! Click next to draw")
            self.next_button_state()
            self.current_state = "DRAW_AFTER_GUESS"
        else:
            if self.game.unbanked_points > 0:
                self.game.bankPoints()
                self.update_ui()
                self.display("You banked! Click next to continue")
            else:
                self.display("No points to bank! Click next to continue")
            self.next_button_state()
            self.current_state = "WAIT_FOR_GUESS"

    def draw_after_guess(self):
        """Draw the card after a guess and check the answer"""
        self.card1 = self.game.draw_card()
        if not self.card1:
            self.display("New deck - no jokers this time! Click next to draw")
            self.next_button_state()
            self.current_state = "DRAW_AFTER_GUESS"
            return
        
        if self.card1.rank == 'Joker':
            self.display("You drew a Joker! +1 Life. Click next to draw again")
            self.update_ui()
            self.current_state = "DRAW_AFTER_GUESS"
        else:
            self.update_ui()
            result = self.game.checkGuess(self.card0, self.card1, self.guess)
            if result == True:
                self.display(f"The next card is: {self.card1} - you were right!")
                self.current_state = "UPDATE_STATE"
            else:
                self.display(f"The next card is: {self.card1} - tough luck!")
                self.current_state = "UPDATE_STATE"

    def update_state(self):
        """Update the game state depending on result of guess"""
        if self.game.checkGuess(self.card0, self.card1, self.guess):
            points_gained = self.game.correct()
            self.display(f"You earned {points_gained} points! Streak +1")
        else:
            points_lost = self.game.incorrect()
            self.display(f"Lost {points_lost} unbanked points and 1 life.")
        self.update_ui()

        # Check if the game is over
        if self.game.lives <= 0:
            self.current_state = "GAME_OVER"
        else:
            self.card0 = self.card1
            self.current_state = "WAIT_FOR_GUESS"

    def game_over(self):
        """Handle the game-over state."""
        self.display("Game Over! Calculating final score...")

        # Prompt the user for their name
        name, ok = QInputDialog.getText(self, "Game Over", "Enter your name:")
        if ok and name.strip():  # Ensure the player entered a valid name
            final_score, position = self.game.gameOver(name.strip())
            if position == 1:
                self.display(f"NEW HIGH SCORE! Final Score: {final_score}")
            else:
                self.display(f"Game Over! Final Score: {final_score}. Leaderboard Position: {position}")

            # Notify the player
            QMessageBox.information(self, "Score Saved", f"Your score has been saved as '{name.strip()}'!")
        else:
            self.display(f"Game Over! Final Score: {self.game.score}. Score not saved.")

        # Disable all buttons to prevent further interaction
        self.disable_all_buttons()
        self.home_button.setText("Home") # For clarity at end of game


    ########## HELPER FUNCTIONS ##############

    def update_ui(self, no_card=False):
        """Update the UI based on the current game state."""
        self.score_value.setText(str(self.game.score))
        self.unbanked_points_value.setText(str(self.game.unbanked_points))
        self.streak_value.setText(str(self.game.streak))
        self.lives_left_value.setText(str(self.game.lives))

        # Update the displayed card
        if not no_card:
            if self.game.card:
                card_image_path = self.get_card_image_path(self.game.card)
                self.card_image.setPixmap(QPixmap(card_image_path))
            else:
                self.card_image.clear()
        else:
            self.card_image.clear()

    def get_card_image_path(self, card):
        """Return the file path for a card's image."""
        filename = card.getImageName()
        card_path = os.path.join(self.dirpath, fr"card-images\{filename}")
        return card_path
    
    def display(self, text):
        self.display_line.setText(text)

