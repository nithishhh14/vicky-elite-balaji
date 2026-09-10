"""Vicky — Executive agent. Routes voice/text commands across the council."""
from __future__ import annotations

import re
from typing import Any, Callable

import google.generativeai as genai

import shared_memory as mem
from agents import email_agent, marketing_agent, scraper_agent, seo_agent


def speakable(text: str) -> str:
    """Strip markdown noise for TTS."""
    t = re.sub(r"[*_`#>•]", " ", text or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t[:600]


def _intent(command: str) -> str:
    c = (command or "").lower().strip()
    if any(x in c for x in ("run hunter", "scrape", "harvest", "find leads", "lead hunter", "maps")):
        return "scrape"
    if any(x in c for x in ("optimize", "clean sheet", "dedupe", "organise ledger", "organize ledger")):
        return "optimize"
    if c.startswith("seo ") or "seo" in c or "keyword" in c:
        return "seo"
    if any(x in c for x in ("marketing", "campaign", "instagram", "caption", "pitch")):
        return "marketing"
    if any(x in c for x in ("email", "mail draft", "write email")):
        return "email"
    if any(x in c for x in ("status", "who is online", "agents", "council")):
        return "status"
    return "chat"


def handle_command(
    command: str,
    *,
    leads_ws=None,
    book=None,
) -> dict[str, Any]:
    """Route a voice/text command. Returns {message, agent, data}."""
    q = mem.clean(command)
    if not q:
        return {"agent": "vicky", "ok": False, "message": "I am listening. Give me a command."}

    intent = _intent(q)

    if intent == "status":
        lines = ["Council status:"]
        for a in mem.AGENT_ROSTER:
            lines.append(f"- {a['name']} ({a['role']}): {a['status']}")
        msg = "\n".join(lines)
        return {"agent": "vicky", "ok": True, "message": msg, "intent": intent}

    if intent == "scrape":
        result = scraper_agent.run_scraper()
        if leads_ws is not None and result.get("ok"):
            opt = scraper_agent.optimize_leads(leads_ws, result.get("leads") or [])
            result["message"] = f"{result['message']}\n{opt['message']}"
            result["total"] = opt.get("total")
        if book is not None:
            mem.log_council(book, "scraper", "harvest", result.get("message", "")[:400])
        return result

    if intent == "optimize":
        if leads_ws is None:
            return {"agent": "scraper", "ok": False, "message": mem.PERM_MSG}
        result = scraper_agent.optimize_leads(leads_ws)
        if book is not None:
            mem.log_council(book, "scraper", "optimize", result.get("message", ""))
        return result

    if intent == "seo":
        # pull keyword after "seo" if present
        kw = re.sub(r"^\s*seo\s*", "", q, flags=re.I).strip() or q
        result = seo_agent.run_seo(kw)
        return result

    if intent == "marketing":
        return marketing_agent.run_marketing(q)

    if intent == "email":
        return email_agent.run_email(q)

    # Default: executive chat from shared memory
    mem.configure_gemini()
    model = genai.GenerativeModel(mem.GEMINI_MODEL)
    response = model.generate_content(
        "You are Vicky, Executive Agent for Elite Balaji Stones and Ceramics "
        f"(trusted since {mem.ESTABLISHED_SINCE}, Karamadai). "
        "You orchestrate Scraper, SEO, Marketing, and Email agents. "
        "Use shared council memory only. Coimbatore / Nilgiris hubs only. "
        "Never invent contractor phones. Be concise and actionable.\n\n"
        f"SHARED MEMORY:\n{mem.rules_text()}\n\n"
        f"STAFF COMMAND:\n{q}"
    )
    text = (getattr(response, "text", None) or "").strip()
    if not text:
        text = "I could not form a reply from shared memory. Try again."
    if book is not None:
        mem.log_council(book, "vicky", "chat", q[:120])
    return {"agent": "vicky", "ok": True, "message": text, "intent": "chat"}
