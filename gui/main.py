from gui.homeUI import HomeUI
from gui.playUI import PlayUI
from leaderboard.leaderboard import Leaderboard
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import sys
import os

class AppWindow(QMainWindow):
    """
    Main application window for Higher or Lower: Point Rush.
    Manages transitions between HomeUI and PlayUI using QStackedWidget.
    """

    def __init__(self):
        """
        Initialises the main application window, sets up UI screens, and manages navigation.
        """
        super(AppWindow, self).__init__()
        # Set fixed window size and initial geometry
        self.setGeometry(100, 100, 1116, 673)
        self.setFixedSize(1116, 673)

        # Set the window icon
        dirpath = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(dirpath, r"card-images\ace_of_hearts.png")
        self.setWindowIcon(QIcon(icon_path))

        # Create a QStackedWidget to manage multiple screens
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialise leaderboard instance
        self.leaderboard = Leaderboard(db_path="leaderboard.db")

        # Create instances of the home and play screens
        self.homeUI = HomeUI(self.leaderboard)
        self.playUI = PlayUI(self.leaderboard)

        # Add the screens to the stack
        self.stack.addWidget(self.homeUI)  # Index 0
        self.stack.addWidget(self.playUI)  # Index 1

        # Connect buttons for screen transitions
        self.homeUI.playButton.clicked.connect(self.showPlayUI)  # Navigate to PlayUI
        self.playUI.home_button.clicked.connect(self.quit_game)  # Return to HomeUI

        # Show the initial screen (HomeUI)
        self.showHomeUI()

    def showHomeUI(self):
        """Switch to the HomeUI screen."""
        self.stack.setCurrentIndex(0)  # Set the current screen to HomeUI
        self.setWindowTitle("Higher or Lower: Point Rush")  # Update the window title

    def showPlayUI(self):
        """Switch to the PlayUI screen."""
        self.stack.setCurrentWidget(self.playUI)  # Set the current screen to PlayUI
        self.setWindowTitle("Higher or Lower: Point Rush")  # Update the window title

    def quit_game(self):
        """
        Return to the HomeUI from the PlayUI and reinitialise the PlayUI.
        This ensures that the game state resets each time the user quits to the home screen.
        """
        # Switch back to the HomeUI
        self.stack.setCurrentWidget(self.homeUI)

        # Reinitialise the PlayUI for a new game
        self.playUI = PlayUI(self.leaderboard)
        self.stack.addWidget(self.playUI)  # Add the new PlayUI instance to the stack
        self.playUI.home_button.clicked.connect(self.quit_game)  # Reconnect the home button

if __name__ == "__main__":
    # Create the PyQt application
    app = QApplication(sys.argv)
    mainWindow = AppWindow()  # Instantiate the main application window
    mainWindow.show()  # Show the main window
    try:
        sys.exit(app.exec_())  # Start the event loop
    except Exception as e:
        # Handle unexpected exceptions during application exit
        print("Exiting...", e)
