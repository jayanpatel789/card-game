class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rank_names = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        rank_str = rank_names.get(self.rank, self.rank)
        return f"{rank_str} of {self.suit}"
    
    def __repr__(self):
        rank_names = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        rank_str = rank_names.get(self.rank, self.rank)
        return f"Card('{rank_str}', '{self.suit}')"
    
    def __lt__(self, other):
        """Less than: Compare if card is less than another card"""
        if not isinstance(other, Card):
            return ValueError('Non Card object used in comparison.')
        return self.rank < other.rank
    
    def __gt__(self, other):
        """Greater than: Compare if card is greater than another card"""
        if not isinstance(other, Card):
            return ValueError('Non Card object used in comparison.')
        return self.rank > other.rank
    
    def __eq__(self, other):
        """Equal to: Compare if card is equal to another card"""
        if not isinstance(other, Card):
            return ValueError('Non Card object used in comparison.')
        return self.rank == other.rank
        