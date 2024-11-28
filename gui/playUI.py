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

        # Widget initialisation
        self.display("Welcome! Click next to draw a card")
        self.next_button_state()

        # Connect buttons
        self.higher_button.clicked.connect(lambda: self.make_guess("h"))
        self.lower_button.clicked.connect(lambda: self.make_guess("l"))
        # self.bank_button.clicked.connect(self.bank_points)
        self.next_button.clicked.connect(self.start_game)
    
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

    def start_game(self):
        """Start the game by drawing the first card."""
        self.game = HigherOrLower()  # Start new game instance
        self.card0 = self.game.draw_card()

        if self.card0:
            self.display(f"The first card is: {self.card0}")
            self.update_ui()
            self.guess_button_state()
        else:
            self.display("Deck reshuffled. Please try again.")

    def make_guess(self, guess):
        """Handle the player's guess (higher or lower)."""
        self.disable_all_buttons()
        if not self.card0:
            self.display("No card to compare! Draw the first card.")
            return

        if guess == 'h':
            self.display("You chose higher!")
        else:
            self.display("You chose lower!")
        time.sleep(3)

        while True:
            self.display("Drawing card...")
            time.sleep(3)
            self.display("...")
            time.sleep(3)

            card1 = self.game.draw_card()
            if not card1:
                self.display("Deck finished. New deck being shuffled. No jokers this time!")
                time.sleep(3)
                self.display("Will now draw again...")
                time.sleep(3)
            elif card1.rank == 'Joker':
                self.display("You just drew a Joker! +1 Life")
                time.sleep(3)
                self.update_ui()
                self.display("Will now draw again...")
                time.sleep(3)
            else:
                break
            
            self.display(f"{str(self.card1)}!")
            time.sleep(3)

            guess = self.game.checkGuess(self.card0, card1, guess)
            if guess:
                points_gained = self.game.correct()
                print(f"You were right!\n+{points_gained} points, +1 streak")
            else:
                points_lost = self.game.incorrect()
                print(f"\nTough luck, you were wrong!\n{points_lost} unbanked points lost, -1 life")
            self.update_ui()
            # Assign last drawn card to base card
            self.card0 = card1
            time.sleep(3)

        

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

