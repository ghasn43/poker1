"""
Formatting and display utilities.
"""

from typing import List, Tuple
from core.cards import Card
from core.evaluator import HandEvaluator
from utils.constants import HAND_NAMES


def format_cards(cards: List[Card], hidden: bool = False) -> str:
    """
    Format cards for display.

    Args:
        cards: List of cards.
        hidden: If True, show as face-down.

    Returns:
        Formatted string.
    """
    if hidden:
        return " ".join(["🂠"] * len(cards))
    if not cards:
        return "(none)"
    return " ".join(str(card) for card in cards)


def format_card_fancy(card: Card) -> str:
    """Return fancy card display with color and styling."""
    return str(card)


def format_cards_fancy(cards: List[Card], hidden: bool = False) -> str:
    """Format cards with fancy styling for visual display."""
    if hidden:
        return " 🂠 " * len(cards)
    
    if not cards:
        return ""
    
    # Return cards with better spacing
    return "  ".join(str(card) for card in cards)


def get_card_color(card: Card) -> str:
    """Get hex color for card suit."""
    suit_colors = {
        "H": "#ff0000",  # Hearts - Red
        "D": "#ff0000",  # Diamonds - Red
        "S": "#000000",  # Spades - Black
        "C": "#000000",  # Clubs - Black
    }
    return suit_colors.get(card.suit, "#000000")


def render_card_html(card: Card) -> str:
    """Render a single card as HTML."""
    color = get_card_color(card)
    color_class = "card-red" if color == "#ff0000" else "card-black"
    return f"<div class='poker-card {color_class}'><span class='poker-card-rank'>{card.rank}</span><span class='poker-card-suit'>{card.suit_symbol}</span></div>"


def render_cards_html(cards: List[Card], hidden: bool = False, size: str = "medium") -> str:
    """Render cards as HTML with nice styling."""
    if hidden:
        card_back = "<div style='display:inline-block;width:60px;height:80px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border:3px solid #9999cc;border-radius:4px;margin:5px;box-shadow:0 4px 8px rgba(0,0,0,0.4);'></div>"
        return f"<div style='text-align:center;'>{card_back * len(cards)}</div>"
    
    if not cards:
        return "<p style='color:#999;text-align:center;'>No cards</p>"
    
    card_html = "".join(render_card_html(card) for card in cards)
    return f"<div style='text-align:center;'>{card_html}</div>"


def format_hand_name(hand_rank: int) -> str:
    """Get display name for hand rank."""
    return HAND_NAMES.get(hand_rank, "Unknown")


def format_action(action: str, amount: int = 0) -> str:
    """
    Format action for display.

    Args:
        action: Action type.
        amount: Amount (if applicable).

    Returns:
        Formatted string.
    """
    if action == "fold":
        return "Fold"
    elif action == "check":
        return "Check"
    elif action == "call":
        return f"Call {amount}"
    elif action == "bet":
        return f"Bet {amount}"
    elif action == "raise":
        return f"Raise to {amount}"
    elif action == "all-in":
        return f"All-in {amount}"
    else:
        return action.capitalize()


def format_pot(amount: int) -> str:
    """Format pot amount."""
    return f"${amount:,.0f}" if amount >= 1000 else f"${amount}"


def format_stack(amount: int) -> str:
    """Format stack amount."""
    return f"${amount:,.0f}" if amount >= 1000 else f"${amount}"


def format_board_texture(community_cards: List[Card]) -> str:
    """
    Analyze and describe board texture.

    Args:
        community_cards: Community cards on board.

    Returns:
        Description of board texture.
    """
    if not community_cards:
        return "Preflop (no board)"

    if len(community_cards) == 3:
        street = "Flop"
    elif len(community_cards) == 4:
        street = "Turn"
    elif len(community_cards) == 5:
        street = "River"
    else:
        street = f"{len(community_cards)} cards"

    # Check for draws and pairs
    ranks = [card.rank for card in community_cards]
    suits = [card.suit for card in community_cards]

    texture_notes = []

    # Pair on board
    if len(ranks) != len(set(ranks)):
        texture_notes.append("paired")

    # Flush possibility
    for suit in ("S", "H", "D", "C"):
        if suits.count(suit) >= 2:
            texture_notes.append(f"flush draw possible ({suit})")
            break

    # Straight possibility (simplified)
    if len(community_cards) >= 3:
        rank_values = sorted(set(card.rank_value for card in community_cards))
        if len(rank_values) >= 3:
            # Check if cards could form straights
            gaps = [rank_values[i + 1] - rank_values[i] for i in range(len(rank_values) - 1)]
            max_gap = max(gaps) if gaps else 0
            if max_gap <= 2:
                texture_notes.append("straight possibility")

    if texture_notes:
        return f"{street}: {', '.join(texture_notes)}"
    else:
        return f"{street}: dry/low activity"


def format_odds(win_pct: float, tie_pct: float = 0.0, loss_pct: float = 0.0) -> str:
    """Format win probabilities."""
    return f"{win_pct*100:.1f}%"


def format_explanation(text: str) -> str:
    """Format explanation text."""
    return text

