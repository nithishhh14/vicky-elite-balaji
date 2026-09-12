"""Shared memory baseline for the Elite Balaji multi-agent council."""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import gspread

import lead_agent as hunter

BASE_DIR = Path(__file__).resolve().parent
RULES_PATH = BASE_DIR / ".cursorrules"
CREDS_PATH = BASE_DIR / "google_creds.json"
MARBLE_PATH = BASE_DIR / "assets" / "black_gold_marble.jpg"

# Overridable via .env — lets the sheet (and the service account behind
# CREDS_PATH) be swapped to the verified Elite Balaji Google Business account
# later without a code change, just a .env + google_creds.json update.
SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "10-5n2epVeVhn9_ecRGd9xHpvmHkJ5qdwlGoHdMumwKg")
GEMINI_MODEL = "gemini-3.6-flash"

BUSINESS_NAME = "Elite Balaji Stones and Ceramics"
ESTABLISHED_SINCE = "2012"
PRIMARY_OFFICE_ADDRESS = (
    "12-B, Gandhi Nagar, Mettupalayam Main Road, Karamadai, Coimbatore (Dist - 641104)"
)
CONTACT_PHONE = "+91 91590 56767"

LEAD_HEADERS = [
    "Contractor Name",
    "Phone Number",
    "City Hub",
    "Source Platform",
    "Source Website",
    "Client Details",
    "Sourced At",
]
SEO_HEADERS = ["timestamp", "keyword", "analysis"]
CONTENT_HEADERS = ["timestamp", "format", "copy"]
EMAIL_HEADERS = ["timestamp", "to_name", "to_phone", "subject", "draft", "status"]
COUNCIL_HEADERS = ["timestamp", "agent", "action", "summary"]

PERM_MSG = (
    "Permission Error: Share the sheet as Editor with "
    "vicky-bot@elite-balaji-automation.iam.gserviceaccount.com"
)

AGENT_ROSTER = [
    {"id": "vicky", "name": "Vicky", "role": "Executive", "status": "ONLINE"},
    {"id": "scraper", "name": "Scraper", "role": "Lead harvest", "status": "READY"},
    {"id": "seo", "name": "SEO", "role": "Demand intel", "status": "STUB"},
    {"id": "marketing", "name": "Marketing", "role": "Campaigns", "status": "WAITING_WEBSITE"},
    {"id": "email", "name": "Email", "role": "Drafts only", "status": "WAITING_WEBSITE"},
]


def clean(v: Any) -> str:
    return hunter.clean(v)


def phone_digits(phone: str) -> str:
    return hunter.phone_digits(phone)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def rules_text() -> str:
    if RULES_PATH.exists():
        return RULES_PATH.read_text(encoding="utf-8")
    return f"BUSINESS={BUSINESS_NAME}\nSINCE={ESTABLISHED_SINCE}\nPHONE={CONTACT_PHONE}\n"


def open_sheet():
    if not CREDS_PATH.exists():
        raise FileNotFoundError("google_creds.json is missing")
    return gspread.service_account(filename=str(CREDS_PATH)).open_by_key(SHEET_ID)


def worksheet(sh, title: str, headers: list[str]):
    try:
        ws = sh.worksheet(title)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=title, rows=2000, cols=max(10, len(headers)))
        ws.append_row(headers)
        return ws
    values = ws.get_all_values()
    if not values:
        ws.append_row(headers)
        return ws
    return ws


def ensure_lead_headers(ws) -> None:
    values = ws.get_all_values()
    if not values:
        ws.update(values=[LEAD_HEADERS], range_name="A1:G1")
        return
    headers = [clean(h) for h in values[0]]
    if headers[:7] == LEAD_HEADERS:
        return
    body: list[list[str]] = []
    for row in values[1:]:
        lead = row_to_lead(row, headers)
        if not lead["name"]:
            continue
        body.append(
            [
                lead["name"],
                lead["phone"],
                lead["city"],
                lead["source"],
                lead["website"],
                lead["details"],
                lead["sourced_at"] or stamp(),
            ]
        )
    ws.clear()
    ws.update(values=[LEAD_HEADERS] + body, range_name=f"A1:G{1 + len(body)}")


def row_to_lead(row: list[str], headers: list[str]) -> dict[str, str]:
    mapped = {
        (headers[i] if i < len(headers) else f"c{i}").lower(): (row[i] if i < len(row) else "")
        for i in range(max(len(headers), len(row)))
    }
    sourced = clean(mapped.get("sourced at"))
    if not sourced and len(row) >= 8 and "custom pitch summary" in [h.lower() for h in headers]:
        sourced = clean(row[7] if len(row) > 7 else "")
    return {
        "name": clean(mapped.get("contractor name")),
        "phone": phone_digits(clean(mapped.get("phone number"))),
        "city": clean(mapped.get("city hub")) or "Coimbatore",
        "source": clean(mapped.get("source platform")) or "Unknown",
        "website": clean(mapped.get("source website")),
        "details": clean(mapped.get("client details")),
        "sourced_at": sourced,
    }


