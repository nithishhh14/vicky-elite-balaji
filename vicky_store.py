"""Vicky's data layer — one place every agent reads and writes.

Plain JSON files under `vicky_data/`, standard library only, so it works
before any agent exists and on a fresh client PC with nothing installed.

Why files and not a database: the whole system is one operator on one PC plus
a static website. Files are inspectable, backed up by copying a folder, and
need no service to be running. `SCHEMA_VERSION` is stamped into every record
so a later move to Postgres/Supabase is a migration script, not a rewrite
(see docs/DAILY_OPS_AND_DASHBOARD.md §6).

Layout
------
vicky_data/
  config/      committed: what to track, campaign templates, the schedule
  state/       runtime: approvals, SEO snapshots, campaigns, run logs
  inbox/       client photos and catalogue PDFs waiting to be processed
  outbox/      generated drafts waiting for a person to post them
  backups/     Sheet exports and other dumps

Nothing here holds secrets. Lead exports under state/leads/ hold personal
data (names, phone numbers) and are gitignored — treat them like the Sheet.
"""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Literal

SCHEMA_VERSION = 1

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("VICKY_DATA_DIR", BASE_DIR / "vicky_data"))
CONFIG_DIR = DATA_DIR / "config"
STATE_DIR = DATA_DIR / "state"
APPROVALS_DIR = STATE_DIR / "approvals"
SEO_DIR = STATE_DIR / "seo" / "daily"
CAMPAIGNS_DIR = STATE_DIR / "campaigns"
LOGS_DIR = STATE_DIR / "logs"
LEADS_DIR = STATE_DIR / "leads"
INBOX_DIR = DATA_DIR / "inbox"
OUTBOX_DIR = DATA_DIR / "outbox"
BACKUPS_DIR = DATA_DIR / "backups"

ALL_DIRS = [
    CONFIG_DIR, APPROVALS_DIR, SEO_DIR, CAMPAIGNS_DIR, LOGS_DIR, LEADS_DIR,
    INBOX_DIR / "photos", INBOX_DIR / "catalogues", OUTBOX_DIR / "drafts", BACKUPS_DIR,
]

ApprovalKind = Literal["website", "campaign", "seo", "email", "other"]
ApprovalStatus = Literal["pending", "approved", "rejected"]
Channel = Literal["gbp", "whatsapp", "instagram", "email", "website"]
CampaignStatus = Literal["draft", "awaiting_approval", "scheduled", "posted", "archived"]


# ─────────────────────────── plumbing ───────────────────────────

def ensure_dirs() -> None:
    for d in ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"


