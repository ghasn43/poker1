"""
AI decision-making for poker.
"""

import random
from typing import List, Tuple, Optional
from core.player import Player
from core.cards import Card
from core.evaluator import HandEvaluator
from core.betting import BettingRound
from utils.monte_carlo import estimate_win_probability, estimate_hand_strength
from utils.constants import (
    AI_STYLE_TIGHT,
    AI_STYLE_BALANCED,
    AI_STYLE_AGGRESSIVE,
    AI_THRESHOLDS,
    STREET_PREFLOP,
    STREET_FLOP,
    STREET_TURN,
    STREET_RIVER,
    ACTION_FOLD,
    ACTION_CHECK,
    ACTION_CALL,
    ACTION_RAISE,
    ACTION_BET,
)


class PokerAI:
    """AI decision-maker for poker."""

    def __init__(self, ai_style: str = AI_STYLE_BALANCED):
        """Initialize AI."""
        self.style = ai_style
        self._validate_style()

    def _validate_style(self) -> None:
        """Validate AI style is recognized."""
        if self.style not in AI_THRESHOLDS:
            raise ValueError(f"Unknown AI style: {self.style}")

    def decide(
        self,
        ai_player: Player,
        opponent_player: Player,
        community_cards: List[Card],
        current_bet_level: int,
        pot_size: int,
        street: str,
        action_history: List[Tuple],
        min_raise: int = 1,
    ) -> Tuple[str, int, str]:
        """
        Decide AI action.

        Args:
            ai_player: The AI player.
            opponent_player: The human opponent.
            community_cards: Current board cards.
            current_bet_level: Current bet in this street.
            pot_size: Total pot size.
            street: Current street (preflop, flop, etc).
            action_history: History of actions this hand.
            min_raise: Minimum raise increment.

        Returns:
            Tuple of (action, amount, explanation).
        """
        legal_actions = BettingRound.legal_actions(
            ai_player, current_bet_level, has_bet=True
        )

        if not legal_actions:
            return (ACTION_CHECK, 0, "No legal actions available")

        # Estimate hand strength
        if street == STREET_PREFLOP:
            hand_strength = self._preflop_hand_strength(ai_player.hole_cards)
            explanation = f"Preflop hand: {self._describe_hand(ai_player.hole_cards)}"
        else:
            # Use Monte Carlo for postflop
            hand_strength = estimate_hand_strength(
                ai_player.hole_cards, community_cards, num_simulations=500
            )
            explanation = f"Postflop equity: {hand_strength*100:.1f}%"

        # Check pot odds if facing a bet
        pot_odds = self._calculate_pot_odds(
            ai_player, opponent_player, current_bet_level, pot_size
        )

        # Decide action based on strength and odds
        action, amount = self._choose_action(
            hand_strength,
            pot_odds,
            street,
            ai_player,
            opponent_player,
            current_bet_level,
            legal_actions,
            action_history,
        )

        # Build explanation
        explanation = self._build_explanation(
            action,
            hand_strength,
            pot_odds,
            street,
            ai_player.hole_cards,
            community_cards,
        )

        return (action, amount, explanation)

    def _preflop_hand_strength(self, hole_cards: List[Card]) -> float:
        """
        Estimate preflop hand strength using hand groups.

        Returns value 0.0 to 1.0.
        """
        if len(hole_cards) != 2:
            return 0.5

        ranks = sorted([card.rank_value for card in hole_cards], reverse=True)
        is_suited = hole_cards[0].suit == hole_cards[1].suit

        r1, r2 = ranks[0], ranks[1]

        # High card strength
        max_rank = 14  # Ace
        base_strength = (r1 + r2) / (2 * max_rank)

        # Adjustments
        if r1 == r2:  # Pair
            strength = 0.5 + (base_strength * 0.4)
        elif is_suited:  # Suited
            strength = base_strength + 0.1
        else:  # Unsuited
            strength = base_strength

        return min(1.0, max(0.0, strength))

    def _calculate_pot_odds(
        self,
        ai_player: Player,
        opponent: Player,
        current_bet_level: int,
        pot_size: int,
    ) -> float:
        """
        Calculate pot odds (simplified).

        Returns: favorable odds ratio (higher is better).
        """
        call_amount = BettingRound.call_amount(ai_player, current_bet_level)

        if call_amount == 0:
            return 1.0  # No call needed, always favorable

        if pot_size == 0:
            return 0.5

        return pot_size / call_amount

    def _choose_action(
        self,
        hand_strength: float,
        pot_odds: float,
        street: str,
        ai_player: Player,
        opponent: Player,
        current_bet_level: int,
        legal_actions: List[str],
        action_history: List[Tuple],
    ) -> Tuple[str, int]:
        """
        Choose action based on hand strength and odds.

        Returns: (action, amount)
        """
        thresholds = AI_THRESHOLDS[self.style]

        # No bet facing - check or bet
        if current_bet_level == 0 or ai_player.current_bet == current_bet_level:
            if ACTION_CHECK in legal_actions:
                # Consider betting out
                if street == STREET_PREFLOP:
                    if hand_strength > thresholds["preflop_raise_threshold"]:
                        if ACTION_BET in legal_actions:
                            bet_size = max(current_bet_level * 2, ai_player.stack // 20)
                            return (ACTION_BET, min(bet_size, ai_player.stack))
                else:
                    # Postflop aggression
                    if hand_strength > 0.6:
                        if ACTION_BET in legal_actions:
                            bet_size = ai_player.stack // 8
                            return (ACTION_BET, min(bet_size, ai_player.stack))

                return (ACTION_CHECK, 0)

        # Facing a bet - fold, call, or raise
        if ACTION_FOLD in legal_actions:
            if hand_strength < thresholds["postflop_call_threshold"]:
                # Consider bluffing
                bluff_rand = random.random()
                if bluff_rand > (1 - thresholds["bluff_frequency"]):
                    if ACTION_RAISE in legal_actions:
                        raise_size = (current_bet_level * 2)
                        return (
                            ACTION_RAISE,
                            min(raise_size, ai_player.stack + ai_player.current_bet),
                        )

                return (ACTION_FOLD, 0)

        if ACTION_CALL in legal_actions:
            call_amt = BettingRound.call_amount(ai_player, current_bet_level)
            if hand_strength > thresholds["postflop_call_threshold"] or pot_odds > 2.0:
                # Consider raising
                if hand_strength > thresholds["postflop_raise_threshold"]:
                    if ACTION_RAISE in legal_actions:
                        raise_size = current_bet_level * 2
                        return (
                            ACTION_RAISE,
                            min(raise_size, ai_player.stack + ai_player.current_bet),
                        )

                # Call
                return (ACTION_CALL, call_amt)

            # Marginal: fold or call?
            if hand_strength > 0.25 and pot_odds > 1.0:
                return (ACTION_CALL, call_amt)

            return (ACTION_FOLD, 0)

        # Fallback: check if available, else fold
        if ACTION_CHECK in legal_actions:
            return (ACTION_CHECK, 0)

        if ACTION_FOLD in legal_actions:
            return (ACTION_FOLD, 0)

        return (ACTION_CHECK, 0)

    def _build_explanation(
        self,
        action: str,
        hand_strength: float,
        pot_odds: float,
        street: str,
        hole_cards: List[Card],
        community_cards: List[Card],
    ) -> str:
        """Build a human-readable explanation of the AI's decision."""
        hand_desc = self._describe_hand(hole_cards)
        strength_pct = hand_strength * 100

        if action == ACTION_FOLD:
            return f"AI folded: {hand_desc} is weak. Strength: {strength_pct:.1f}%"
        elif action == ACTION_CHECK:
            return f"AI checked with {hand_desc}. Strength: {strength_pct:.1f}%"
        elif action == ACTION_CALL:
            return (
                f"AI called with {hand_desc}. Strength: {strength_pct:.1f}%, "
                f"Pot odds favorable ({pot_odds:.1f}:1)"
            )
        elif action == ACTION_BET or action == ACTION_RAISE:
            return f"AI raised with {hand_desc}. Strength: {strength_pct:.1f}%"
        else:
            return f"AI {action}s with {hand_desc}."

    def _describe_hand(self, hole_cards: List[Card]) -> str:
        """Describe hole cards in English."""
        if len(hole_cards) != 2:
            return "(no cards)"

        r1, r2 = hole_cards[0].rank, hole_cards[1].rank
        suited = "suited" if hole_cards[0].suit == hole_cards[1].suit else "unsuited"

        if r1 == r2:
            return f"Pair of {self._rank_name(r1)}"
        else:
            return f"{self._rank_name(r1)}-{self._rank_name(r2)} {suited}"

    @staticmethod
    def _rank_name(rank: str) -> str:
        """Convert rank letter to name."""
        names = {
            "2": "Twos",
            "3": "Threes",
            "4": "Fours",
            "5": "Fives",
            "6": "Sixes",
            "7": "Sevens",
            "8": "Eights",
            "9": "Nines",
            "T": "Tens",
            "J": "Jacks",
            "Q": "Queens",
            "K": "Kings",
            "A": "Aces",
        }
        return names.get(rank, rank)
