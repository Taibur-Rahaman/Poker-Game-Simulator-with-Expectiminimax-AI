import streamlit as st
import time

from poker_ai.evaluation import run_simulation, summarize_results
from poker_ai.game_engine import PokerGame
from poker_ai.kid_ui import render_kid_play_tab
from poker_ai.visualization import inject_styles, render_last_hand_report, render_table


def render_new_player_help(game: PokerGame) -> None:
    """Right-side help panel for users who do not know poker."""
    st.markdown("#### New to poker? Start here")
    with st.expander("Quick guide: how this game works", expanded=True):
        st.markdown(
            """
            - **Goal**: Win chips by ending the hand with the best 5‑card poker hand or by making the opponent fold.
            - **Cards you use**:
              - You get **2 private cards** (your hand).
              - Up to **5 shared cards** appear in the middle (the board).
              - Your best 5‑card hand can use any combination of your 2 + 5 board cards.
            - **Stages**:
              - **Pre‑flop**: Only your 2 private cards are visible.
              - **Flop**: 3 board cards appear.
              - **Turn**: 4th board card appears.
              - **River**: 5th board card appears, then **showdown**.
            - **Your actions**:
              - **Fold**: Give up this hand and lose what you already put in the pot.
              - **Check**: Pass without betting (only when no bet is required).
              - **Call**: Match the current bet to stay in the hand.
              - **Raise**: Increase the bet, forcing the opponent to pay more to continue.
            """
        )

    stage_help = {
        "preflop": "Look at your two starting cards. High pairs (A‑A, K‑K, Q‑Q) and big cards of same suit are strong.",
        "flop": "Three board cards are visible. Check if you hit a pair, straight or flush draws, or strong made hands.",
        "turn": "Fourth board card. The pot is usually bigger; be more careful calling big raises.",
        "river": "Fifth and final board card. No more cards to come – decide if your hand is strong enough to win.",
        "showdown": "All cards are revealed. The best 5‑card hand wins the pot.",
    }

    st.markdown("#### What to look at this moment")
    current_stage = game.state.stage
    hint = stage_help.get(current_stage, "")
    if hint:
        st.markdown(f"- **Stage:** `{current_stage}`  \n- **Tip:** {hint}")

    st.markdown("#### About the AI decision panel")
    st.markdown(
        """
        - The **AI root decision analysis** lists each action and its estimated **EV (expected value)** in chips.
        - The AI chooses the action with the **highest EV**, based on many simulated future games.
        """
    )


def resolve_manual_play_status(game: PokerGame, status: str) -> str:
    """Advance streets until human turn or hand end for manual-vs-AI mode."""
    s = status
    guard = 0
    while s == "round_complete" and game.kid_interactive and guard < 8:
        s = game.kid_advance_street_or_end()
        guard += 1
    return s


