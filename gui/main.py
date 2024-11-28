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


class PlayUI(QMainWindow):
    def __init__(self):
        super(PlayUI, self).__init__()
        dirpath = os.path.dirname(os.path.abspath(__file__))
        UIpath = os.path.join(dirpath, r"ui\play_screen.ui")
        print(UIpath)
        loadUi(UIpath, self)


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        # Set initial window size and make it fixed
        self.setGeometry(100, 100, 1116, 673)
        self.setFixedSize(1116, 673)
        # Set the window icon
        dirpath = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(dirpath, r"card-images\ace_of_hearts.png")
        self.setWindowIcon(QIcon(icon_path))
        # Create QStackedWidget to hold different screens
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        # Create instances of the screens
        self.homeUI = HomeUI()
        self.playUI = PlayUI()
        # Add screens to the QStackedWidget
        self.stack.addWidget(self.homeUI)  # Index 0
        self.stack.addWidget(self.playUI)  # Index 1

        # Initialise buttons that change windows
        self.homeUI.playButton.clicked.connect(self.showPlayUI)

        # Show the initial screen
        self.showHomeUI()

    def showHomeUI(self):
        # Set current index to HomeUI (index 0)
        self.stack.setCurrentIndex(0)

    def showPlayUI(self):
        # Set current index to PlayUI (index 1)
        self.stack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = AppWindow()
    mainWindow.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("Exiting...", e)