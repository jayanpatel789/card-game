class Card:
    """
    Represents a playing card with a rank and suit. 

    Attributes:
        rank (str): The rank of the card, which can be a number (e.g., '2') or a face card ('1' for Ace, '11' for Jack, '12' for Queen, '13' for King). 
                    For Jokers, rank is 'Joker'.
        suit (str): The suit of the card, such as 'Hearts', 'Diamonds', 'Clubs', or 'Spades'.
    """

    def __init__(self, rank, suit):
        """
        Initializes a Card object with a given rank and suit.

        Args:
            rank (str): The rank of the card.
            suit (str): The suit of the card.
        """
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Provides a human-readable string representation of the card.

        Returns:
            str: The formatted string representation, such as "Ace of Hearts" or "Red Joker".
        """
        if self.rank == 'Joker':
            return f"{self.suit} {self.rank}"
        else:
            rank_names = {'1': "Ace", '11': "Jack", '12': "Queen", '13': "King"}
            rank_str = rank_names.get(self.rank, self.rank)
            return f"{rank_str} of {self.suit}"
    
    def __repr__(self):
        """
        Provides a developer-friendly representation of the card.

        Returns:
            str: A string representation in the format Card('<Rank>', '<Suit>').
        """
        rank_names = {'1': "Ace", '11': "Jack", '12': "Queen", '13': "King"}
        rank_str = rank_names.get(self.rank, self.rank)
        return f"Card('{rank_str}', '{self.suit}')"
    
    def __lt__(self, other):
        """
        Determines if the current card is less than another card based on rank.

        Args:
            other (Card): Another Card object to compare against.
        Returns:
            bool: True if the current card's rank is less than the other card's rank, False otherwise.
        Raises:
            ValueError: If the other object is not an instance of Card.
        """
        if not isinstance(other, Card):
            return ValueError('Non Card object used in comparison.')
        return int(self.rank) < int(other.rank)
    
    def __gt__(self, other):
        """
        Determines if the current card is greater than another card based on rank.

        Args:
            other (Card): Another Card object to compare against.
        Returns:
            bool: True if the current card's rank is greater than the other card's rank, False otherwise.
        Raises:
            ValueError: If the other object is not an instance of Card.
        """
        if not isinstance(other, Card):
            return ValueError('Non Card object used in comparison.')
        return int(self.rank) > int(other.rank)
    
    def __eq__(self, other):
        """
        Checks if the current card is equal to another card based on rank.

        Args:
            other (Card): Another Card object to compare against.
        Returns:
            bool: True if the ranks of the two cards are equal, False otherwise.
        Raises:
            ValueError: If the other object is not an instance of Card.
        """
        if not isinstance(other, Card):
            return ValueError('Non Card object used in comparison.')
        return int(self.rank) == int(other.rank)
    
    def getImageName(self):
        """
        Generates the file name for the card's image representation within gui/card-images folder

        Returns:
            str: The file name, formatted as '<rank>_of_<suit>.png' for regular cards or '<suit>_joker.png' for Jokers.
        """
        if self.rank == 'Joker':
            return f"{self.suit}_{self.rank}.png".lower()
        else:
            rank_names = {'1': "Ace", '11': "Jack", '12': "Queen", '13': "King"}
            rank_str = rank_names.get(self.rank, self.rank)
            return f"{rank_str}_of_{self.suit}.png".lower()


def test():
    """
    A test function to test the Card class functionality.
    """
    pass
    

if __name__ == "__main__":
    test()