def optimize_sheet(ws, incoming: list[dict[str, str]] | None = None) -> int:
    ensure_lead_headers(ws)
    values = ws.get_all_values()
    headers = [clean(h) for h in (values[0] if values else LEAD_HEADERS)]
    bag: list[dict[str, str]] = []
    for row in values[1:] if len(values) > 1 else []:
        bag.append(row_to_lead(row, headers))
    if incoming:
        bag.extend(incoming)

    fake_phones = {"9443312345", "9842267890", "9159056767", "9486011223", "9629544556"}
    cleaned: list[dict[str, str]] = []
    for lead in bag:
        name = clean(lead.get("name"))
        phone = phone_digits(clean(lead.get("phone")))
        website = clean(lead.get("website"))
        city = clean(lead.get("city")) or "Coimbatore"
        source = clean(lead.get("source")) or "Unknown"
        details = clean(lead.get("details"))
        if not name or not website:
            continue
        if not hunter.is_clean_company_name(name):
            continue
        if not hunter.is_outreach_target(name, "", details):
            continue
        if phone in fake_phones or source.lower() in {"justdial", "olx"}:
            continue
        site_l = website.lower()
        if "google.com/goto" in site_l:
            continue
        if "/url?" in site_l and "instagram.com" not in site_l:
            continue
        if source == "Instagram" and "instagram.com" not in site_l:
            continue
        if re.match(
            r"^(civil\s+engineers?\s*,?\s*contractors?|tiles?\s+laying\s+contractors?|builders?\s+in\b)",
            name,
            re.I,
        ):
            continue
        if re.search(
            r"(contractors? in coimbatore|builders? in coimbatore|engineers?,?\s*contractors?\s*-)",
            name,
            re.I,
        ) and not re.search(r"\b(pvt|ltd|llp|associates|architects?|deejos)\b", name, re.I):
            if re.match(
                r"^(tiles?|civil|building|home)?\s*(flooring\s+)?(contractors?|builders?|engineers?)\b",
                name,
                re.I,
            ):
                continue
        blob = f"{name} {city} {details} {website}"
        if source in {"Instagram", "Buyer Signal"}:
            if not hunter.local_ok(blob + " coimbatore"):
                continue
        elif not hunter.local_ok(blob):
            continue
        if source in {"Google Maps", "Google Search", "Instagram"} and not (
            hunter.trade_ok(blob)
            or hunter.is_outreach_target(name, "", details)
        ):
            continue
        cleaned.append(
            {
                "name": name,
                "phone": phone,
                "city": city,
                "source": source,
                "website": website,
                "details": details,
                "sourced_at": clean(lead.get("sourced_at")) or stamp(),
            }
        )

    final = hunter.dedupe_leads(cleaned)
    preferred: list[dict[str, str]] = []
    for row in final:
        if row.get("phone"):
            preferred.append(row)
        elif row.get("source") in {"Google Maps", "Instagram"} and row.get("website"):
            preferred.append(row)
        elif row.get("source") == "Buyer Signal":
            preferred.append(row)

    matrix = [LEAD_HEADERS]
    for row in preferred:
        note = clean(row.get("details"))
        if not row.get("phone"):
            note = (note + " · Open Source Website for contact.").strip(" ·")
        matrix.append(
            [
                row["name"],
                row.get("phone") or "",
                row.get("city") or "Coimbatore",
                row.get("source") or "Unknown",
                row.get("website") or "",
                note[:260],
                clean(row.get("sourced_at")) or stamp(),
            ]
        )
    ws.clear()
    ws.update(values=matrix, range_name=f"A1:G{len(matrix)}")
    return max(0, len(matrix) - 1)


def load_ledger(ws) -> dict[str, list[str]]:
    cols = {h: [] for h in LEAD_HEADERS}
    values = ws.get_all_values()
    if len(values) < 2:
        return cols
    headers = [clean(h) for h in values[0]]
    rows = [row_to_lead(r, headers) for r in values[1:]]
    rows.sort(key=lambda r: (0 if r.get("phone") else 1, clean(r.get("name")).lower()))
    seen: set[str] = set()
    for lead in rows:
        name = lead["name"]
        phone = lead["phone"]
        website = lead["website"]
        if not name:
            continue
        key = phone if phone else f"{name.lower()}|{website.lower()}"
        if key in seen:
            continue
        seen.add(key)
        cols["Contractor Name"].append(name)
        cols["Phone Number"].append(phone or "—")
        cols["City Hub"].append(lead["city"] or "Coimbatore")
        cols["Source Platform"].append(lead["source"] or "Unknown")
        cols["Source Website"].append(website)
        cols["Client Details"].append(lead["details"])
        cols["Sourced At"].append(lead["sourced_at"])
    return cols


def log_council(book, agent: str, action: str, summary: str) -> None:
    try:
        ws = worksheet(book, "Council_Log", COUNCIL_HEADERS)
        ws.append_row([stamp(), agent, action, summary[:500]], value_input_option="USER_ENTERED")
    except Exception:
        pass


def configure_gemini() -> None:
    import google.generativeai as genai

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file — "
            "no key should ever be hardcoded in source."
        )
    genai.configure(api_key=key)
