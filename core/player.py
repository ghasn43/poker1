"""
Player class for poker.
"""

from typing import List, Optional
from core.cards import Card
from utils.constants import AI_STYLE_BALANCED


class Player:
    """Represents a poker player."""

    def __init__(
        self,
        name: str,
        stack: int,
        is_ai: bool = False,
        ai_style: str = AI_STYLE_BALANCED,
    ) -> None:
        """
        Initialize a player.

        Args:
            name: Player name.
            stack: Starting chip count.
            is_ai: Whether this is an AI player.
            ai_style: AI style preference (only relevant if is_ai=True).
        """
        self.name = name
        self.stack = stack
        self.is_ai = is_ai
        self.ai_style = ai_style

        # Hand state
        self.hole_cards: List[Card] = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def receive_cards(self, cards: List[Card]) -> None:
        """Receive hole cards."""
        self.hole_cards = cards.copy()

    def reset_hand(self) -> None:
        """Reset state for a new hand."""
        self.hole_cards = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def place_bet(self, amount: int) -> int:
        """
        Place a bet, returning actual amount bet (may be less if all-in).

        Args:
            amount: Desired bet amount.

        Returns:
            Actual amount bet.
        """
        actual_bet = min(amount, self.stack)
        self.stack -= actual_bet
        self.current_bet += actual_bet

        if self.stack == 0:
            self.all_in = True

        return actual_bet

    def fold(self) -> None:
        """Fold the hand."""
        self.folded = True

    def win_pot(self, amount: int) -> None:
        """Add pot winnings to stack."""
        self.stack += amount

    def get_remaining_hand_value(self) -> int:
        """Get the value of best 5-card hand from hole + community (cached elsewhere)."""
        # This will be calculated by game engine, not here
        pass

    def has_cards(self) -> bool:
        """Check if player has hole cards."""
        return len(self.hole_cards) == 2

    def __repr__(self) -> str:
        """String representation."""
        return f"Player({self.name}, stack={self.stack}, {'AI' if self.is_ai else 'Human'})"
