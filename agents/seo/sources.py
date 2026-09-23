"""Where the SEO agent's facts come from.

Each source answers three questions: what am I called, am I available right
now, and what can you fetch from me. Jobs never import an API client directly
— they ask the registry what is available and work with whatever answers. That
is what makes adding Business Profile or Analytics later a new file here
rather than an edit to every job.

A source that is not configured says so out loud and returns nothing. It never
returns plausible-looking filler, because a job cannot tell the difference
between filler and data, and neither can the owner reading the result.
"""
from __future__ import annotations

import json
import re
import ssl
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Protocol

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDS_PATH = BASE_DIR / "google_creds.json"
GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
USER_AGENT = "VickySEOAgent/1.0 (+https://elitebalaji.com)"


class SourceUnavailable(RuntimeError):
    """Raised when a source cannot serve a request. Never swallowed silently."""


class Source(Protocol):
    name: str

    def available(self) -> tuple[bool, str]:
        """(is_available, human-readable reason when it is not)."""


# ────────────────────────── Google Search Console ──────────────────────────

class SearchConsoleSource:
    """Live Search Console data for one verified property.

    Authenticates with the service-account key already on this machine. The
    key is read by the Google client library from a path; its contents are
    never read, logged or returned by anything here.
    """

    name = "google_search_console"

    def __init__(self, site_url: str = "sc-domain:elitebalaji.com", creds_path: Path | None = None):
        self.site_url = site_url
        self.creds_path = creds_path or CREDS_PATH
        self._service = None

    def available(self) -> tuple[bool, str]:
        if not self.creds_path.exists():
            return False, f"service-account key not found at {self.creds_path.name}"
        try:
            self._connect()
        except Exception as exc:
            return False, f"authentication failed: {_safe_error(exc)}"
        return True, ""

    def _connect(self):
        if self._service is not None:
            return self._service
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
        except ImportError as exc:  # pragma: no cover - dependency is pinned
            raise SourceUnavailable(f"google client libraries missing: {exc}") from exc
        creds = service_account.Credentials.from_service_account_file(
            str(self.creds_path), scopes=GSC_SCOPES
        )
        self._service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        return self._service

    def list_properties(self) -> list[dict[str, str]]:
        svc = self._connect()
        return svc.sites().list().execute().get("siteEntry", [])

    def has_property(self) -> bool:
        return any(e.get("siteUrl") == self.site_url for e in self.list_properties())

    def query(
        self,
        start: date,
        end: date,
        dimensions: list[str] | None = None,
        row_limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Raw Search Console rows, normalised into plain dicts.

        Returns [] when the property has no data for the window — which is the
        truthful answer for a new site, and must not be mistaken for a failure.
        """
        svc = self._connect()
        body: dict[str, Any] = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "rowLimit": row_limit,
        }
        if dimensions:
            body["dimensions"] = dimensions
        try:
            resp = svc.searchanalytics().query(siteUrl=self.site_url, body=body).execute()
        except Exception as exc:
            raise SourceUnavailable(f"Search Console query failed: {_safe_error(exc)}") from exc
        out = []
        for row in resp.get("rows", []):
            keys = row.get("keys", [])
            item = {
                "clicks": int(row.get("clicks", 0)),
                "impressions": int(row.get("impressions", 0)),
                "ctr": float(row.get("ctr", 0.0)),
                "position": float(row.get("position", 0.0)),
            }
            for dim, key in zip(dimensions or [], keys):
                item[dim] = key
            out.append(item)
        return out

    def sitemaps(self) -> list[dict[str, Any]]:
        svc = self._connect()
        try:
            return svc.sitemaps().list(siteUrl=self.site_url).execute().get("sitemap", [])
        except Exception as exc:
            raise SourceUnavailable(f"sitemap list failed: {_safe_error(exc)}") from exc

    def inspect(self, page_url: str) -> dict[str, Any]:
        """URL Inspection — Google's own view of one page's index status."""
        svc = self._connect()
        try:
            resp = svc.urlInspection().index().inspect(
                body={"inspectionUrl": page_url, "siteUrl": self.site_url}
            ).execute()
        except Exception as exc:
            raise SourceUnavailable(f"URL inspection failed: {_safe_error(exc)}") from exc
        return resp.get("inspectionResult", {})


# ────────────────────────────── Website crawl ──────────────────────────────

class WebsiteCrawlSource:
    """What the live site actually serves, fetched by us.

    Deliberately stdlib-only and read-only: it issues GETs and parses what
    comes back. Everything it reports is `CRAWL_OBSERVED`, never presented as
    Google's opinion of the page.
    """

    name = "website_crawl"

    def __init__(self, origin: str = "https://elitebalaji.com", timeout: int = 20):
        self.origin = origin.rstrip("/")
        self.timeout = timeout

    def available(self) -> tuple[bool, str]:
        try:
            self.fetch("/robots.txt")
        except Exception as exc:
            return False, f"site unreachable: {_safe_error(exc)}"
        return True, ""

    def fetch(self, path: str) -> dict[str, Any]:
        url = path if path.startswith("http") else f"{self.origin}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        ctx = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
                body = resp.read()
                return {
                    "url": resp.geturl(),
                    "status": resp.status,
                    "content_type": resp.headers.get("Content-Type", ""),
                    "body": body.decode("utf-8", errors="replace"),
                    "redirected": resp.geturl() != url,
                }
        except urllib.error.HTTPError as exc:
            return {"url": url, "status": exc.code, "content_type": "", "body": "", "redirected": False}
        except Exception as exc:
            raise SourceUnavailable(f"fetch {url}: {_safe_error(exc)}") from exc

    # Parsing our own, known-shape HTML. Deliberately narrow: these read one
    # tag each and return "" when absent, which the caller treats as a finding.
    @staticmethod
    def title_of(html: str) -> str:
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        return _unescape(m.group(1).strip()) if m else ""

    @staticmethod
    def description_of(html: str) -> str:
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I | re.S)
        return _unescape(m.group(1).strip()) if m else ""

    @staticmethod
    def canonical_of(html: str) -> str:
        m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.I)
        return m.group(1).strip() if m else ""

    @staticmethod
    def robots_meta_of(html: str) -> str:
        m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.I)
        return m.group(1).strip().lower() if m else ""

    @staticmethod
    def sitemap_locs(xml: str) -> list[str]:
        return re.findall(r"<loc>(.*?)</loc>", xml, re.I | re.S)


# ─────────────────── declared-but-not-configured sources ───────────────────

class NotConfiguredSource:
    """A source we intend to add, kept visible so its absence is explicit.

    Registering these means a run report lists exactly what it could not see,
    instead of the reader having to remember what was never wired up.
    """

    def __init__(self, name: str, reason: str):
        self.name = name
        self._reason = reason

    def available(self) -> tuple[bool, str]:
        return False, self._reason


def default_registry(site_url: str = "sc-domain:elitebalaji.com",
                     origin: str = "https://elitebalaji.com") -> dict[str, Source]:
    """Every source the agent knows about, configured or not."""
    return {
        "google_search_console": SearchConsoleSource(site_url),
        "website_crawl": WebsiteCrawlSource(origin),
        "google_business_profile": NotConfiguredSource(
            "google_business_profile",
            "listing verification pending; GBP API also needs Google's approval",
        ),
        "google_analytics": NotConfiguredSource(
            "google_analytics", "no analytics on the site by choice — see docs/DAILY_OPS_AND_DASHBOARD.md"
        ),
        "competitor_research": NotConfiguredSource(
            "competitor_research", "manual today: docs/COMPETITOR_ANALYSIS.md"
        ),
        "keyword_volume": NotConfiguredSource(
            "keyword_volume", "no keyword tool connected; volumes are never estimated"
        ),
    }


# ────────────────────────────────── helpers ─────────────────────────────────

def _safe_error(exc: Exception) -> str:
    """An error message with anything key-shaped stripped out.

    Google client errors can quote request bodies and URLs carrying tokens.
    Run logs are written to disk and shown in the dashboard, so they get the
    shape of the failure and never the secret inside it.
    """
    text = f"{type(exc).__name__}: {exc}"
    text = re.sub(r"[A-Za-z0-9_\-]{32,}", "<redacted>", text)
    text = re.sub(r"(key|token|secret|password|credential)=[^\s&\"']+", r"\1=<redacted>", text, flags=re.I)
    text = re.sub(r"-----BEGIN[^-]+-----.*?-----END[^-]+-----", "<redacted key>", text, flags=re.S)
    return text[:300]


def _unescape(s: str) -> str:
    for a, b in (("&amp;", "&"), ("&#38;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&apos;", "'")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def yesterday() -> date:
    """Search Console lags ~2 days; callers asking for "the last complete day"
    still get a real date, and empty rows when Google has not finalised it."""
    return date.today() - timedelta(days=1)
