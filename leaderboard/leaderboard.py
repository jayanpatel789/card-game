import sqlite3
from datetime import datetime

class Leaderboard:
    """
    Manages the leaderboard by storing, retrieving, and displaying high scores using an SQLite database.
    """

    def __init__(self, db_path='leaderboard.db'):
        """
        Initialise the leaderboard with a specified database path.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.display_no = 10  # Number of top scores to display
        self.conn = sqlite3.connect(self.db_path)  # Establish connection to the database
        self.create_table()  # Ensure the leaderboard table exists

    def create_table(self):
        """
        Create the leaderboard table if it does not already exist.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL
                )
            """)  # Define table schema for storing scores
    
    def add_score(self, name, score):
        """
        Add a new score to the leaderboard.

        Args:
            name (str): Name of the player.
            score (int): Score achieved by the player.
        Returns:
            int: The rank of the newly added score.
        """
        current_date = datetime.now()
        date = current_date.strftime("%Y-%m-%d")  # Format date for storage

        with self.conn:
            self.conn.execute(
                "INSERT INTO leaderboard (date, name, score) VALUES (?, ?, ?)",
                (date, name, score)
            )

        # Determine the rank of the newly added score
        position = self.conn.execute("""
            SELECT COUNT(*)
            FROM leaderboard
            WHERE score > ?
               OR (score = ? AND date > ?)
        """, (score, score, date)).fetchone()[0] + 1  # Add 1 for 1-based ranking

        return position

    def get_top_scores(self, limit=10):
        """
        Retrieve the top scores from the leaderboard.

        Args:
            limit (int): The maximum number of scores to retrieve. Defaults to 10.
        Returns:
            list: A list of tuples containing (date, name, score) for each top score.
        """
        limit = self.display_no
        with self.conn:
            return self.conn.execute("""
                SELECT date, name, score
                FROM leaderboard
                ORDER BY score DESC, date DESC
                LIMIT ?
            """, (limit,)).fetchall()  # Retrieve scores in descending order

    def display_leaderboard(self):
        """
        Print the leaderboard to the console in a formatted style.
        """
        print("\n\n######## Leaderboard ########:")
        scores = self.get_top_scores()
        for i, (date, name, score) in enumerate(scores, start=1):
            # Format the date for display
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%y")
            print(f"{i}. {formatted_date} | {name} | {score}")
        print("#############################:")

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

def test():
    """
    Test the Leaderboard class by adding scores, displaying the leaderboard, and closing the database connection.
    """
    leaderboard = Leaderboard(db_path="leaderboard/test_leaderboard.db")

    # Add scores for testing
    leaderboard.add_score("Al", 25)
    leaderboard.add_score("Bob", 30)

    # Display the leaderboard
    leaderboard.display_leaderboard()

    # Close the database connection
    leaderboard.close()


if __name__ == "__main__":
    test()
