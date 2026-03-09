"""
Constants for PokerMind AI application.
"""

# Suits
SUITS = ("♠", "♥", "♦", "♣")
SUIT_SYMBOLS = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}

# Ranks
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
}


# Game settings
DEFAULT_STARTING_STACK = 1000
DEFAULT_SMALL_BLIND = 5
DEFAULT_BIG_BLIND = 10

# Actions
ACTION_FOLD = "fold"
ACTION_CHECK = "check"
ACTION_CALL = "call"
ACTION_BET = "bet"
ACTION_RAISE = "raise"
ACTION_ALL_IN = "all-in"

# Streets
STREET_PREFLOP = "preflop"
STREET_FLOP = "flop"
STREET_TURN = "turn"
STREET_RIVER = "river"
STREET_SHOWDOWN = "showdown"

STREETS = [STREET_PREFLOP, STREET_FLOP, STREET_TURN, STREET_RIVER, STREET_SHOWDOWN]

# Hand rankings (higher is better)
HAND_HIGH_CARD = 0
HAND_ONE_PAIR = 1
HAND_TWO_PAIR = 2
HAND_THREE_OF_A_KIND = 3
HAND_STRAIGHT = 4
HAND_FLUSH = 5
HAND_FULL_HOUSE = 6
HAND_FOUR_OF_A_KIND = 7
HAND_STRAIGHT_FLUSH = 8
HAND_ROYAL_FLUSH = 9

HAND_NAMES = {
    HAND_HIGH_CARD: "High Card",
    HAND_ONE_PAIR: "One Pair",
    HAND_TWO_PAIR: "Two Pair",
    HAND_THREE_OF_A_KIND: "Three of a Kind",
    HAND_STRAIGHT: "Straight",
    HAND_FLUSH: "Flush",
    HAND_FULL_HOUSE: "Full House",
    HAND_FOUR_OF_A_KIND: "Four of a Kind",
    HAND_STRAIGHT_FLUSH: "Straight Flush",
    HAND_ROYAL_FLUSH: "Royal Flush",
}

# AI styles
AI_STYLE_TIGHT = "Tight Conservative"
AI_STYLE_BALANCED = "Balanced"
AI_STYLE_AGGRESSIVE = "Aggressive Bluffing"

AI_STYLES = [AI_STYLE_TIGHT, AI_STYLE_BALANCED, AI_STYLE_AGGRESSIVE]

# AI thresholds (adjustable by style)
AI_THRESHOLDS = {
    AI_STYLE_TIGHT: {
        "preflop_raise_threshold": 0.65,
        "postflop_call_threshold": 0.40,
        "postflop_raise_threshold": 0.60,
        "bluff_frequency": 0.05,
        "cbet_frequency": 0.50,
    },
    AI_STYLE_BALANCED: {
        "preflop_raise_threshold": 0.55,
        "postflop_call_threshold": 0.35,
        "postflop_raise_threshold": 0.50,
        "bluff_frequency": 0.15,
        "cbet_frequency": 0.70,
    },
    AI_STYLE_AGGRESSIVE: {
        "preflop_raise_threshold": 0.45,
        "postflop_call_threshold": 0.25,
        "postflop_raise_threshold": 0.40,
        "bluff_frequency": 0.30,
        "cbet_frequency": 0.85,
    },
}

# Monte Carlo simulation
DEFAULT_MONTE_CARLO_SIMULATIONS = 1000
MIN_MONTE_CARLO_SIMULATIONS = 100
MAX_MONTE_CARLO_SIMULATIONS = 10000
