"""
PokerMind AI - Texas Hold'em Poker App with AI Opponent
Main Streamlit UI application.
"""

import streamlit as st
from typing import Optional
from core.player import Player
from core.game import PokerGame
from core.ai_logic import PokerAI
from core.evaluator import HandEvaluator
from utils.formatters import (
    format_cards,
    format_hand_name,
    format_action,
    format_pot,
    format_stack,
    format_board_texture,
    format_odds,
    render_cards_html,
)
from utils.monte_carlo import estimate_win_probability, estimate_hand_strength
from utils.constants import (
    DEFAULT_STARTING_STACK,
    DEFAULT_SMALL_BLIND,
    DEFAULT_BIG_BLIND,
    AI_STYLE_TIGHT,
    AI_STYLE_BALANCED,
    AI_STYLE_AGGRESSIVE,
    AI_STYLES,
    STREET_PREFLOP,
    STREET_SHOWDOWN,
    ACTION_FOLD,
    ACTION_CHECK,
    ACTION_CALL,
    ACTION_BET,
    ACTION_RAISE,
    ACTION_ALL_IN,
)


# Custom CSS for better UI
def add_custom_css():
    """Add custom CSS for game styling."""
    st.markdown("""
    <style>
    /* Text and font improvements */
    body, .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #f0f0f0;
    }
    
    p, span, label {
        color: #e8e8e8 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Cards display */
    .card-display {
        font-size: 24px;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 2px solid rgba(255,255,255,0.2);
        color: #ffffff !important;
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    /* Player sections */
    .player-section {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00d4ff;
    }
    
    .player-section div {
        color: #f0f0f0 !important;
    }
    
    .ai-section {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff006e;
    }
    
    .ai-section div {
        color: #f0f0f0 !important;
    }
    
    /* Action buttons */
    .action-button {
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        color: #ffffff !important;
    }
    
    /* Pot display */
    .pot-display {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #00ff88 !important;
        padding: 15px;
        background: rgba(0,255,136,0.1);
        border-radius: 8px;
        border: 2px solid rgba(0,255,136,0.3);
    }
    
    /* Info panels */
    .info-panel {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
        color: #e8e8e8 !important;
    }
    
    .info-panel > div, .info-panel > p {
        color: #e8e8e8 !important;
    }
    
    /* Street indicator */
    .street-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* Metrics */
    .metric-label {
        font-size: 12px;
        color: #c0c0c0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(255,255,255,0.1);
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] {
        background-color: rgba(22, 33, 62, 0.95);
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #e8e8e8 !important;
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Sidebar selectbox and inputs */
    [data-testid="stSidebar"] select {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] button {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [role="button"] {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="input"] {
        color: #ffffff !important;
    }
    
    /* AGGRESSIVE selectbox override - target all possible elements */
    .stSelectbox {
        opacity: 1 !important;
        filter: brightness(1) contrast(1.5) !important;
    }
    
    .stSelectbox * {
        opacity: 1 !important;
        color: #000000 !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    /* Override Streamlit's default styling */
    div[data-testid="stSelectbox"] {
        opacity: 1 !important;
        filter: brightness(1) contrast(1.5) !important;
    }
    
    /* Target the button/field that shows selected value */
    div[data-testid="stSelectbox"] button {
        opacity: 1 !important;
        color: #000000 !important;
        background-color: #ffffff !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    div[data-testid="stSelectbox"] button:not(:hover) {
        opacity: 1 !important;
        color: #000000 !important;
        background-color: #ffffff !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    /* All text inside selectbox */
    div[data-testid="stSelectbox"] button span,
    div[data-testid="stSelectbox"] button div,
    div[data-testid="stSelectbox"] button p {
        opacity: 1 !important;
        color: #000000 !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    /* Target every single child */
    div[data-testid="stSelectbox"] button * {
        opacity: 1 !important;
        color: #000000 !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    div[data-testid="stSelectbox"] button *::before,
    div[data-testid="stSelectbox"] button *::after {
        opacity: 1 !important;
        color: #000000 !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    /* Sidebar version */
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] {
        opacity: 1 !important;
        filter: brightness(1) contrast(1.5) !important;
    }
    
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] button {
        opacity: 1 !important;
        color: #000000 !important;
        background-color: #ffffff !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] button * {
        opacity: 1 !important;
        color: #000000 !important;
        filter: brightness(1.2) contrast(1.5) !important;
    }
    
    /* Dropdown menu styling */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    div[role="listbox"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    div[role="option"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    div[role="option"]:hover {
        background-color: #e0e0e0 !important;
        color: #000000 !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }
    
    /* Input labels and text */
    label {
        color: #e8e8e8 !important;
        font-weight: 500;
    }
    
    .stMetric label {
        color: #b0b0b0 !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background-color: rgba(255,255,255,0.02);
    }
    
    /* Card styling */
    .card-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        padding: 20px 0;
    }
    
    .card {
        width: 70px;
        height: 100px;
        background: white;
        border: 3px solid #333;
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.5);
    }
    
    .card-rank {
        font-size: 20px;
        line-height: 1;
    }
    
    .card-suit {
        font-size: 16px;
        margin-top: 5px;
    }
    
    .card-back {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 3px solid #9999cc;
    }
    
    /* Button styling - Primary buttons */
    button {
        color: #ffffff !important;
        font-weight: bold;
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,212,255,0.3) !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #00f5ff 0%, #00ccee 100%) !important;
        box-shadow: 0 6px 16px rgba(0,212,255,0.5) !important;
    }
    
    button[kind="secondary"] {
        background: linear-gradient(135deg, #ff006e 0%, #cc0055 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255,0,110,0.3) !important;
    }
    
    button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #ff3385 0%, #ff0066 100%) !important;
        box-shadow: 0 6px 16px rgba(255,0,110,0.5) !important;
    }
    
    /* General button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,212,255,0.3) !important;
        padding: 12px 20px !important;
        border-radius: 6px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00f5ff 0%, #00ccee 100%) !important;
        box-shadow: 0 6px 16px rgba(0,212,255,0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Card rendering - force opaque and color */
    [data-testid="element-container"] div[style*="background:#ffffff"] {
        opacity: 1 !important;
        color: inherit !important;
    }
    
    [data-testid="element-container"] div[style*="background:#ffffff"] div {
        opacity: 1 !important;
        color: inherit !important;
    }
    
    /* Poker card classes */
    .poker-card {
        display: inline-block;
        width: 65px;
        height: 85px;
        background: #ffffff !important;
        border: 3px solid #000 !important;
        border-radius: 4px;
        padding: 2px;
        margin: 5px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.6);
        text-align: center;
        vertical-align: middle;
        opacity: 1 !important;
    }
    
    .poker-card-rank {
        display: block;
        font-size: 28px;
        font-weight: 900 !important;
        line-height: 0.9;
        letter-spacing: 1px;
        opacity: 1 !important;
    }
    
    .poker-card-suit {
        display: block;
        font-size: 24px;
        font-weight: 900 !important;
        opacity: 1 !important;
    }
    
    .card-black .poker-card-rank,
    .card-black .poker-card-suit {
        color: #000000 !important;
        opacity: 1 !important;
    }
    
    .card-red .poker-card-rank,
    .card-red .poker-card-suit {
        color: #cc0000 !important;
        opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_game() -> None:
    """Initialize game in session state."""
    if "game" not in st.session_state:
        human = Player("You", DEFAULT_STARTING_STACK, is_ai=False)
        ai = Player(
            "PokerMind AI",
            DEFAULT_STARTING_STACK,
            is_ai=True,
            ai_style=st.session_state.get("sidebar_ai_opponent", AI_STYLE_BALANCED),
        )
        game = PokerGame(human, ai, DEFAULT_SMALL_BLIND, DEFAULT_BIG_BLIND)
        st.session_state.game = game
        st.session_state.ai_logic = PokerAI(ai_style=ai.ai_style)

        st.session_state.game.start_new_hand()
        st.session_state.game_log = []


def get_game() -> PokerGame:
    """Get current game instance."""
    if "game" not in st.session_state:
        initialize_game()
    return st.session_state.game


def render_header() -> None:
    """Render app header."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 48px; margin: 0;'>♠️ PokerMind AI ♥️</h1>
            <p style='color: rgba(255,255,255,0.7); margin: 5px 0; font-size: 16px;'>
                Texas Hold'em • Heads-Up • AI-Powered
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()


def render_sidebar() -> None:
    """Render settings sidebar."""
    with st.sidebar:
        st.markdown("## ⚙️ Game Settings")
        
        # AI Style selector
        ai_choice = st.selectbox(
            "🤖 AI Opponent",
            AI_STYLES,
            index=1,
            help="Choose AI personality",
            key="sidebar_ai_opponent"
        )
        
        # Starting stack
        starting_stack = st.slider(
            "💰 Starting Stack",
            min_value=100,
            max_value=5000,
            value=DEFAULT_STARTING_STACK,
            step=100,
            help="Chips per player at game start",
        )
        st.session_state.starting_stack = starting_stack

        # Blind sizes
        col1, col2 = st.columns(2)
        with col1:
            small_blind = st.slider(
                "🔹 Small Blind",
                min_value=1,
                max_value=50,
                value=DEFAULT_SMALL_BLIND,
                step=1,
            )
            st.session_state.small_blind = small_blind

        with col2:
            big_blind = st.slider(
                "🔸 Big Blind",
                min_value=small_blind * 2,
                max_value=200,
                value=DEFAULT_BIG_BLIND,
                step=1,
            )
            st.session_state.big_blind = big_blind

        st.divider()
        
        # Help section
        with st.expander("❓ How to Play", expanded=False):
            st.markdown("""
            ### 🎯 Game Objective
            Win chips by making the best poker hand or bluffing your opponent into folding.
            
            ### 🎴 Hand Rankings (Highest → Lowest)
            1. **Royal Flush** - A-K-Q-J-10, same suit
            2. **Straight Flush** - 5 consecutive, same suit
            3. **Four of a Kind** - 4 matching ranks
            4. **Full House** - 3 of a kind + pair
            5. **Flush** - 5 cards same suit
            6. **Straight** - 5 consecutive cards
            7. **Three of a Kind** - 3 matching ranks
            8. **Two Pair** - 2 different pairs
            9. **One Pair** - 2 matching ranks
            10. **High Card** - Highest single card
            
            ### 🃏 Game Streets
            - **PREFLOP** - You get 2 cards, first betting round
            - **FLOP** - 3 community cards revealed
            - **TURN** - 4th community card revealed
            - **RIVER** - 5th community card revealed
            - **SHOWDOWN** - Best 5-card hand wins pot
            
            ### 🎮 Your Actions
            - **FOLD** - Give up, lose your bet
            - **CHECK** - Pass without betting
            - **CALL** - Match current bet
            - **BET/RAISE** - Increase the bet
            - **ALL-IN** - Bet all your chips
            
            ### 💡 Tips
            - Play tight early (strong hands only)
            - Position matters (act after opponent = advantage)
            - Bet when ahead, fold when beat
            - Mix up your play to avoid predictability
            """)
        
        st.divider()
        
        # Educational mode
        st.markdown("### 📚 Learning")
        educational = st.checkbox("Show AI analysis", value=True, help="Display equity & reasoning")
        st.session_state.educational_mode = educational

        if educational:
            num_sims = st.slider(
                "Monte Carlo Sims",
                min_value=100,
                max_value=5000,
                value=1000,
                step=100,
                help="More sims = more accurate",
            )
            st.session_state.num_sims = num_sims

        st.divider()

        # Game info
        game = get_game()
        st.markdown("### 📊 Match Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hand #", game.hand_number, delta=None)
        with col2:
            st.metric("Your Chips", format_stack(game.human.stack))
        
        st.metric("AI Chips", format_stack(game.ai.stack))

        st.divider()
        
        # Actions
        if st.button("🔄 New Match", use_container_width=True, key="sidebar_new_match"):
            st.session_state.clear()
            st.rerun()


def render_game_table(game: PokerGame) -> None:
    """Render the game table with players and cards."""
    
    # Street and Pot Row
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <div class='street-badge'>{game.street.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='pot-display'>
            💵 {format_pot(game.pot)}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        button_position = "🔘 BUTTON" if game.button_position == 0 else "💯 BUY-IN"
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; font-size: 12px; color: rgba(255,255,255,0.6);'>
            {button_position}
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Community Cards
    st.markdown("### 🃏 Community Cards")
    if game.community_cards:
        st.markdown(render_cards_html(game.community_cards), unsafe_allow_html=True)
        board_desc = format_board_texture(game.community_cards)
        st.caption(f"📈 {board_desc}")
    else:
        st.markdown("""
        <div style='text-align: center; padding: 20px; color: rgba(255,255,255,0.3);'>
            Waiting for flop...
        </div>
        """, unsafe_allow_html=True)
    
    # Deck and cards remaining
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if game.deck:
            cards_left = len(game.deck.cards)
        else:
            cards_left = 0
        st.metric("📚 Deck", f"{cards_left} cards", delta=None)
    
    with col2:
        community_count = len(game.community_cards)
        st.metric("🎲 Board", f"{community_count}/5", delta=None)
    
    with col3:
        st.metric("💰 Total Bets", format_pot(game.human.current_bet + game.ai.current_bet), delta=None)
    
    st.divider()
    
    # Player and AI comparison
    col_player, col_mid, col_ai = st.columns([1, 0.5, 1])
    
    with col_player:
        st.markdown("#### 🧑 Your Hand")
        if game.human.hole_cards:
            st.markdown(render_cards_html(game.human.hole_cards), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 20px; color: rgba(255,255,255,0.3);'>
                No cards dealt
            </div>
            """, unsafe_allow_html=True)
        
        # Your status
        status_items = []
        if game.human.folded:
            status_items.append("❌ Folded")
        if game.human.all_in:
            status_items.append("🚨 All-In")
        if game.active_player == game.human and not game.human.folded:
            status_items.append("👉 Your Turn")
        
        if status_items:
            st.caption(" • ".join(status_items))
        
        st.markdown(f"""
        <div class='player-section'>
            <div style='color: rgba(255,255,255,0.6); font-size: 12px;'>Your Bet</div>
            <div style='font-size: 18px; font-weight: bold; color: #00d4ff;'>{format_stack(game.human.current_bet)}</div>
            <div style='color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 10px;'>Stack</div>
            <div style='font-size: 20px; font-weight: bold;'>{format_stack(game.human.stack)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_mid:
        st.markdown("")
    
    with col_ai:
        st.markdown("#### 🤖 AI Hand")
        if game.street == STREET_SHOWDOWN and game.ai.hole_cards and not game.ai.folded:
            st.markdown(render_cards_html(game.ai.hole_cards), unsafe_allow_html=True)
        else:
            st.markdown(render_cards_html(game.ai.hole_cards, hidden=True), unsafe_allow_html=True)
        
        # AI status
        status_items = []
        if game.ai.folded:
            status_items.append("❌ Folded")
        if game.ai.all_in:
            status_items.append("🚨 All-In")
        if game.active_player == game.ai and not game.ai.folded:
            status_items.append("🤔 Thinking...")
        
        if status_items:
            st.caption(" • ".join(status_items))
        
        st.markdown(f"""
        <div class='ai-section'>
            <div style='color: rgba(255,255,255,0.6); font-size: 12px;'>AI Bet</div>
            <div style='font-size: 18px; font-weight: bold; color: #ff006e;'>{format_stack(game.ai.current_bet)}</div>
            <div style='color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 10px;'>Stack</div>
            <div style='font-size: 20px; font-weight: bold;'>{format_stack(game.ai.stack)}</div>
        </div>
        """, unsafe_allow_html=True)


def render_actions(game: PokerGame) -> None:
    """Render action buttons."""
    
    if game.is_hand_over() or game.human.folded:
        return
    
    if game.active_player != game.human:
        st.info("🤔 AI is thinking...")
        return
    
    st.markdown("### 🎮 Your Action")
    
    # Help text for actions
    st.info("""
    **FOLD** - Give up & lose your chips | **CHECK** - Pass without betting | 
    **CALL** - Match the bet | **BET/RAISE** - Increase the stake | 
    **ALL-IN** - Bet all remaining chips
    """)
    
    from core.betting import BettingRound

    legal_actions = BettingRound.legal_actions(
        game.human, game.current_round_bet_level, True
    )

    if not legal_actions:
        st.warning("No legal actions available")
        return

    # Create action columns
    action_cols = st.columns(5)
    
    with action_cols[0]:
        if ACTION_FOLD in legal_actions:
            if st.button("❌\nFOLD", use_container_width=True, key="fold_btn"):
                game.process_player_action(ACTION_FOLD)
                st.session_state.action_taken = True
                st.rerun()

    with action_cols[1]:
        if ACTION_CHECK in legal_actions:
            if st.button("✓\nCHECK", use_container_width=True, key="check_btn"):
                game.process_player_action(ACTION_CHECK)
                st.session_state.action_taken = True
                st.rerun()

    with action_cols[2]:
        if ACTION_CALL in legal_actions:
            call_amt = BettingRound.call_amount(game.human, game.current_round_bet_level)
            btn_text = f"📞\nCALL\n{format_stack(call_amt)}"
            if st.button(btn_text, use_container_width=True, key="call_btn"):
                game.process_player_action(ACTION_CALL)
                st.session_state.action_taken = True
                st.rerun()

    with action_cols[3]:
        if ACTION_BET in legal_actions or ACTION_RAISE in legal_actions:
            action_type = "BET" if ACTION_BET in legal_actions else "RAISE"
            if st.button(f"💰\n{action_type}", use_container_width=True, key="bet_raise_btn"):
                st.session_state.show_bet_slider = True

    with action_cols[4]:
        if ACTION_ALL_IN in legal_actions:
            btn_text = f"🚨\nALL-IN\n{format_stack(game.human.stack)}"
            if st.button(btn_text, use_container_width=True, key="allin_btn"):
                game.process_player_action(ACTION_ALL_IN, game.human.stack)
                st.session_state.action_taken = True
                st.rerun()

    # Bet/Raise slider if needed
    if st.session_state.get("show_bet_slider", False):
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            action_type = "bet" if ACTION_BET in legal_actions else "raise"
            amount = st.slider(
                f"Amount to {action_type}",
                min_value=1,
                max_value=game.human.stack,
                value=min(game.big_blind * 4, game.human.stack),
                step=max(1, game.big_blind),
            )
        with col2:
            action = ACTION_BET if ACTION_BET in legal_actions else ACTION_RAISE
            if st.button("✓ Confirm", use_container_width=True, key="confirm_bet"):
                game.process_player_action(action, amount)
                st.session_state.action_taken = True
                st.session_state.show_bet_slider = False
                st.rerun()


def render_hand_result(game: PokerGame) -> None:
    """Render hand result and award pot."""
    if not game.is_hand_over():
        return

    st.divider()
    
    winner, description = game.resolve_hand()

    if winner:
        if winner == game.human:
            st.success(f"### ✅ {description}")
            st.success(f"🎉 You won {format_pot(game.pot)}!")
        else:
            st.error(f"### ❌ {description}")
            st.error(f"😔 AI won {format_pot(game.pot)}")
    else:
        st.warning(f"### 🤝 {description}")

    st.divider()
    
    # Show community cards
    st.markdown("#### 📋 Community Cards")
    st.markdown(render_cards_html(game.community_cards), unsafe_allow_html=True)
    
    # Show final hands
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Your Hole Cards")
        st.markdown(render_cards_html(game.human.hole_cards), unsafe_allow_html=True)
    with col2:
        if not game.ai.folded or game.human.folded:
            st.markdown("#### AI Hole Cards")
            st.markdown(render_cards_html(game.ai.hole_cards), unsafe_allow_html=True)
    
    # Show best 5-card hands if at showdown
    if not game.human.folded and not game.ai.folded:
        st.markdown("---")
        st.markdown("#### 🏆 Best 5-Card Hands")
        
        human_best = HandEvaluator.best_hand_from_7(
            game.human.hole_cards, game.community_cards
        )
        ai_best = HandEvaluator.best_hand_from_7(
            game.ai.hole_cards, game.community_cards
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Your Best Hand:**")
            st.markdown(render_cards_html(human_best[2]), unsafe_allow_html=True)
            st.text(f"Hand: {HandEvaluator.hand_name(human_best[0])}")
        with col2:
            st.markdown("**AI Best Hand:**")
            st.markdown(render_cards_html(ai_best[2]), unsafe_allow_html=True)
            st.text(f"Hand: {HandEvaluator.hand_name(ai_best[0])}")

    st.divider()
    
    # Next hand button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Next Hand", use_container_width=True, key="next_hand_btn"):
            game.button_position = 1 - game.button_position
            game.start_new_hand()
            st.session_state.action_taken = False
            st.session_state.show_bet_slider = False
            st.rerun()

    with col2:
        if st.button("📊 View History", use_container_width=True, key="view_history_btn"):
            st.session_state.show_history = True

    # Check if match is over
    if game.is_match_over():
        st.divider()
        if game.human.stack <= 0:
            st.error("### 💔 Match Over!")
            st.error("You ran out of chips. Better luck next time!")
        else:
            st.success("### 🏆 Match Over!")
            st.success(f"🎉 You knocked out the AI! Final stack: {format_stack(game.human.stack)}")

        if st.button("🎮 New Match", use_container_width=True, key="endgame_new_match"):
            st.session_state.clear()
            st.rerun()


def render_educational_panel(game: PokerGame) -> None:
    """Render educational insights."""
    if not st.session_state.get("educational_mode", True):
        return

    with st.expander("📚 Hand Analysis", expanded=False):
        st.markdown("""
        **Equity** = Probability of winning against random opponent hands
        - **Win** - % chance you have best hand  
        - **Tie** - % chance of split pot  
        - **Loss** - % chance opponent has better hand
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Your Equity")
            if game.human.hole_cards and len(game.community_cards) > 0:
                win_rate, tie_rate, loss_rate = estimate_win_probability(
                    game.human.hole_cards,
                    game.community_cards,
                    num_simulations=st.session_state.get("num_sims", 1000),
                )
                
                col_eq1, col_eq2, col_eq3 = st.columns(3)
                with col_eq1:
                    st.metric("Win", f"{win_rate*100:.1f}%")
                with col_eq2:
                    st.metric("Tie", f"{tie_rate*100:.1f}%")
                with col_eq3:
                    st.metric("Loss", f"{loss_rate*100:.1f}%")

                best = HandEvaluator.best_hand_from_7(
                    game.human.hole_cards, game.community_cards
                )
                st.markdown(f"**Best Hand:** {HandEvaluator.hand_name(best[0])}")
            else:
                st.info("Play to see hand analysis")

        with col2:
            st.markdown("#### AI Analysis")
            if hasattr(st.session_state, "ai_last_explanation"):
                st.markdown(f"💭 {st.session_state.ai_last_explanation}")
            else:
                st.info("AI decisions will appear here")


def process_ai_action(game: PokerGame) -> None:
    """Process AI action if needed."""
    if game.active_player != game.ai or game.is_hand_over():
        return

    ai_logic = st.session_state.ai_logic
    action, amount, explanation = ai_logic.decide(
        game.ai,
        game.human,
        game.community_cards,
        game.current_round_bet_level,
        game.pot,
        game.street,
        game.action_history,
    )

    st.session_state.ai_last_explanation = explanation
    game.process_player_action(action, amount)

    if not game.is_hand_over() and game.active_player == game.ai:
        process_ai_action(game)


def main() -> None:
    """Main app."""
    st.set_page_config(
        page_title="PokerMind AI",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={"About": "PokerMind AI - Educational Texas Hold'em Poker with AI"}
    )
    
    add_custom_css()
    render_header()
    render_sidebar()

    game = get_game()
    
    # Show quick tips on first visit
    if "first_visit" not in st.session_state:
        st.session_state.first_visit = False
        with st.info("👋 **Welcome to PokerMind AI!** Expand the **'How to Play'** section in the sidebar to learn the rules. Check **'Hand Analysis'** below for equity info."):
            pass

    # Main game area
    render_game_table(game)
    render_actions(game)

    # Process AI action if needed
    if game.active_player == game.ai and not game.is_hand_over():
        with st.spinner("🤔 AI is thinking..."):
            process_ai_action(game)
            st.rerun()

    render_hand_result(game)
    render_educational_panel(game)


if __name__ == "__main__":
    main()
