from games.higherOrLower import HigherOrLower
from gui.leaderboardDialog import LeaderboardDialog
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel
from PyQt5.uic import loadUi
import os

class HomeUI(QMainWindow):
    """
    Represents the main home screen for the Higher or Lower: Point Rush game.
    Provides navigation to view game rules and leaderboard using a PyQt5 GUI.
    """

    def __init__(self, leaderboard):
        """
        Initialises the home screen UI, loading the UI file and setting up navigation buttons.

        Args:
            leaderboard (Leaderboard): Instance of the leaderboard to display scores.
        """
        super(HomeUI, self).__init__()

        # Define the path to the UI file
        dirpath = os.path.dirname(os.path.abspath(__file__))
        UIpath = os.path.join(dirpath, r"ui\home_screen.ui")
        print(UIpath)

        # Load the UI file
        loadUi(UIpath, self)

        # Set the title of the main window
        self.setWindowTitle("Higher or Lower: Point Rush")

        # Initialise the leaderboard
        self.leaderboard = leaderboard

        # Connect buttons to their respective actions
        self.rulesButton.clicked.connect(self.showRules)          # Show game rules
        self.leaderboardButton.clicked.connect(self.showLeaderboard)  # Show leaderboard

    def showRules(self):
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

    def showLeaderboard(self):
        """
        Displays the leaderboard in a custom dialog window.

        - Creates an instance of the LeaderboardDialog with the current leaderboard.
        - Executes the dialog to allow user interaction.
        """
        # Create and display the leaderboard dialog
        dialog = LeaderboardDialog(self.leaderboard)
        dialog.exec_()
