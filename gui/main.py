from gui.homeUI import HomeUI
from gui.playUI import PlayUI
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import sys
import os

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
        self.playUI.home_button.clicked.connect(self.quit_game)

        # Show the initial screen
        self.showHomeUI()

    def showHomeUI(self):
        """Show the HomeUI."""
        self.stack.setCurrentIndex(0)

    def showPlayUI(self):
        """Show the PlayUI."""
        self.stack.setCurrentWidget(self.playUI)

    def quit_game(self):
        """Return to the HomeUI from PlayUI and reinitialise PlayUI."""
        # Switch to the HomeUI
        self.stack.setCurrentWidget(self.homeUI)

        # Reinitialize PlayUI
        self.playUI = PlayUI()
        self.stack.addWidget(self.playUI)  # Add the new PlayUI to the stack
        self.playUI.home_button.clicked.connect(self.quit_game)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = AppWindow()
    mainWindow.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("Exiting...", e)