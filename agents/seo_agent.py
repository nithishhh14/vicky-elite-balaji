"""SEO Agent — local demand notes (stub until website phase)."""
from __future__ import annotations

from typing import Any

import google.generativeai as genai

import shared_memory as mem


def run_seo(keyword: str) -> dict[str, Any]:
    term = mem.clean(keyword)
    if not term:
        return {"agent": "seo", "ok": False, "message": "Give SEO a keyword first."}
    mem.configure_gemini()
    model = genai.GenerativeModel(mem.GEMINI_MODEL)
    prompt = (
        f"SEO demand note for {mem.BUSINESS_NAME} (since {mem.ESTABLISHED_SINCE}). "
        f"Keyword: {term}. Coimbatore / Nilgiris hubs only. Short actionable bullets."
    )
    response = model.generate_content(
        f"COUNCIL MEMORY:\n{mem.rules_text()}\n\nTASK:\n{prompt}"
    )
    text = (getattr(response, "text", None) or "").strip()
    if not text:
        return {"agent": "seo", "ok": False, "message": "SEO Agent returned empty analysis."}
    try:
        book = mem.open_sheet()
        ws = mem.worksheet(book, "SEO_Audits", mem.SEO_HEADERS)
        ws.append_row([mem.stamp(), term, text], value_input_option="USER_ENTERED")
        mem.log_council(book, "seo", "analyze", f"keyword={term}")
    except Exception as exc:
        return {"agent": "seo", "ok": True, "analysis": text, "message": text, "warn": str(exc)}
    return {"agent": "seo", "ok": True, "analysis": text, "message": text}
