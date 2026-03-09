"""
Tests for game logic.
"""

import unittest
from core.player import Player
from core.game import PokerGame
from core.cards import Card


class TestPokerGame(unittest.TestCase):
    """Test game logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.human = Player("Human", 1000)
        self.ai = Player("AI", 1000, is_ai=True)
        self.game = PokerGame(self.human, self.ai, small_blind=5, big_blind=10)

    def test_game_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.pot, 0)
        self.assertEqual(self.game.hand_number, 0)

    def test_start_new_hand(self):
        """Test starting a new hand."""
        self.game.start_new_hand()

        # Hand should be initialized
        self.assertEqual(self.game.hand_number, 1)
        self.assertEqual(self.game.pot, 15)  # Small blind (5) + Big blind (10)

        # Players should have hole cards
        self.assertEqual(len(self.game.human.hole_cards), 2)
        self.assertEqual(len(self.game.ai.hole_cards), 2)

        # Deck should have 48 cards remaining
        self.assertEqual(len(self.game.deck.cards), 48)

    def test_blinds_posted(self):
        """Test that blinds are posted correctly."""
        self.game.start_new_hand()

        # In heads-up: button has small blind
        if self.game.button_position == 0:
            self.assertEqual(self.game.human.current_bet, 5)
            self.assertEqual(self.game.ai.current_bet, 10)
        else:
            self.assertEqual(self.game.ai.current_bet, 5)
            self.assertEqual(self.game.human.current_bet, 10)

    def test_first_action_preflop(self):
        """Test that first player acts first preflop."""
        self.game.start_new_hand()
        # In heads-up, button (small blind) acts first preflop
        if self.game.button_position == 0:
            self.assertEqual(self.game.active_player, self.game.human)
        else:
            self.assertEqual(self.game.active_player, self.game.ai)

    def test_player_fold(self):
        """Test player folding."""
        self.game.start_new_hand()

        # Save initial pot
        initial_pot = self.game.pot

        # Current player folds
        player = self.game.active_player
        self.game.process_player_action("fold")

        # Player should be marked as folded
        self.assertTrue(player.folded)

        # Hand should be over
        self.assertTrue(self.game.is_hand_over())

    def test_match_over_when_busted(self):
        """Test match ends when player runs out of chips."""
        self.game.human.stack = 0
        self.assertTrue(self.game.is_match_over())

        self.game.ai.stack = 0
        self.assertTrue(self.game.is_match_over())


if __name__ == "__main__":
    unittest.main()
