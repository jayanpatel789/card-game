from games.higherOrLower import HigherOrLower
from leaderboard.leaderboard import Leaderboard
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDialog, QVBoxLayout, QLabel
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

        ## Assign state
        self.current_state = "START_GAME"

        # Connect buttons
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
            pass
    
    def start_game(self):
        """Start the game by drawing the first card."""
        self.game = HigherOrLower()  # Start new game instance
        self.card0 = self.game.draw_card()

        if self.card0:
            self.display(f"The card is: {self.card0}")
            self.update_ui()
            self.guess_button_state()
            self.current_state = "WAIT_FOR_GUESS"
        else:
            self.display("Deck reshuffled. Please try again.")

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
            self.bank_points()
            self.display("You banked! Click next to continue")
            self.next_button_state()
            self.current_state = "WAIT_FOR_GUESS"

    def draw_after_guess(self):
        self.card1 = self.game.draw_card()
        if not self.card1:
            self.display("New deck. Click next to draw")
            self.next_button_state()
            self.current_state = "DRAW_AFTER_GUESS"
            return
        
        if self.card1.rank == 'Joker':
            self.display("You drew a Joker! +1 Life. Click next to draw again")
            self.game.lives += 1
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

    def bank_points(self):
        self.game.bankPoints()
        self.update_ui()


    ########## HELPER FUNCTIONS ##############

    def update_ui(self):
        """Update the UI based on the current game state."""
        self.score_value.setText(str(self.game.score))
        self.unbanked_points_value.setText(str(self.game.unbanked_points))
        self.streak_value.setText(str(self.game.streak))
        self.lives_left_value.setText(str(self.game.lives))

        # Update the displayed card
        if self.game.card:
            card_image_path = self.get_card_image_path(self.game.card)
            self.card_image.setPixmap(QPixmap(card_image_path))
        else:
            self.card_image.clear()

    def get_card_image_path(self, card):
        """Return the file path for a card's image."""
        filename = card.getImageName()
        card_path = os.path.join(self.dirpath, fr"card-images\{filename}")
        return card_path
    
    def display(self, text):
        self.display_line.setText(text)

