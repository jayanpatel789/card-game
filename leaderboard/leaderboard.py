import sqlite3
from datetime import datetime

class Leaderboard:
    def __init__(self, db_path='leaderboard.db'):
        self.db_path = db_path
        self.display_no = 10
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL
                )
            """)
    
    def add_score(self, name, score):
        """Add a new score to the leaderboard."""
        current_date = datetime.now()
        date = current_date.strftime("%Y-%m-%d")

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
        limit=self.display_no
        with self.conn:
            return self.conn.execute("""
                SELECT date, name, score
                FROM leaderboard
                ORDER BY score DESC, date DESC
                LIMIT ?
            """, (limit,)).fetchall()
        
    def display_leaderboard(self):
        print("\n\n######## Leaderboard ########:")
        scores = self.get_top_scores()
        for i, (date, name, score) in enumerate(scores, start=1):
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%y")
            print(f"{i}. {formatted_date} | {name} | {score}")
        print("#############################:")

    def close(self):
        self.conn.close()

def test():
    leaderboard = Leaderboard(db_path="leaderboard/test_leaderboard.db")

    # Add scores
    leaderboard.add_score("Al", 25)
    leaderboard.add_score("Bob", 30)

    # Display leaderboard
    leaderboard.display_leaderboard()

    # Close the database connection
    leaderboard.close()


if __name__ == "__main__":
    test()