def read_json(path: Path, default: Any = None) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, data: Any) -> Path:
    """Atomic write: a crash mid-write can never truncate an existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return path


def _stamp(record: dict[str, Any]) -> dict[str, Any]:
    record.setdefault("schemaVersion", SCHEMA_VERSION)
    record.setdefault("created", now())
    record["updated"] = now()
    return record


def config(name: str, default: Any = None) -> Any:
    """Read a committed config file, e.g. config("seo_targets")."""
    return read_json(CONFIG_DIR / f"{name}.json", default)


# ─────────────────────── approvals (the gate) ───────────────────────
# Every change an agent proposes lands here first. Nothing publishes itself.

def create_approval(
    kind: ApprovalKind,
    title: str,
    summary: str,
    *,
    payload: dict[str, Any] | None = None,
    preview_url: str = "",
    requested_by: str = "vicky",
) -> dict[str, Any]:
    record = _stamp({
        "id": new_id("apr"),
        "kind": kind,
        "title": title,
        "summary": summary,
        "payload": payload or {},
        "previewUrl": preview_url,
        "requestedBy": requested_by,
        "status": "pending",
        "decidedBy": "",
        "decidedAt": "",
        "note": "",
    })
    write_json(APPROVALS_DIR / f"{record['id']}.json", record)
    return record


def list_approvals(status: ApprovalStatus | None = "pending", limit: int = 50) -> list[dict[str, Any]]:
    items = [read_json(p, {}) for p in sorted(APPROVALS_DIR.glob("apr-*.json"), reverse=True)]
    items = [i for i in items if i and (status is None or i.get("status") == status)]
    return items[:limit]


def decide_approval(approval_id: str, decision: ApprovalStatus, *, by: str = "owner", note: str = "") -> dict[str, Any] | None:
    path = APPROVALS_DIR / f"{approval_id}.json"
    record = read_json(path)
    if not record:
        return None
    record.update(status=decision, decidedBy=by, decidedAt=now(), note=note)
    write_json(path, _stamp(record))
    return record


# ─────────────────────────── daily SEO ───────────────────────────
# One snapshot per day, so trends come from our own history and never from a
# guess. `totals` and `queries` come from Search Console once it is connected.

def save_seo_day(day: str | date, data: dict[str, Any]) -> dict[str, Any]:
    day = day.isoformat() if isinstance(day, date) else day
    record = _stamp({"date": day, **data})
    write_json(SEO_DIR / f"{day}.json", record)
    return record


def seo_history(days: int = 30) -> list[dict[str, Any]]:
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    out = []
    for p in sorted(SEO_DIR.glob("*.json")):
        if p.stem >= cutoff:
            record = read_json(p)
            if record:
                out.append(record)
    return out


def latest_seo() -> dict[str, Any] | None:
    files = sorted(SEO_DIR.glob("*.json"))
    return read_json(files[-1]) if files else None


def seo_delta(metric: str = "clicks", days: int = 7) -> float | None:
    """Change in a metric between the two most recent halves of the window."""
    history = [h for h in seo_history(days * 2) if isinstance(h.get("totals", {}).get(metric), (int, float))]
    if len(history) < 2:
        return None
    half = len(history) // 2
    older = [h["totals"][metric] for h in history[:half]]
    newer = [h["totals"][metric] for h in history[half:]]
    if not older or not newer or sum(older) == 0:
        return None
    return round((sum(newer) / len(newer) - sum(older) / len(older)) / (sum(older) / len(older)) * 100, 1)


# ─────────────────────────── campaigns ───────────────────────────

def upsert_campaign(
    name: str,
    channel: Channel,
    body: str,
    *,
    campaign_id: str = "",
    status: CampaignStatus = "draft",
    scheduled_for: str = "",
    assets: Iterable[str] = (),
    approval_id: str = "",
    notes: str = "",
) -> dict[str, Any]:
    campaign_id = campaign_id or new_id("cmp")
    path = CAMPAIGNS_DIR / f"{campaign_id}.json"
    record = read_json(path, {})
    record.update({
        "id": campaign_id,
        "name": name,
        "channel": channel,
        "body": body,
        "status": status,
        "scheduledFor": scheduled_for,
        "assets": list(assets),
        "approvalId": approval_id,
        "notes": notes,
    })
    write_json(path, _stamp(record))
    return record


def list_campaigns(status: CampaignStatus | None = None, limit: int = 50) -> list[dict[str, Any]]:
    items = [read_json(p, {}) for p in sorted(CAMPAIGNS_DIR.glob("cmp-*.json"), reverse=True)]
    items = [i for i in items if i and (status is None or i.get("status") == status)]
    return items[:limit]


def due_campaigns(on: str | date | None = None) -> list[dict[str, Any]]:
    on = (on.isoformat() if isinstance(on, date) else on) or date.today().isoformat()
    return [c for c in list_campaigns("scheduled", limit=200) if (c.get("scheduledFor") or "")[:10] <= on]


# ─────────────────────────── run log ───────────────────────────
# Append-only JSONL per month: cheap to write, easy to tail, trivial to prune.

def log_run(agent: str, action: str, ok: bool, detail: str = "") -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    line = {"ts": now(), "agent": agent, "action": action, "ok": ok, "detail": detail[:500]}
    with open(LOGS_DIR / f"runs-{datetime.now():%Y-%m}.jsonl", "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


def recent_runs(limit: int = 20) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in sorted(LOGS_DIR.glob("runs-*.jsonl"), reverse=True):
        lines = path.read_text(encoding="utf-8").splitlines()
        for line in reversed(lines):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
            if len(out) >= limit:
                return out
    return out


# ─────────────────────────── housekeeping ───────────────────────────

def prune(days: int = 400) -> int:
    """Delete decided approvals and SEO snapshots older than `days`."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    removed = 0
    for path in list(APPROVALS_DIR.glob("apr-*.json")):
        record = read_json(path, {})
        decided = record.get("decidedAt") or ""
        if record.get("status") in {"approved", "rejected"} and decided and datetime.fromisoformat(decided) < cutoff:
            path.unlink(missing_ok=True)
            removed += 1
    keep_from = (cutoff.date()).isoformat()
    for path in list(SEO_DIR.glob("*.json")):
        if path.stem < keep_from:
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def _count(folder: Path) -> int:
    """Real files waiting in a folder — .gitkeep and hidden files don't count."""
    return len([p for p in folder.glob("*") if p.is_file() and not p.name.startswith(".")])


def stats() -> dict[str, Any]:
    """One call for the dashboard header."""
    seo = latest_seo() or {}
    return {
        "pendingApprovals": len(list_approvals("pending", limit=500)),
        "campaignsDraft": len(list_campaigns("draft", limit=500)),
        "campaignsScheduled": len(list_campaigns("scheduled", limit=500)),
        "seoLastRun": seo.get("date", ""),
        "seoClicks7dChangePct": seo_delta("clicks", 7),
        "inboxPhotos": _count(INBOX_DIR / "photos"),
        "inboxCatalogues": _count(INBOX_DIR / "catalogues"),
    }


ensure_dirs()
