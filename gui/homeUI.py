from games.higherOrLower import HigherOrLower
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import sys
import os

class HomeUI(QMainWindow):
    def __init__(self):
        super(HomeUI, self).__init__()
        dirpath = os.path.dirname(os.path.abspath(__file__))
        UIpath = os.path.join(dirpath, r"ui\home_screen.ui")
        print(UIpath)
        loadUi(UIpath, self)

        # Connect buttons for navigation
        self.rulesButton.clicked.connect(self.showRules)

    def showRules(self):
        # Retrieve the rules from the game instance
        # Initialise game for rules
        self.game = HigherOrLower()
        rules = self.game.getRules()

        # Create a QDialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Rules")
        dialog.setGeometry(200, 200, 800, 400)  # Set the size of the dialog

        # Add a QLabel to display the rules
        layout = QVBoxLayout(dialog)
        label = QLabel(rules, dialog)
        label.setWordWrap(True)  # Enable text wrapping
        layout.addWidget(label)

        # Apply a stylesheet to customize the font
        label.setStyleSheet("color: white; font-size: 16px; font-family: Arial;")

        dialog.exec_()  # Show the dialog
