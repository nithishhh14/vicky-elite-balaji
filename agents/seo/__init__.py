"""SEO agent package.

Modular by source: `sources.py` owns every integration, `analysis.py` owns the
rules, `jobs.py` owns the three scheduled runs. Adding Business Profile or
Analytics later means a new class in `sources.py` and a registry entry — no
job needs to change.
"""
from .jobs import daily_snapshot, health_check, run_all, source_status, weekly_opportunities
from .model import Confidence, Evidence, Finding, Opportunity, Provenance, RunReport, Severity

__all__ = [
    "daily_snapshot", "health_check", "weekly_opportunities", "run_all", "source_status",
    "Confidence", "Evidence", "Finding", "Opportunity", "Provenance", "RunReport", "Severity",
]
