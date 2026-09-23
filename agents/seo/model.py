"""The vocabulary the SEO agent reasons in.

The one idea everything else hangs off: **a fact and an opinion must never
look alike**. Search Console telling us a query got 41 impressions is not the
same kind of statement as our own guess that a page's click-through is low for
its position. Both are useful; presenting the second as the first is how an
agent quietly starts lying.

So every Finding carries a `Provenance`, and every Opportunity carries the
`Evidence` it was derived from. An Opportunity that cannot show its evidence
is not a recommendation — it is `INSUFFICIENT_EVIDENCE`, and says so.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class Provenance(str, Enum):
    """Where a statement came from. Printed next to every finding."""

    #: Returned by the Google Search Console API. A measurement, not a view.
    GOOGLE_CONFIRMED = "google_confirmed"
    #: We fetched the page ourselves and observed this. True of the site, but
    #: it is our observation of it, not Google's opinion of it.
    CRAWL_OBSERVED = "crawl_observed"
    #: Our reasoning on top of the two above. May be wrong. Never a fact.
    INFERRED = "inferred"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    #: Not a weak recommendation — an explicit refusal to make one.
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


@dataclass
class Evidence:
    """The chain behind a single opportunity, in the order a person reads it.

    Every field here is either measured or empty. Nothing is estimated into
    existence; `expected_ctr` is the one modelled number and it is labelled as
    inferred wherever it is shown.
    """

    query: str = ""
    page: str = ""
    impressions: int = 0
    clicks: int = 0
    ctr: float = 0.0
    position: float = 0.0
    matching_page: str = ""          # a page we already have that targets this
    expected_ctr: float | None = None  # INFERRED — from the position curve
    window_days: int = 0
    source: Provenance = Provenance.GOOGLE_CONFIRMED

    def as_chain(self) -> list[str]:
        """The evidence rendered as the reader's own reasoning path."""
        chain = [f"query: {self.query or '(page-level)'}"]
        if self.page:
            chain.append(f"page: {self.page}")
        chain += [
            f"impressions: {self.impressions}",
            f"clicks: {self.clicks}",
            f"CTR: {self.ctr * 100:.1f}%",
            f"average position: {self.position:.1f}",
        ]
        chain.append(f"matching page: {self.matching_page or 'none found'}")
        if self.expected_ctr is not None:
            chain.append(f"expected CTR at this position: {self.expected_ctr * 100:.1f}% (inferred)")
        chain.append(f"window: last {self.window_days} days")
        return chain

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["source"] = self.source.value
        return d


@dataclass
class Finding:
    """Something observed. Not a proposal — see Opportunity for that."""

    code: str
    title: str
    detail: str
    provenance: Provenance
    severity: Severity = Severity.INFO
    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["provenance"] = self.provenance.value
        d["severity"] = self.severity.value
        return d


@dataclass
class Opportunity:
    """A proposed change, with everything an owner needs to judge it.

    `requires_human_review` is always True. It is a field rather than a
    constant so the record carries the claim with it into the approvals
    queue — a reader should not have to know how this class was written.
    """

    code: str
    title: str
    what_to_change: str
    why: str
    evidence: Evidence
    affected_url: str = ""
    affected_file: str = ""
    seo_purpose: str = ""
    risks: str = ""
    confidence: Confidence = Confidence.MEDIUM
    limitations: str = ""
    requires_human_review: bool = True

    @property
    def actionable(self) -> bool:
        """False when we are declining to recommend rather than recommending."""
        return self.confidence is not Confidence.INSUFFICIENT_EVIDENCE

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "title": self.title,
            "whatToChange": self.what_to_change,
            "why": self.why,
            "evidence": self.evidence.to_dict(),
            "evidenceChain": self.evidence.as_chain(),
            "affectedUrl": self.affected_url,
            "affectedFile": self.affected_file,
            "seoPurpose": self.seo_purpose,
            "risks": self.risks,
            "confidence": self.confidence.value,
            "limitations": self.limitations,
            "requiresHumanReview": self.requires_human_review,
            "actionable": self.actionable,
        }

    def summary_text(self) -> str:
        """What the owner reads in the approvals queue."""
        lines = [self.what_to_change, "", f"Why: {self.why}", "", "Evidence:"]
        lines += [f"  · {step}" for step in self.evidence.as_chain()]
        if self.seo_purpose:
            lines += ["", f"Purpose: {self.seo_purpose}"]
        if self.risks:
            lines += [f"Risks: {self.risks}"]
        if self.limitations:
            lines += [f"Limitations: {self.limitations}"]
        lines += ["", f"Confidence: {self.confidence.value}. Needs your approval before anything changes."]
        return "\n".join(lines)


@dataclass
class RunReport:
    """Everything one job run did, for the run log and the dashboard."""

    job: str
    started: str
    finished: str = ""
    ok: bool = True
    sources_used: list[str] = field(default_factory=list)
    sources_unavailable: list[str] = field(default_factory=list)
    pages_processed: int = 0
    queries_processed: int = 0
    findings: list[Finding] = field(default_factory=list)
    opportunities: list[Opportunity] = field(default_factory=list)
    approvals_created: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "job": self.job,
            "started": self.started,
            "finished": self.finished,
            "ok": self.ok,
            "sourcesUsed": self.sources_used,
            "sourcesUnavailable": self.sources_unavailable,
            "pagesProcessed": self.pages_processed,
            "queriesProcessed": self.queries_processed,
            "findings": [f.to_dict() for f in self.findings],
            "opportunities": [o.to_dict() for o in self.opportunities],
            "approvalsCreated": self.approvals_created,
            "errors": self.errors,
        }

    def headline(self) -> str:
        bits = [f"{len(self.findings)} findings"]
        act = [o for o in self.opportunities if o.actionable]
        if act:
            bits.append(f"{len(act)} opportunities")
        held = [o for o in self.opportunities if not o.actionable]
        if held:
            bits.append(f"{len(held)} held for insufficient evidence")
        if self.errors:
            bits.append(f"{len(self.errors)} errors")
        return ", ".join(bits)
