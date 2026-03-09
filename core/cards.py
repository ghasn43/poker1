"""
Card and Deck classes for poker.
"""

from typing import List, Tuple
from utils.constants import SUITS, RANKS, RANK_VALUES


class Card:
    """Represents a single playing card."""

    def __init__(self, rank: str, suit: str) -> None:
        """
        Initialize a card.

        Args:
            rank: Card rank ('2' through 'A')
            suit: Card suit ('S', 'H', 'D', 'C')
        """
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in ("S", "H", "D", "C"):
            raise ValueError(f"Invalid suit: {suit}")

        self.rank = rank
        self.suit = suit

    @property
    def suit_symbol(self) -> str:
        """Return the symbol for the suit."""
        suit_map = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}
        return suit_map[self.suit]

    @property
    def rank_value(self) -> int:
        """Return the numeric value of the rank."""
        return RANK_VALUES[self.rank]

    def __str__(self) -> str:
        """Return pretty string representation like 'A♠'."""
        return f"{self.rank}{self.suit_symbol}"

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Card({self.rank}{self.suit})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another card."""
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self) -> int:
        """Return hash for card (allows use in sets and dicts)."""
        return hash((self.rank, self.suit))

    def __lt__(self, other: "Card") -> bool:
        """Compare cards by rank value."""
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank_value < other.rank_value


class Deck:
    """Represents a 52-card poker deck."""

    def __init__(self) -> None:
        """Initialize a full deck."""
        self.cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        """Reset deck to a full 52 cards."""
        self.cards = [Card(rank, suit) for rank in RANKS for suit in ("S", "H", "D", "C")]

    def shuffle(self) -> None:
        """Shuffle the deck in place."""
        import random

        random.shuffle(self.cards)

    def deal_one(self) -> Card:
        """
        Deal and remove one card from the deck.

        Returns:
            The dealt card.

        Raises:
            ValueError: If deck is empty.
        """
        if not self.cards:
            raise ValueError("Cannot deal from empty deck")
        return self.cards.pop()

    def deal_many(self, count: int) -> List[Card]:
        """
        Deal and remove multiple cards from the deck.

        Args:
            count: Number of cards to deal.

        Returns:
            List of dealt cards.

        Raises:
            ValueError: If not enough cards in deck.
        """
        if count > len(self.cards):
            raise ValueError(f"Not enough cards to deal {count} cards")
        dealt = [self.deal_one() for _ in range(count)]
        return dealt

    def __len__(self) -> int:
        """Return number of cards remaining in deck."""
        return len(self.cards)
