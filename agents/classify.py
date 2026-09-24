"""Classification: rules first, Laya for what the rules cannot decide.

Measured before writing this, on real leads pulled from Google Maps:

    Laya, 3-way choice   4/9   collapsed to one label for every input
    Laya, binary         5/5   ~1000 ms per call on this laptop's CPU
    existing regex       5/5   0.8 ms for all five

So the honest finding is that replacing the rules with Laya would make the
system slower and no more accurate. The rules encode real local knowledge —
which Coimbatore suffixes mean a showroom, which mean a contractor — and they
are right about the cases they were built from.

What the rules cannot do is generalise. They fail on phrasings nobody wrote a
pattern for, on Tamil or transliterated names, and on businesses that describe
themselves in an unusual way. That is exactly where a small decision model
earns its second of latency.

Hence: the rules answer, and Laya is asked only when they abstain. On a
typical harvest that is a handful of calls, not hundreds.

Two things worth knowing before trusting a confidence from here:
  • Laya's headline is 32.8 ms on a T4 GPU. On this CPU it is about 1000 ms.
  • The typed-decisions checkpoint warns on load that it ships temperatures
    outside the valid range, so its probabilities are NOT calibrated despite
    the project's claims. They are treated as a ranking, never as a
    probability, and never shown to the client as one.
"""
from __future__ import annotations

import os
import threading
from typing import Any

#: Below this the model is not confident enough to overrule "unknown".
#: Deliberately high: an uncertain guess is worse than an honest abstention,
#: because a wrong lead costs a phone call to a restaurant.
MIN_CONFIDENCE = 0.55

_agent = None
_agent_lock = threading.Lock()
_agent_failed = False


def _get_agent():
    """Load Laya once, on first genuine need.

    Importing torch costs several seconds and ~500 MB; a harvest that never
    hits an ambiguous lead should never pay it. Failure is remembered so we
    do not retry the import on every call.
    """
    global _agent, _agent_failed
    if _agent is not None or _agent_failed:
        return _agent
    with _agent_lock:
        if _agent is not None or _agent_failed:
            return _agent
        try:
            from laya import Agent

            _agent = Agent(
                "convaiinnovations/laya",
                subfolder="typed-decisions",
                token=os.environ.get("HF_TOKEN"),
            )
        except Exception:
            _agent_failed = True
            _agent = None
        return _agent


def available() -> bool:
    """Whether the fallback can answer at all, without loading it to find out."""
    if _agent is not None:
        return True
    if _agent_failed:
        return False
    try:
        import importlib.util

        return importlib.util.find_spec("laya") is not None
    except Exception:
        return False


def ask_binary(subject: str, instructions: str, yes: str, no: str) -> tuple[bool | None, float]:
    """One yes/no question. Returns (answer, score), or (None, 0.0) if unsure.

    Binary on purpose. The same model given three labels returned the same
    label for every input, including a restaurant and a sweet shop — so the
    multi-way form is not trustworthy here and is not offered.
    """
    agent = _get_agent()
    if agent is None or not subject.strip():
        return None, 0.0
    question = {
        "q": {
            "type": "choice",
            "instructions": instructions,
            "criteria": {"yes": yes, "no": no},
        }
    }
    try:
        out = agent.predict(subject, question)
        ans = out["answers"]["q"]
        choice = ans["choice"]
        score = float(ans["probabilities"].get(choice, 0.0))
    except Exception:
        return None, 0.0
    if score < MIN_CONFIDENCE:
        return None, score
    return choice == "yes", score


def is_showroom(name: str, category: str = "", details: str = "") -> tuple[bool | None, str]:
    """Is this a stone/tile retail showroom — i.e. a competitor, not a customer?

    Returns (verdict, how_decided). `None` means genuinely undecided, which
    the caller should treat as "leave it in and let a human look", not as a no.
    """
    from lead_agent import is_retail_showroom, is_outreach_target

    if is_retail_showroom(name, category, details):
        return True, "rule"
    if is_outreach_target(name, category, details):
        return False, "rule"

    # The rules have no opinion. This is the case Laya exists for.
    subject = ", ".join(x for x in (name, category, details) if x)[:400]
    verdict, score = ask_binary(
        subject,
        "Does this business sell tiles, granite, marble or sanitaryware directly "
        "to the public from a shop or showroom?",
        yes="Yes, it is a stone, tile or sanitaryware shop or showroom.",
        no="No, it is not a stone or tile shop.",
    )
    if verdict is None:
        return None, f"undecided (laya score {score:.2f})" if score else "undecided (laya unavailable)"
    return verdict, f"laya {score:.2f}"


def query_intent(query: str) -> tuple[str, str]:
    """Commercial / local / informational, for the SEO agent's query analysis.

    The word lists in agents/seo/analysis.py catch the obvious cases at no
    cost. Anything they miss comes here — which matters because real search
    queries are exactly where unseen phrasing shows up.
    """
    from agents.seo.analysis import has_commercial_intent, has_local_intent

    if has_commercial_intent(query):
        return "commercial", "rule"
    if has_local_intent(query):
        return "local", "rule"

    verdict, score = ask_binary(
        f"Search query: {query}",
        "Is the person typing this query looking to buy or find a supplier, "
        "rather than just reading about the topic?",
        yes="They want to buy, get a price, or find a shop or supplier.",
        no="They only want information or ideas.",
    )
    if verdict is None:
        return "unknown", "undecided"
    return ("commercial" if verdict else "informational"), f"laya {score:.2f}"
