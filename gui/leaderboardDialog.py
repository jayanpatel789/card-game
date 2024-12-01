from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QIcon
import os
from datetime import datetime

class LeaderboardDialog(QDialog):
    """
    Represents a dialog window to display the leaderboard with top scores.
    """

    def __init__(self, leaderboard):
        """
        Initialise the leaderboard dialog, setting up the window, layout, and styles.

        Args:
            leaderboard (Leaderboard): An instance of the leaderboard to fetch and display scores.
        """
        super(LeaderboardDialog, self).__init__()
        self.leaderboard = leaderboard

        # Configure the dialog window
        self.setWindowTitle("Leaderboard")
        self.setGeometry(300, 100, 425, 500)  # Position and size of the dialog
        self.setFixedSize(425, 500)  # Fixed size to prevent resizing

        # Set the window icon
        dirpath = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(dirpath, r"card-images\ace_of_hearts.png")
        self.setWindowIcon(QIcon(icon_path))

        # Create a vertical layout for the dialog content
        layout = QVBoxLayout()

        # Apply stylesheet for consistent styling
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(0, 118, 0);
            }
            QLabel {
                color: white;
                font-size: 26px;
                font-family: Bodoni MT;
                text-align: center;
            }
            QTableWidget {
                background-color: rgb(0, 118, 0);
                gridline-color: rgb(200, 200, 200);
                color: white;
                font-size: 20px;
                font-family: Bodoni MT;
                border: 1px solid rgb(0, 0, 0);
            }
            QHeaderView::section {
                background-color: rgb(200, 200, 200);
                font-weight: bold;
            }
        """)

        # Add a label for the title
        title_label = QLabel("Top 10 Leaderboard")
        layout.addWidget(title_label)

        # Create and configure the leaderboard table
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Columns for Date, Name, and Score
        self.table.setHorizontalHeaderLabels(["Date", "Name", "Score"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        self.populate_table()  # Populate table with leaderboard data
        layout.addWidget(self.table)

        # Set the dialog layout
        self.setLayout(layout)

    def populate_table(self):
        """
        Fetch and populate leaderboard data into the table.
        """
        scores = self.leaderboard.get_top_scores()  # Retrieve the top scores
        self.table.setRowCount(len(scores))  # Set the number of rows in the table

        # Populate each row with date, name, and score
        for row, (date, name, score) in enumerate(scores):
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%y")  # Format the date
            self.table.setItem(row, 0, QTableWidgetItem(formatted_date))  # Date column
            self.table.setItem(row, 1, QTableWidgetItem(name))  # Name column
            self.table.setItem(row, 2, QTableWidgetItem(str(score)))  # Score column
