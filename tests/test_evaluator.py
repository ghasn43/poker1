"""
Tests for hand evaluator.
"""

import unittest
from core.cards import Card
from core.evaluator import HandEvaluator
from utils.constants import (
    HAND_HIGH_CARD,
    HAND_ONE_PAIR,
    HAND_TWO_PAIR,
    HAND_THREE_OF_A_KIND,
    HAND_STRAIGHT,
    HAND_FLUSH,
    HAND_FULL_HOUSE,
    HAND_FOUR_OF_A_KIND,
    HAND_STRAIGHT_FLUSH,
)


class TestHandEvaluator(unittest.TestCase):
    """Test hand evaluation logic."""

    def test_high_card(self):
        """Test high card evaluation."""
        cards = [
            Card("A", "S"),
            Card("K", "H"),
            Card("Q", "D"),
            Card("J", "C"),
            Card("9", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_HIGH_CARD)

    def test_one_pair(self):
        """Test one pair."""
        cards = [
            Card("A", "S"),
            Card("A", "H"),
            Card("K", "D"),
            Card("Q", "C"),
            Card("J", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_ONE_PAIR)
        self.assertEqual(kickers[0], 14)  # Aces

    def test_two_pair(self):
        """Test two pair."""
        cards = [
            Card("A", "S"),
            Card("A", "H"),
            Card("K", "D"),
            Card("K", "C"),
            Card("Q", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_TWO_PAIR)

    def test_three_of_a_kind(self):
        """Test three of a kind."""
        cards = [
            Card("A", "S"),
            Card("A", "H"),
            Card("A", "D"),
            Card("K", "C"),
            Card("Q", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_THREE_OF_A_KIND)

    def test_straight(self):
        """Test straight."""
        cards = [
            Card("A", "S"),
            Card("K", "H"),
            Card("Q", "D"),
            Card("J", "C"),
            Card("T", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_STRAIGHT)
        self.assertEqual(kickers[0], 14)  # Ace high

    def test_wheel_straight(self):
        """Test wheel (A-2-3-4-5) straight."""
        cards = [
            Card("A", "S"),
            Card("5", "H"),
            Card("4", "D"),
            Card("3", "C"),
            Card("2", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_STRAIGHT)
        self.assertEqual(kickers[0], 5)  # 5 high for wheel

    def test_flush(self):
        """Test flush."""
        cards = [
            Card("A", "S"),
            Card("K", "S"),
            Card("Q", "S"),
            Card("J", "S"),
            Card("9", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_FLUSH)

    def test_full_house(self):
        """Test full house."""
        cards = [
            Card("A", "S"),
            Card("A", "H"),
            Card("A", "D"),
            Card("K", "C"),
            Card("K", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_FULL_HOUSE)

    def test_four_of_a_kind(self):
        """Test four of a kind."""
        cards = [
            Card("A", "S"),
            Card("A", "H"),
            Card("A", "D"),
            Card("A", "C"),
            Card("K", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_FOUR_OF_A_KIND)

    def test_straight_flush(self):
        """Test straight flush."""
        cards = [
            Card("A", "S"),
            Card("K", "S"),
            Card("Q", "S"),
            Card("J", "S"),
            Card("T", "S"),
        ]
        rank, kickers = HandEvaluator.evaluate_5_card_hand(cards)[:2]
        self.assertEqual(rank, HAND_STRAIGHT_FLUSH)

    def test_best_hand_from_7(self):
        """Test finding best hand from 7 cards."""
        hole = [Card("A", "S"), Card("K", "S")]
        community = [Card("Q", "S"), Card("J", "S"), Card("T", "S"), Card("9", "H"), Card("8", "H")]

        rank, kickers, best_cards = HandEvaluator.best_hand_from_7(hole, community)
        # Should find the royal flush in all spades
        self.assertEqual(rank, HAND_STRAIGHT_FLUSH)
        self.assertEqual(len(best_cards), 5)


if __name__ == "__main__":
    unittest.main()
