"""
Monte Carlo simulation for poker equity calculation.
"""

import random
from typing import List, Tuple
from core.cards import Card, Deck
from core.evaluator import HandEvaluator
from utils.constants import DEFAULT_MONTE_CARLO_SIMULATIONS


def estimate_win_probability(
    ai_hole_cards: List[Card],
    community_cards: List[Card],
    num_simulations: int = DEFAULT_MONTE_CARLO_SIMULATIONS,
) -> Tuple[float, float, float]:
    """
    Estimate win, tie, and loss probabilities using Monte Carlo simulation.

    Simulates all possible opponent hands and remaining board cards.

    Args:
        ai_hole_cards: AI's 2 hole cards.
        community_cards: Current community cards (0-5).
        num_simulations: Number of simulations to run.

    Returns:
        Tuple of (win_rate, tie_rate, loss_rate) as floats [0, 1].
    """
    wins = 0
    ties = 0
    losses = 0

    for _ in range(num_simulations):
        # Create a deck and remove known cards
        deck = Deck()
        known_cards = set(ai_hole_cards + community_cards)
        deck.cards = [card for card in deck.cards if card not in known_cards]

        # Deal random opponent hole cards
        opponent_hole = [deck.deal_one(), deck.deal_one()]

        # Complete the board with remaining cards
        cards_needed = 5 - len(community_cards)
        remaining_board = [deck.deal_one() for _ in range(cards_needed)]
        full_board = community_cards + remaining_board

        # Evaluate hands
        ai_best = HandEvaluator.best_hand_from_7(ai_hole_cards, full_board)
        opp_best = HandEvaluator.best_hand_from_7(opponent_hole, full_board)

        # Compare (higher is better)
        comparison = HandEvaluator._compare_hands(ai_best[:2], opp_best[:2])
        if comparison > 0:
            wins += 1
        elif comparison == 0:
            ties += 1
        else:
            losses += 1

    total = wins + ties + losses
    return (
        wins / total if total > 0 else 0,
        ties / total if total > 0 else 0,
        losses / total if total > 0 else 0,
    )


def estimate_hand_strength(
    ai_hole_cards: List[Card],
    community_cards: List[Card],
    num_simulations: int = 500,
) -> float:
    """
    Quick estimate of hand strength (win + 0.5*tie).

    Args:
        ai_hole_cards: AI's hole cards.
        community_cards: Board cards.
        num_simulations: Number of sims.

    Returns:
        Hand strength [0, 1].
    """
    win_rate, tie_rate, _ = estimate_win_probability(
        ai_hole_cards, community_cards, num_simulations
    )
    return win_rate + 0.5 * tie_rate
