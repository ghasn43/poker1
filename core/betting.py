"""
Betting utilities and rules for poker.
"""

from typing import List, Tuple, Optional
from core.player import Player
from utils.constants import (
    ACTION_FOLD,
    ACTION_CHECK,
    ACTION_CALL,
    ACTION_BET,
    ACTION_RAISE,
    ACTION_ALL_IN,
)


class BettingRound:
    """Manages betting logic and validation."""

    @staticmethod
    def legal_actions(player: Player, current_bet_level: int, has_bet: bool) -> List[str]:
        """
        Determine legal actions for a player.

        Args:
            player: The player.
            current_bet_level: Current bet size this round.
            has_bet: Whether player has already acted this round.

        Returns:
            List of legal actions.
        """
        if player.folded or player.all_in:
            return []

        actions = []

        # Can always fold
        actions.append(ACTION_FOLD)

        # Can check if no bet facing them
        if current_bet_level == 0 or player.current_bet >= current_bet_level:
            actions.append(ACTION_CHECK)

        # Can call if facing a bet and have chips
        if current_bet_level > player.current_bet and player.stack > 0:
            actions.append(ACTION_CALL)

        # Can bet if no bet out and have chips
        if current_bet_level == 0 and player.stack > 0:
            actions.append(ACTION_BET)

        # Can raise if facing bet and have chips
        if (
            current_bet_level > 0
            and player.current_bet < current_bet_level
            and player.stack > 0
        ):
            actions.append(ACTION_RAISE)

        # All-in shortcut
        if player.stack > 0 and current_bet_level > player.current_bet:
            if ACTION_ALL_IN not in actions:
                if ACTION_RAISE in actions or ACTION_CALL in actions:
                    actions.append(ACTION_ALL_IN)

        return actions

    @staticmethod
    def call_amount(player: Player, current_bet_level: int) -> int:
        """
        Calculate amount needed to call.

        Args:
            player: The player.
            current_bet_level: Current bet size this round.

        Returns:
            Amount needed to call (at most player's remaining stack).
        """
        call = max(0, current_bet_level - player.current_bet)
        return min(call, player.stack)

    @staticmethod
    def min_raise_amount(player: Player, current_bet_level: int, last_bet_size: int) -> int:
        """
        Calculate minimum raise amount.

        Args:
            player: The player.
            current_bet_level: Current bet size this round.
            last_bet_size: Size of last bet/raise.

        Returns:
            Minimum raise amount.
        """
        if last_bet_size == 0:
            # First bet of round
            return current_bet_level if current_bet_level > 0 else 1

        # Raise must be at least the size of last bet
        return current_bet_level + last_bet_size

    @staticmethod
    def max_raise_amount(player: Player) -> int:
        """Maximum amount player can raise (all their chips)."""
        return player.stack

    @staticmethod
    def resolve_action(
        player: Player,
        action: str,
        amount: int = 0,
        current_bet_level: int = 0,
    ) -> Tuple[str, int]:
        """
        Process a betting action.

        Args:
            player: The player acting.
            action: The action (fold, check, call, bet, raise, all-in).
            amount: Amount for bet/raise actions.
            current_bet_level: Current bet size in round.

        Returns:
            Tuple of (actual_action, actual_amount).
        """
        actual_action = action
        actual_amount = 0

        if action == ACTION_FOLD:
            player.fold()

        elif action == ACTION_CHECK:
            # No chips added
            pass

        elif action == ACTION_CALL:
            call_amt = BettingRound.call_amount(player, current_bet_level)
            actual_amount = player.place_bet(call_amt)

        elif action == ACTION_BET:
            bet_amt = min(amount, player.stack)
            actual_amount = player.place_bet(bet_amt)

        elif action == ACTION_RAISE:
            raise_amt = min(amount, player.stack + player.current_bet)
            call_amt = BettingRound.call_amount(player, current_bet_level)
            raise_total = call_amt + (raise_amt - current_bet_level)
            raise_total = min(raise_total, player.stack + player.current_bet)
            to_add = raise_total - player.current_bet
            if to_add > 0:
                actual_amount = player.place_bet(to_add)
            else:
                actual_amount = 0

        elif action == ACTION_ALL_IN:
            actual_amount = player.place_bet(player.stack)
            if actual_amount > 0:
                actual_action = ACTION_ALL_IN

        return (actual_action, actual_amount)
