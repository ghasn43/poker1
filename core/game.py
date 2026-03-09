"""
Main poker game engine.
"""

from typing import List, Tuple, Optional, Dict
from core.cards import Card, Deck
from core.player import Player
from core.evaluator import HandEvaluator
from core.betting import BettingRound
from core.ai_logic import PokerAI
from utils.constants import (
    STREET_PREFLOP,
    STREET_FLOP,
    STREET_TURN,
    STREET_RIVER,
    STREET_SHOWDOWN,
    STREETS,
    ACTION_FOLD,
    ACTION_CHECK,
    ACTION_CALL,
    ACTION_BET,
    ACTION_RAISE,
    ACTION_ALL_IN,
)


class PokerGame:
    """Manages a full heads-up Texas Hold'em poker match."""

    def __init__(
        self,
        human_player: Player,
        ai_player: Player,
        small_blind: int = 5,
        big_blind: int = 10,
    ):
        """
        Initialize a poker game.

        Args:
            human_player: The human player.
            ai_player: The AI opponent.
            small_blind: Small blind size.
            big_blind: Big blind size.
        """
        self.human = human_player
        self.ai = ai_player
        self.small_blind = small_blind
        self.big_blind = big_blind

        # Game state
        self.deck: Optional[Deck] = None
        self.community_cards: List[Card] = []
        self.pot = 0
        self.street = STREET_PREFLOP
        self.button_position = 0  # 0 = human, 1 = ai
        self.active_player: Optional[Player] = None
        self.action_history: List[Tuple] = []
        self.hand_history: List[Dict] = []
        self.hand_number = 0
        self.last_bet_size = 0
        self.current_round_bet_level = 0

    def start_new_hand(self) -> None:
        """Initialize a new hand."""
        # Reset players
        self.human.reset_hand()
        self.ai.reset_hand()

        # Reset game state
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.street = STREET_PREFLOP
        self.action_history = []
        self.hand_number += 1
        self.last_bet_size = 0
        self.current_round_bet_level = 0

        # Post blinds
        self._post_blinds()

        # Deal hole cards
        self.human.receive_cards(self.deck.deal_many(2))
        self.ai.receive_cards(self.deck.deal_many(2))

        # Determine first to act (in heads-up, button acts first preflop)
        self._set_first_to_act()

    def _post_blinds(self) -> None:
        """Post small and big blinds."""
        if self.button_position == 0:
            # Human is button (posts small blind)
            sb_player = self.human
            bb_player = self.ai
        else:
            # AI is button (posts small blind)
            sb_player = self.ai
            bb_player = self.human

        # Small blind
        sb_amt = min(self.small_blind, sb_player.stack)
        sb_player.place_bet(sb_amt)
        self.pot += sb_amt

        # Big blind
        bb_amt = min(self.big_blind, bb_player.stack)
        bb_player.place_bet(bb_amt)
        self.pot += bb_amt

        self.current_round_bet_level = bb_amt
        self.last_bet_size = bb_amt

    def _set_first_to_act(self) -> None:
        """Determine who acts first this street."""
        if self.street == STREET_PREFLOP:
            # In heads-up, button (small blind) acts first preflop
            if self.button_position == 0:
                self.active_player = self.human
            else:
                self.active_player = self.ai
        else:
            # Postflop, big blind acts first
            if self.button_position == 0:
                self.active_player = self.ai
            else:
                self.active_player = self.human

    def get_other_player(self, player: Player) -> Player:
        """Get the other player."""
        return self.ai if player == self.human else self.human

    def advance_street(self) -> None:
        """Advance to next street and deal community cards."""
        street_idx = STREETS.index(self.street)

        if street_idx < len(STREETS) - 1:
            self.street = STREETS[street_idx + 1]

            # Deal cards for this street
            if self.street == STREET_FLOP:
                self.community_cards = self.deck.deal_many(3)
            elif self.street == STREET_TURN:
                self.community_cards.append(self.deck.deal_one())
            elif self.street == STREET_RIVER:
                self.community_cards.append(self.deck.deal_one())

            # Reset bets for new street
            self.human.current_bet = 0
            self.ai.current_bet = 0
            self.current_round_bet_level = 0
            self.last_bet_size = 0

            # Big blind acts first postflop
            self._set_first_to_act()

    def process_player_action(
        self, action: str, amount: int = 0
    ) -> Tuple[str, str]:
        """
        Process a player's action.

        Args:
            action: Action type (fold, check, call, bet, raise, all-in).
            amount: Amount for bet/raise.

        Returns:
            Tuple of (action_taken, reason).
        """
        if not self.active_player:
            return (action, "No active player")

        player = self.active_player
        other = self.get_other_player(player)

        # Validate action
        legal = BettingRound.legal_actions(player, self.current_round_bet_level, True)
        if action not in legal:
            return (action, f"Illegal action. Legal actions: {legal}")

        # Process action
        actual_action, actual_amount = BettingRound.resolve_action(
            player, action, amount, self.current_round_bet_level
        )

        # Update pot and bet tracking
        self.pot += actual_amount
        self.last_bet_size = actual_amount

        if actual_action in (ACTION_BET, ACTION_RAISE, ACTION_ALL_IN):
            self.current_round_bet_level = player.current_bet

        # Log action
        self.action_history.append((player.name, actual_action, actual_amount))

        # Check if hand is over
        if player.folded:
            return (actual_action, f"{player.name} folded")

        # Move to next player or next street
        if other.folded:
            # Hand over, current player wins pot
            return (actual_action, f"Hand over - {player.name} wins")

        # Check if both players have bet same amount (or checked)
        if player.current_bet == other.current_bet and (
            player.all_in or other.all_in or not other.folded
        ):
            # Move to next street or showdown
            if self.street == STREET_RIVER or player.all_in or other.all_in:
                self.street = STREET_SHOWDOWN
            else:
                self.advance_street()
            self.active_player = other
        else:
            # Other player acts
            self.active_player = other

        return (actual_action, f"{player.name} {actual_action}d")

    def get_handhistory(self) -> Dict:
        """Get history of current hand."""
        return {
            "hand_number": self.hand_number,
            "human_hole": str(self.human.hole_cards),
            "ai_hole": str(self.ai.hole_cards),
            "board": str(self.community_cards),
            "actions": self.action_history,
            "final_pot": self.pot,
        }

    def determine_winner(self) -> Tuple[Player, str]:
        """
        Determine winner at showdown.

        Returns:
            Tuple of (winner_player, result_description).
        """
        # If only one player hasn't folded
        if self.human.folded and not self.ai.folded:
            return (self.ai, "Human folded")

        if self.ai.folded and not self.human.folded:
            return (self.human, "AI folded")

        # Both still in - showdown
        if len(self.community_cards) < 5:
            # Should not happen in normal flow
            return (self.human, "Early end")

        human_best = HandEvaluator.best_hand_from_7(
            self.human.hole_cards, self.community_cards
        )
        ai_best = HandEvaluator.best_hand_from_7(
            self.ai.hole_cards, self.community_cards
        )

        comparison = HandEvaluator._compare_hands(human_best[:2], ai_best[:2])

        if comparison > 0:
            hand_name = HandEvaluator.hand_name(human_best[0])
            return (self.human, f"Human wins with {hand_name}")
        elif comparison < 0:
            hand_name = HandEvaluator.hand_name(ai_best[0])
            return (self.ai, f"AI wins with {hand_name}")
        else:
            return (None, "Tie")

    def resolve_hand(self) -> Tuple[Player, str]:
        """
        Resolve the current hand and award pot.

        Returns:
            Tuple of (winner, description).
        """
        if self.human.folded and self.ai.folded:
            # Both folded (shouldn't happen)
            return (None, "Both folded")

        winner, description = self.determine_winner()

        if winner:
            winner.win_pot(self.pot)

        return (winner, description)

    def is_hand_over(self) -> bool:
        """Check if current hand is complete."""
        # Hand is over if:
        # - Someone folded, OR
        # - We're at showdown, OR
        # - Both players are all-in
        if self.human.folded or self.ai.folded:
            return True

        if self.street == STREET_SHOWDOWN:
            return True

        if self.human.all_in and self.ai.all_in:
            return True

        return False

    def is_match_over(self) -> bool:
        """Check if the entire match is over (one player busted)."""
        return self.human.stack <= 0 or self.ai.stack <= 0

    def get_game_state(self) -> Dict:
        """Get current game state for display."""
        return {
            "hand_number": self.hand_number,
            "human": {
                "name": self.human.name,
                "stack": self.human.stack,
                "hole_cards": self.human.hole_cards,
                "current_bet": self.human.current_bet,
                "folded": self.human.folded,
                "all_in": self.human.all_in,
            },
            "ai": {
                "name": self.ai.name,
                "stack": self.ai.stack,
                "hole_cards": self.ai.hole_cards,
                "current_bet": self.ai.current_bet,
                "folded": self.ai.folded,
                "all_in": self.ai.all_in,
            },
            "community_cards": self.community_cards,
            "pot": self.pot,
            "street": self.street,
            "button_position": self.button_position,
            "active_player": self.active_player.name if self.active_player else None,
            "action_history": self.action_history,
        }