def main() -> None:
    st.set_page_config(page_title="Poker Game Simulator with Expectiminimax AI", layout="wide")
    inject_styles()
    st.markdown("### Poker Game Simulator with **Expectiminimax AI**")

    if "game" not in st.session_state:
        st.session_state.game = PokerGame(num_players=2)
    game: PokerGame = st.session_state.game

    tab_play, tab_kid, tab_sim = st.tabs(["Play Game", "Kid Play 🎈", "Simulation & Evaluation"])

    with tab_play:

        col_left, col_right = st.columns([3, 2])

        with col_left:
            render_table(game)
            render_last_hand_report(game)

        with col_right:
            render_new_player_help(game)

            st.subheader("Controls")
            depth = st.slider("AI search depth", min_value=1, max_value=4, value=2, step=1)
            samples = st.slider("Monte Carlo samples", min_value=16, max_value=256, value=64, step=16)
            game.ai.max_depth = depth
            game.ai.num_samples = samples
            st.caption(
                f"Coins now → Buddy: **{game.players[0].stack}** · You: **{game.players[-1].stack}**"
            )
            c_reset, c_add_buddy, c_add_you = st.columns(3)
            with c_reset:
                if st.button("Reset coins", use_container_width=True):
                    for p in game.players:
                        p.stack = game.config.starting_stack
                    game.last_hand_summary = None
                    game.hand_action_log = []
                    st.session_state.last_winners = []
                    st.rerun()
            with c_add_buddy:
                if st.button("+500 Buddy", use_container_width=True):
                    game.players[0].stack += 500
                    st.rerun()
            with c_add_you:
                if st.button("+500 You", use_container_width=True):
                    game.players[-1].stack += 500
                    st.rerun()
            mode = st.radio(
                "Play mode",
                ["Manual vs AI (recommended)", "Auto hand (demo)"],
                index=0,
                help="Manual mode = you choose actions; AI controls the other side.",
            )
            manual_mode = mode.startswith("Manual")

            if manual_mode:
                if not game.kid_interactive:
                    st.caption(
                        "You are manual player. Opponent has `Expectiminimax` tag on table. "
                        "Click start, then act each turn."
                    )
                    if st.button("Start manual hand", type="primary"):
                        # If a player is busted, restart stacks for a fresh match before the next hand.
                        if any(p.stack <= 0 for p in game.players):
                            for p in game.players:
                                p.stack = game.config.starting_stack
                            game.last_hand_summary = None
                            game.hand_action_log = []
                            st.session_state.last_winners = []
                        game.kid_configure(human_seat=len(game.players) - 1)
                        status = game.kid_start_new_hand_interactive()
                        status = resolve_manual_play_status(game, status)
                        if not game.kid_interactive and game.last_hand_summary:
                            winners = game.last_hand_summary.get("winners", [])
                            st.session_state.last_winners = [
                                game.players[i].name for i in winners if 0 <= i < len(game.players)
                            ]
                        st.rerun()
                else:
                    st.caption("Hand in progress: you play `You`; opponent uses `Expectiminimax`.")
                    if game.kid_is_human_turn():
                        legal, call_amount, min_raise, _max_raise, _to_call = game.kid_current_legal_bundle()
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            if st.button("Fold", disabled="fold" not in legal, use_container_width=True):
                                status = game.kid_submit_engine_action("fold", None)
                                status = resolve_manual_play_status(game, status)
                                if not game.kid_interactive and game.last_hand_summary:
                                    winners = game.last_hand_summary.get("winners", [])
                                    st.session_state.last_winners = [
                                        game.players[i].name for i in winners if 0 <= i < len(game.players)
                                    ]
                                st.rerun()
                        with c2:
                            can_stay = "check" in legal or "call" in legal
                            if st.button("Check / Call", disabled=not can_stay, use_container_width=True):
                                if "check" in legal:
                                    act, amt = "check", None
                                else:
                                    act, amt = "call", call_amount
                                status = game.kid_submit_engine_action(act, amt)
                                status = resolve_manual_play_status(game, status)
                                if not game.kid_interactive and game.last_hand_summary:
                                    winners = game.last_hand_summary.get("winners", [])
                                    st.session_state.last_winners = [
                                        game.players[i].name for i in winners if 0 <= i < len(game.players)
                                    ]
                                st.rerun()
                        with c3:
                            if st.button("Raise", disabled="raise" not in legal, use_container_width=True):
                                status = game.kid_submit_engine_action("raise", min_raise)
                                status = resolve_manual_play_status(game, status)
                                if not game.kid_interactive and game.last_hand_summary:
                                    winners = game.last_hand_summary.get("winners", [])
                                    st.session_state.last_winners = [
                                        game.players[i].name for i in winners if 0 <= i < len(game.players)
                                    ]
                                st.rerun()
                    else:
                        st.info("Waiting for street transition...")
            else:
                if st.button("Play new hand"):
                    winners = game.play_hand()
                    st.session_state.last_winners = [w.name for w in winners]

            if "last_winners" in st.session_state:
                st.markdown("**Last hand winners:** " + ", ".join(st.session_state.last_winners))

            st.markdown("#### Hand activity (both sides)")
            action_log = getattr(game, "hand_action_log", [])
            if action_log:
                for i, line in enumerate(action_log, start=1):
                    st.write(f"{i}. {line}")
            else:
                st.caption("_Play a hand to see each move from both players._")

            st.markdown("---")
            st.markdown("**AI root decision analysis (estimated EV per action)**")
            analysis = getattr(game.ai, "last_root_analysis", [])
            if analysis:
                for action, amount, ev in analysis:
                    if amount is not None:
                        label = f"{action} ({amount})"
                    else:
                        label = action
                    st.write(f"- {label}: EV ≈ {ev:.1f}")
            else:
                st.write("_Play a hand to see analysis._")

    with tab_kid:
        render_kid_play_tab(game)

    with tab_sim:
        st.subheader("Automated Simulation")
        num_hands = st.slider("Number of hands", min_value=50, max_value=1000, value=200, step=50)
        depth = st.slider("AI search depth (simulation)", min_value=1, max_value=4, value=2, step=1)
        samples = st.slider("Monte Carlo samples (simulation)", min_value=16, max_value=256, value=64, step=16)
        compare_modes = st.checkbox("Compare with normal logic (side by side)", value=False)
        if st.button("Run simulation"):
            if compare_modes:
                compare_seed = int(time.time() * 1000) % 1_000_000_000
                df_ai = run_simulation(
                    num_hands=num_hands,
                    max_depth=depth,
                    num_samples=samples,
                    mode="expectiminimax",
                    seed=compare_seed,
                )
                df_normal = run_simulation(
                    num_hands=num_hands,
                    max_depth=depth,
                    num_samples=samples,
                    mode="normal",
                    seed=compare_seed,
                )
                st.session_state.sim_compare = {
                    "expectiminimax": df_ai,
                    "normal": df_normal,
                    "seed": compare_seed,
                }
                st.session_state.sim_df = None
            else:
                df = run_simulation(
                    num_hands=num_hands,
                    max_depth=depth,
                    num_samples=samples,
                    mode="expectiminimax",
                )
                st.session_state.sim_df = df
                st.session_state.sim_compare = None

        compare = st.session_state.get("sim_compare")
        df = st.session_state.get("sim_df")
        if compare:
            df_ai = compare["expectiminimax"]
            df_normal = compare["normal"]
            if not df_ai.empty and not df_normal.empty:
                st.caption(f"Both modes ran with the same seed: `{compare['seed']}`")
                s_ai = summarize_results(df_ai)
                s_normal = summarize_results(df_normal)
                st.markdown("#### Side-by-side output")
                left, right = st.columns(2)
                with left:
                    st.markdown("**Expectiminimax**")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Win rate", f"{s_ai['win_rate']*100:.1f}%")
                    c2.metric("Loss rate", f"{s_ai['loss_rate']*100:.1f}%")
                    c3.metric("Avg profit / hand", f"{s_ai['avg_profit']:.1f}")
                    c4.metric("Avg decision time (s)", f"{s_ai['avg_decision_time']:.3f}")
                with right:
                    st.markdown("**Normal logic**")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Win rate", f"{s_normal['win_rate']*100:.1f}%")
                    c2.metric("Loss rate", f"{s_normal['loss_rate']*100:.1f}%")
                    c3.metric("Avg profit / hand", f"{s_normal['avg_profit']:.1f}")
                    c4.metric("Avg decision time (s)", f"{s_normal['avg_decision_time']:.3f}")

                st.markdown("#### Delta (Expectiminimax - Normal)")
                d1, d2, d3, d4 = st.columns(4)
                d1.metric("Win rate delta", f"{(s_ai['win_rate'] - s_normal['win_rate']) * 100:.1f}%")
                d2.metric("Loss rate delta", f"{(s_ai['loss_rate'] - s_normal['loss_rate']) * 100:.1f}%")
                d3.metric("Profit delta", f"{s_ai['avg_profit'] - s_normal['avg_profit']:.1f}")
                d4.metric("Decision time delta (s)", f"{s_ai['avg_decision_time'] - s_normal['avg_decision_time']:.3f}")

                st.markdown("#### Cumulative profit comparison")
                cmp_plot = df_ai[["hand", "ai_delta"]].copy()
                cmp_plot["expectiminimax"] = cmp_plot["ai_delta"].cumsum()
                cmp_plot["normal"] = df_normal["ai_delta"].cumsum()
                st.line_chart(cmp_plot.set_index("hand")[["expectiminimax", "normal"]])

                st.markdown("#### Hand-by-hand output (size by size)")
                hand_cmp = df_ai[["hand", "ai_delta", "winner"]].rename(
                    columns={"ai_delta": "expectiminimax_delta", "winner": "expectiminimax_winner"}
                )
                hand_cmp["normal_delta"] = df_normal["ai_delta"].values
                hand_cmp["normal_winner"] = df_normal["winner"].values
                hand_cmp["delta_gap"] = hand_cmp["expectiminimax_delta"] - hand_cmp["normal_delta"]
                st.dataframe(hand_cmp, use_container_width=True)

        elif df is not None and not df.empty:
            summary = summarize_results(df)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Win rate", f"{summary['win_rate']*100:.1f}%")
            col2.metric("Loss rate", f"{summary['loss_rate']*100:.1f}%")
            col3.metric("Avg profit / hand", f"{summary['avg_profit']:.1f}")
            col4.metric("Avg decision time (s)", f"{summary['avg_decision_time']:.3f}")

            st.markdown("#### Win/Loss over time")
            df_plot = df.copy()
            df_plot["cum_profit"] = df_plot["ai_delta"].cumsum()
            st.line_chart(df_plot.set_index("hand")[["cum_profit"]])

            st.markdown("#### Profit distribution")
            st.bar_chart(df["ai_delta"].value_counts().sort_index())


if __name__ == "__main__":
    main()



