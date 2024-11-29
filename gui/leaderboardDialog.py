from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QIcon
import os
from datetime import datetime

class LeaderboardDialog(QDialog):
    def __init__(self, leaderboard):
        super(LeaderboardDialog, self).__init__()
        self.leaderboard = leaderboard

        # Initalise window
        self.setWindowTitle("Leaderboard")
        self.setGeometry(300, 100, 425, 500)
        self.setFixedSize(425, 500)
        # Set the window icon
        dirpath = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(dirpath, r"card-images\ace_of_hearts.png")
        self.setWindowIcon(QIcon(icon_path))

        # Layout for the dialog
        layout = QVBoxLayout()

        # Stylesheet
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

        # Add the table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Date", "Name", "Score"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        self.populate_table()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def populate_table(self):
        """Fetch and populate leaderboard data into the table."""
        scores = self.leaderboard.get_top_scores()
        self.table.setRowCount(len(scores))

        for row, (date, name, score) in enumerate(scores):
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%y")
            self.table.setItem(row, 0, QTableWidgetItem(formatted_date))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(str(score)))
