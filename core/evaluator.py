"""
Hand evaluator for Texas Hold'em poker.
Evaluates 5-card hands and finds best 5-card hand from 7 cards.
"""

from typing import List, Tuple
from collections import Counter
from itertools import combinations
from core.cards import Card
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
    HAND_ROYAL_FLUSH,
    HAND_NAMES,
)


class HandEvaluator:
    """Evaluates and ranks poker hands."""

    @staticmethod
    def evaluate_5_card_hand(cards: List[Card]) -> Tuple[int, Tuple]:
        """
        Evaluate a 5-card hand.

        Args:
            cards: Exactly 5 cards to evaluate.

        Returns:
            Tuple of (hand_rank, tiebreaker_tuple).
            hand_rank is 0-9 (higher is better).
            tiebreaker_tuple contains kickers in descending order.
        """
        if len(cards) != 5:
            raise ValueError("Must evaluate exactly 5 cards")

        is_flush = HandEvaluator._is_flush(cards)
        straight_high = HandEvaluator._get_straight(cards)
        rank_counts = Counter(card.rank_value for card in cards)

        # Check for four of a kind
        four_kind = HandEvaluator._get_four_of_a_kind(rank_counts)
        if four_kind is not None:
            kicker = max(r for r in rank_counts.keys() if r != four_kind)
            return (HAND_FOUR_OF_A_KIND, (four_kind, kicker, 0, 0, 0))

        # Check for full house
        three_kind = HandEvaluator._get_three_of_a_kind(rank_counts)
        if three_kind is not None:
            pair = HandEvaluator._get_pair(rank_counts, exclude=three_kind)
            if pair is not None:
                return (HAND_FULL_HOUSE, (three_kind, pair, 0, 0, 0))

        # Check for flush or straight
        if is_flush and straight_high:
            return (HAND_STRAIGHT_FLUSH, (straight_high, 0, 0, 0, 0))

        if is_flush:
            kickers = tuple(sorted([card.rank_value for card in cards], reverse=True))
            return (HAND_FLUSH, kickers)

        if straight_high:
            return (HAND_STRAIGHT, (straight_high, 0, 0, 0, 0))

        # Check for three of a kind
        if three_kind is not None:
            kickers = sorted([r for r in rank_counts.keys() if r != three_kind], reverse=True)
            return (HAND_THREE_OF_A_KIND, (three_kind,) + tuple(kickers))

        # Check for two pair
        pair = HandEvaluator._get_pair(rank_counts)
        if pair is not None:
            second_pair = HandEvaluator._get_pair(rank_counts, exclude=pair)
            if second_pair is not None:
                high_pair = max(pair, second_pair)
                low_pair = min(pair, second_pair)
                kicker = max(r for r in rank_counts.keys() if r != high_pair and r != low_pair)
                return (HAND_TWO_PAIR, (high_pair, low_pair, kicker, 0, 0))

        # Check for one pair
        if pair is not None:
            kickers = sorted([r for r in rank_counts.keys() if r != pair], reverse=True)
            return (HAND_ONE_PAIR, (pair,) + tuple(kickers))

        # High card
        kickers = tuple(sorted([card.rank_value for card in cards], reverse=True))
        return (HAND_HIGH_CARD, kickers)

    @staticmethod
    def best_hand_from_7(hole_cards: List[Card], community_cards: List[Card]) -> Tuple[int, Tuple, List[Card]]:
        """
        Find the best 5-card hand from 7 cards (hole cards + community).

        Args:
            hole_cards: Player's 2 hole cards.
            community_cards: 3-5 community cards.

        Returns:
            Tuple of (hand_rank, tiebreaker_tuple, best_5_cards_list).
        """
        if len(hole_cards) != 2:
            raise ValueError("Must have exactly 2 hole cards")
        if len(community_cards) > 5:
            raise ValueError("Cannot have more than 5 community cards")

        all_seven = hole_cards + community_cards
        best_hand = None
        best_cards = None

        for five_cards in combinations(all_seven, 5):
            hand = HandEvaluator.evaluate_5_card_hand(list(five_cards))
            if best_hand is None or HandEvaluator._compare_hands(hand, best_hand) > 0:
                best_hand = hand
                best_cards = list(five_cards)

        return best_hand + (best_cards,)

    @staticmethod
    def _is_flush(cards: List[Card]) -> bool:
        """Check if 5 cards form a flush."""
        suits = [card.suit for card in cards]
        return len(set(suits)) == 1

    @staticmethod
    def _get_straight(cards: List[Card]) -> int:
        """
        Check if 5 cards form a straight.

        Returns:
            High card value of straight (5-14), or 0 if no straight.
            Note: Ace can be high (14) or low (1 for A-2-3-4-5).
        """
        ranks = sorted(set(card.rank_value for card in cards), reverse=True)

        # Check ace-high straight
        if len(ranks) == 5 and ranks[0] - ranks[4] == 4:
            return ranks[0]

        # Check wheel (A-2-3-4-5) - ace is low
        if ranks == [14, 5, 4, 3, 2]:
            return 5

        return 0

    @staticmethod
    def _get_four_of_a_kind(rank_counts: Counter) -> int:
        """Return rank value if 4-of-a-kind exists, else None."""
        for rank, count in rank_counts.items():
            if count == 4:
                return rank
        return None

    @staticmethod
    def _get_three_of_a_kind(rank_counts: Counter) -> int:
        """Return rank value if 3-of-a-kind exists, else None."""
        for rank, count in rank_counts.items():
            if count == 3:
                return rank
        return None

    @staticmethod
    def _get_pair(rank_counts: Counter, exclude: int = None) -> int:
        """Return rank value if pair exists, else None."""
        pairs = [rank for rank, count in rank_counts.items() if count >= 2]
        if exclude is not None:
            pairs = [r for r in pairs if r != exclude]
        if pairs:
            return max(pairs)
        return None

    @staticmethod
    def _get_remaining_kickers(rank_counts: Counter, num_in_combo: int) -> List[int]:
        """Get kickers sorted descending, excluding cards already counted."""
        kickers = []
        for rank in sorted(rank_counts.keys(), reverse=True):
            count = rank_counts[rank]
            for _ in range(max(0, count - num_in_combo)):
                kickers.append(rank)
        return kickers[:5]

    @staticmethod
    def _compare_hands(hand1: Tuple, hand2: Tuple) -> int:
        """
        Compare two hands.

        Args:
            hand1: (hand_rank, tiebreaker_tuple) from evaluate_5_card_hand.
            hand2: (hand_rank, tiebreaker_tuple) from evaluate_5_card_hand.

        Returns:
            > 0 if hand1 is better
            < 0 if hand2 is better
            0 if hands are identical
        """
        rank1, kickers1 = hand1[:2]
        rank2, kickers2 = hand2[:2]

        if rank1 != rank2:
            return rank1 - rank2

        # Compare kickers
        for k1, k2 in zip(kickers1, kickers2):
            if k1 != k2:
                return k1 - k2

        return 0

    @staticmethod
    def hand_name(hand_rank: int) -> str:
        """Return readable name of hand rank."""
        return HAND_NAMES.get(hand_rank, "Unknown")
