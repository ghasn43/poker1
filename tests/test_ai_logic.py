"""
Tests for AI logic.
"""

import unittest
from core.cards import Card
from core.ai_logic import PokerAI
from core.player import Player
from utils.constants import (
    AI_STYLE_TIGHT,
    AI_STYLE_BALANCED,
    AI_STYLE_AGGRESSIVE,
    STREET_PREFLOP,
)


class TestPokerAI(unittest.TestCase):
    """Test AI decision-making."""

    def test_ai_initialization(self):
        """Test AI initialization."""
        ai = PokerAI(AI_STYLE_BALANCED)
        self.assertEqual(ai.style, AI_STYLE_BALANCED)

    def test_ai_styles(self):
        """Test different AI styles load correctly."""
        for style in [AI_STYLE_TIGHT, AI_STYLE_BALANCED, AI_STYLE_AGGRESSIVE]:
            ai = PokerAI(style)
            self.assertEqual(ai.style, style)

    def test_preflop_hand_strength_pair(self):
        """Test hand strength evaluation for pairs."""
        ai = PokerAI()

        # Pair should be strong
        pair = [Card("A", "S"), Card("A", "H")]
        strength_pair = ai._preflop_hand_strength(pair)

        # High cards should be weaker
        high = [Card("2", "S"), Card("3", "H")]
        strength_high = ai._preflop_hand_strength(high)

        self.assertGreater(strength_pair, strength_high)

    def test_preflop_hand_strength_suited(self):
        """Test hand strength for suited vs unsuited."""
        ai = PokerAI()

        # Suited should be stronger
        suited = [Card("A", "S"), Card("K", "S")]
        unsuited = [Card("A", "S"), Card("K", "H")]

        strength_suited = ai._preflop_hand_strength(suited)
        strength_unsuited = ai._preflop_hand_strength(unsuited)

        self.assertGreater(strength_suited, strength_unsuited)

    def test_ai_decision_has_action(self):
        """Test that AI decide returns a valid action."""
        ai = PokerAI(AI_STYLE_BALANCED)

        human = Player("Human", 1000)
        ai_player = Player("AI", 1000, is_ai=True)

        ai_player.hole_cards = [Card("A", "S"), Card("K", "H")]
        human.hole_cards = [Card("Q", "S"), Card("J", "H")]

        action, amount, explanation = ai.decide(
            ai_player,
            human,
            [],  # No community cards yet
            current_bet_level=10,  # Big blind
            pot_size=15,
            street=STREET_PREFLOP,
            action_history=[],
        )

        # Should return a valid action
        self.assertIn(
            action,
            ["fold", "check", "call", "bet", "raise", "all-in"],
        )

        # Should have an explanation
        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 0)


if __name__ == "__main__":
    unittest.main()
