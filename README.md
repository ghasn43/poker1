# PokerMind AI - Texas Hold'em Poker Application

![PokerMind AI](https://img.shields.io/badge/Poker-AI-blue) ![Python](https://img.shields.io/badge/Python-3.11%2B-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## Overview

**PokerMind AI** is an educational Texas Hold'em poker application featuring a playable heads-up poker game against an intelligent AI opponent. Built with Python and Streamlit, it combines accurate poker game mechanics with an AI engine that uses Monte Carlo simulation to estimate hand equity and make strategic decisions.

### Purpose

This application is designed for:
- **Education**: Learn Texas Hold'em poker rules and strategy through interactive play
- **Simulation**: Practice poker strategy and decision-making
- **Entertainment**: Play casual poker games against an AI opponent

**Disclaimer**: This is an educational tool only. It is not designed to bypass any online poker platform rules or to automate play on real-money poker websites.

## Features

### Core Gameplay
- ✅ **Heads-Up Texas Hold'em**: Play 1v1 against an AI opponent
- ✅ **Complete Rule Support**: Preflop, Flop, Turn, River, Showdown
- ✅ **Accurate Hand Evaluation**: Correctly ranks all poker hand types (high card through royal flush)
- ✅ **Betting Actions**: Fold, Check, Call, Bet, Raise, All-in
- ✅ **Blind Management**: Small blind/Big blind rotation in heads-up
- ✅ **Side Pot Logic**: Handles all-in scenarios with side pots

### AI Opponent
- 🤖 **Three AI Personalities**:
  - **Tight Conservative**: Folds weak hands, raises with quality hands only
  - **Balanced**: Balanced play based on equity and pot odds
  - **Aggressive Bluffing**: Wide playing range, frequent bluffs and continuation bets
  
- 🎯 **Smart Decision Engine**:
  - Preflop hand strength evaluation using ranked hand groups
  - Postflop Monte Carlo equity calculation (500-5000 simulations)
  - Pot odds analysis
  - Board texture assessment
  - Controlled bluffing based on style
  - Action history awareness

### Educational Mode
- 📊 **Hand Analysis**: View your estimated win probability and equity
- 🎓 **AI Reasoning**: See explanations for each AI decision
- 📈 **Board Texture**: Understand community card dynamics
- ✨ **Best Hand Display**: See which 5-card hand your cards make

### User Interface
- 🎨 **Clean Design**: Organized Streamlit interface
- 🎮 **Interactive Controls**: Intuitive action buttons
- 📋 **Game History**: Action timeline for each hand
- ⚙️ **Customizable Settings**:
  - Starting stack size (100-5000 chips)
  - Blind sizes
  - AI opponent style
  - Monte Carlo simulation count
  - Educational mode toggle

## Installation

### Requirements
- **Python 3.11+**
- **pip** (Python package manager)

### Setup

1. **Clone or download the project**:
   ```bash
   cd pokermind_ai
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Start the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## How to Play

### Game Flow

1. **Setup Phase**:
   - Choose your AI opponent style (Tight, Balanced, Aggressive)
   - Adjust blind sizes and starting stack if desired
   - Click "Next Hand" to begin

2. **Each Hand**:
   - Blinds are automatically posted
   - You receive 2 hole cards
   - AI receives 2 hole cards (hidden until showdown)
   - Community cards are dealt (flop, turn, river)

3. **Betting Rounds**:
   - When it's your turn to act, click an action button:
     - **Fold**: Forfeit the hand
     - **Check**: Pass action without betting
     - **Call**: Match the current bet
     - **Bet/Raise**: Increase the bet (use slider to choose amount)
     - **All-in**: Go all-in with remaining chips
   - AI acts automatically in turn
   - Rounds continue until:
     - One player folds, OR
     - Everyone checks/calls to showdown

4. **Showdown**:
   - Best 5-card hand wins the pot
   - AI cards are revealed
   - Winner is declared
   - Stacks are updated

5. **Next Hand**:
   - Button rotates
   - Click "Next Hand" to continue match
   - Match ends when one player runs out of chips

### Educational Insights

When in Educational Mode:
- See your **win probability** against AI's unknown hand
- View AI's **action reasoning** (why it folded, called, raised, etc.)
- Understand **board texture** (pairs, straight possibilities, flush draws)
- Analyze your **best 5-card hand** from your cards + community

## Project Structure

```
pokermind_ai/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
│
├── core/                     # Core game engine
│   ├── cards.py             # Card and Deck classes
│   ├── evaluator.py         # Hand evaluation and ranking
│   ├── player.py            # Player representation
│   ├── betting.py           # Betting rules and validation
│   ├── game.py              # Main game orchestration
│   └── ai_logic.py          # AI decision-making engine
│
├── utils/                   # Utility modules
│   ├── constants.py         # Game constants and thresholds
│   ├── monte_carlo.py       # Equity calculation via simulation
│   └── formatters.py        # Display formatting helpers
│
└── tests/                   # Unit tests
    ├── test_evaluator.py    # Hand evaluation tests
    ├── test_game.py         # Game logic tests
    └── test_ai_logic.py     # AI decision tests
```

## Poker Rules Supported

### Hand Rankings (Best to Worst)
1. **Royal Flush**: A-K-Q-J-10 of same suit
2. **Straight Flush**: Five cards in sequence, same suit
3. **Four of a Kind**: Four cards of same rank
4. **Full House**: Three of a kind + Pair
5. **Flush**: Five cards of same suit
6. **Straight**: Five cards in sequence
7. **Three of a Kind**: Three cards of same rank
8. **Two Pair**: Two different pairs
9. **One Pair**: Two cards of same rank
10. **High Card**: No combination (highest card wins)

### Game Rules
- **Heads-Up**: Exactly 2 players (button posts small blind)
- **Blinding**: Small blind / Big blind to start betting
- **Preflop Action**: Button acts first (as small blind)
- **Postflop Action**: Non-button player acts first
- **All-In**: Player can go all-in with remaining chips
- **Side pots**: Handled correctly for unequal betting
- **Betting Limits**: No-limit (can bet any amount)

### Special Rules
- **Wheel straight** (A-2-3-4-5): Ace counts as 1, not 14
- **Chop/Run-it-Twice**: Not implemented
- **Rake**: No rake (not a real money situation)

## AI Strategy Overview

### Preflop Strategy

The AI evaluates starting hands using a strength-based approach:

- **Premium Hands** (Tight:100%, Balanced:80%, Aggressive:60%): AA, KK, QQ, AK
- **Strong Hands** (Tight:60%, Balanced:50%, Aggressive:40%): JJ, TT, AQ, AJ, KQ
- **Medium Hands** (Tight:30%, Balanced:40%, Aggressive:60%): Pairs, suited connectors, broadway
- **Weak Hands** (Folds unless bluffing)

### Postflop Strategy

On the flop, turn, and river, the AI:

1. **Calculates Equity**: Monte Carlo simulation (500+ hands)
2. **Assesses Board**: Looks for made hands, draws, and danger cards
3. **Estimates Pot Odds**: Compares required investment to pot size
4. **Decides Action**:
   - If equity > threshold: Bet or raise
   - If equity borderline: Call if pot odds favorable
   - If equity low: Fold unless bluffing opportunity

### Bluffing

The AI incorporates controlled randomness:
- **Tight**: 5% bluff frequency
- **Balanced**: 15% bluff frequency
- **Aggressive**: 30% bluff frequency

Bluffs are more likely on scary/wet boards where it's plausible the AI has a strong hand.

## Technical Details

### Hand Evaluation Algorithm

The evaluator uses:
- **Rank-based grouping**: Groups cards by rank for duplicate detection
- **Combination checking**: Evaluates in order: 4-kind, full house, 3-kind, 2-pair, pair, high card
- **Straight detection**: Handles both ace-high and wheel (ace-low) straights
- **Kicker tracking**: Maintains proper kickers for tie-breaking
- **Best 5-of-7 selection**: Enumerates all C(7,5) = 21 combinations

### Monte Carlo Simulation

For postflop equity:
1. Remove known cards (your hand + board) from deck
2. For N simulations:
   - Deal random opponent hole cards
   - Complete board with random remaining cards
   - Evaluate both hands
   - Track win/tie/loss
3. Return win%, tie%, loss% frequencies

### Pot Odds Example

If pot is $100 and you need to call $20:
- Pot odds are 100:20 = 5:1
- You need ~17% equity to call (1/(1+5))
- Favorable to call if your equity > 17%

## Dependencies

- **streamlit** (≥1.28.0): Web interface
- **numpy** (≥1.21.0): Numerical operations
- **pandas** (≥1.3.0): Data handling (future enhancement)

Note: Pure Python is used where possible. NumPy is optional but recommended for performance.

## Testing

Run the test suite:

```bash
python -m pytest tests/
# or
python -m unittest discover -s tests
```

### Test Coverage

- **test_evaluator.py**: Hand ranking, straight detection, best hand selection
- **test_game.py**: Game initialization, blind posting, action processing
- **test_ai_logic.py**: AI initialization, hand strength, decision validity

## Future Enhancements

Possible improvements for future versions:

1. **Tournament Mode**: Multi-handed or tournament structure
2. **Hand History Export**: Save/replay hands
3. **Bankroll Graph**: Visualize chip stack over time
4. **Difficulty Selector**: Separate skill level from style
5. **Ranges UI**: Show AI's preflop/postflop ranges
6. **Replay Last Hand**: Re-run a previous hand
7. **More AI Personalities**: Exploitative styles, GTO approximation
8. **Position Analysis**: More sophisticated positional awareness
9. **Pot Limit Omaha**: Extend to other games
10. **Multiplayer Network**: Play against other humans online

## Known Limitations

- AI does not adapt its strategy based on player exploits (static strategy)
- No simplified GTO (Game Theory Optimal) solving
- Hand history export not yet implemented
- No hand replayer feature
- AI does not use bet sizing tells to infer opponent strength
- Cannot save/load game state between sessions

## Disclaimer

**This application is for educational and entertainment purposes only.**

- Not designed to bypass any online poker platform rules
- Not designed to automate play on real-money poker websites
- Not affiliated with any casino or poker room
- Should not be used for gambling
- Created for learning poker strategy and game mechanics

Responsible Gaming: Poker involves risk. Play only with money you can afford to lose.

## Contributing

Suggestions and improvements are welcome! Areas for contribution:

- Improved AI strategy
- Additional personality types
- Better UI/UX
- Performance optimizations
- Bug fixes
- Documentation improvements

## License

MIT License - Feel free to use, modify, and distribute.

## Author

PokerMind AI Development Team

## References

### Poker Resources
- [Wikipedia: Texas Hold'em](https://en.wikipedia.org/wiki/Texas_hold_%27em)
- [Hand Rankings](https://www.pokerhandranker.com/)
- [Pot Odds](https://en.wikipedia.org/wiki/Pot_odds)

### Technical Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Official](https://www.python.org/)

---

**Enjoy playing PokerMind AI! 🎰🤖**
