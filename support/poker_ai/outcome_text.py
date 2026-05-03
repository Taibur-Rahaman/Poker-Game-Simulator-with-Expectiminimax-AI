"""Human-readable explanations of who won the last hand and why."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Mapping


def format_last_hand_why_won(
    summary: Dict[str, Any],
    name_by_index: Mapping[int, str],
    *,
    tone: Literal["standard", "kid"] = "standard",
) -> str:
    """
    Explain pot award: fold-away vs showdown vs split pot.
    Uses ``last_hand_summary`` from ``PokerGame`` (stage, winners, players rows).
    """
    winners: List[int] = list(summary.get("winners") or [])
    stage = str(summary.get("stage") or "")
    rows: List[Dict[str, Any]] = list(summary.get("players") or [])

    def nm(i: int) -> str:
        return str(name_by_index.get(i, f"Seat {i}"))

    win_names = [nm(i) for i in winners]
    if not winners or not rows:
        return ""

    showdown = stage == "showdown"
    row_by: Dict[int, Dict[str, Any]] = {int(r["player_index"]): r for r in rows}

    folded = [r for r in rows if r.get("ended_folded")]
    folded_who = [nm(int(r["player_index"])) for r in folded]

    if not showdown:
        wn_join = ", ".join(win_names)
        fh = (
            folded_who[0]
            if len(folded_who) == 1
            else ", ".join(folded_who)
            if folded_who
            else "the other player(s)"
        )
        if tone == "kid":
            return f"{wn_join} gets the pile because {fh} gave up — no cards were compared."
        if len(win_names) > 1:
            return (
                f"**Pot awarded to:** {wn_join}. Everyone else folded before showdown "
                "(hole cards were not compared)."
            )
        return (
            f"**{win_names[0]}** wins the pot because **{fh}** folded "
            "(no showdown — hole cards were not compared)."
        )

    if len(winners) >= 2:
        cats: List[str] = []
        for i in winners:
            r = row_by.get(i, {})
            c = str(r.get("category_name") or "").strip()
            if c and c != "—":
                cats.append(c)
        joined = ", ".join(win_names)
        if cats and len(set(cats)) == 1:
            tie = cats[0]
            if tone == "kid":
                return f"{joined} split — tied with {tie} when all cards were shown."
            return f"**{joined}** split the pot — tied best hand at showdown (**{tie}**)."
        if tone == "kid":
            return f"{joined} split the pile — same strength at showdown."
        return f"**{joined}** split the pot — tied best five-card hands at showdown."

    winner_ix = winners[0]
    wname = nm(winner_ix)
    wr = row_by.get(winner_ix, {})
    wcat = str(wr.get("category_name") or "—")

    showdown_losers = [
        r
        for r in rows
        if int(r["player_index"]) != winner_ix and not r.get("ended_folded") and str(r.get("category_name") or "").strip() not in ("", "—")
    ]

    if not showdown_losers:
        if tone == "kid":
            return f"{wname} had the strongest cards when everything was shown — {wcat}."
        return f"**{wname}** wins at showdown — best five from seven (**{wcat}**)."

    lr = showdown_losers[0]
    lname = nm(int(lr["player_index"]))
    lcat = str(lr.get("category_name") or "—")

    reason = ""
    wi = wr.get("category_index")
    lj = lr.get("category_index")
    if wi is not None and lj is not None:
        try:
            wi_i, lj_i = int(wi), int(lj)
            if wi_i > lj_i:
                reason = f"({wcat} outranks {lcat} on the standard list.) "
            elif wi_i == lj_i:
                reason = "(Same category — tiebreakers on the five winning cards settled it.) "
        except (TypeError, ValueError):
            pass

    if tone == "kid":
        if wcat != lcat:
            return (
                f"{wname} wins — {wcat} beats {lname}'s {lcat} when all cards were up."
            )
        return f"{wname} wins at the end — both had {wcat}, but {wname} won the tiebreak."

    if wcat != lcat:
        return (
            f"**{wname}** wins at showdown with **{wcat}** over **{lname}**'s **{lcat}**. {reason}".strip()
        )
    return (
        f"**{wname}** wins at showdown — **{wcat}** versus **{lname}**, but stronger kickers. {reason}".strip()
    )
