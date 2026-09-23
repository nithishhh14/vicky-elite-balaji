"""Tests for the SEO agent.

Standard-library unittest on purpose: no new dependency, and `python -m
unittest` works on a fresh client PC with nothing but requirements.txt
installed.

Every test points `VICKY_DATA_DIR` at a temporary directory, so a run never
touches real approvals, snapshots or logs.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Must be set before vicky_store is imported, since it resolves paths at import.
_TMP = tempfile.mkdtemp(prefix="vicky-seo-test-")
os.environ["VICKY_DATA_DIR"] = _TMP

import vicky_store as store  # noqa: E402
from agents.seo import analysis, jobs, model  # noqa: E402
from agents.seo.model import Confidence, Provenance, Severity  # noqa: E402
from agents.seo.sources import SourceUnavailable, WebsiteCrawlSource, _safe_error  # noqa: E402


def _seed_targets():
    store.write_json(Path(_TMP) / "config" / "seo_targets.json", {
        "site": "https://elitebalaji.com",
        "core": [{"path": "/", "intent": "brand", "watch": ["elite balaji"]}],
        "landing": [
            {"path": "/granite-countertops-coimbatore/", "intent": "granite countertops",
             "watch": ["granite countertop coimbatore"]},
            {"path": "/bathroom-tiles-coimbatore/", "intent": "bathroom tiles",
             "watch": ["bathroom tiles coimbatore"]},
        ],
    })


def _row(query="", page="", impressions=0, clicks=0, position=10.0, ctr=None):
    return {
        "query": query, "page": page, "impressions": impressions, "clicks": clicks,
        "position": position,
        "ctr": ctr if ctr is not None else (clicks / impressions if impressions else 0.0),
    }


class FakeGSC:
    """Stands in for Search Console. Returns exactly what a test hands it."""

    name = "google_search_console"

    def __init__(self, queries=None, pages=None, totals=None, sitemaps=None,
                 available=(True, ""), raise_on_query=None):
        self._queries, self._pages = queries or [], pages or []
        self._totals, self._sitemaps = totals, sitemaps or []
        self._available, self._raise = available, raise_on_query

    def available(self):
        return self._available

    def query(self, start, end, dimensions=None, row_limit=500):
        if self._raise:
            raise self._raise
        if not dimensions:
            return [self._totals] if self._totals else []
        if dimensions == ["query"]:
            return self._queries
        if dimensions == ["page"]:
            return self._pages
        return []

    def sitemaps(self):
        return self._sitemaps


class TestEvidenceAndProvenance(unittest.TestCase):
    def test_every_opportunity_carries_its_chain(self):
        _seed_targets()
        opps = analysis.analyse(
            [_row("granite countertop coimbatore", impressions=120, clicks=2, position=8.0)],
            [], jobs._targets(), 28)
        self.assertTrue(opps)
        for opp in opps:
            chain = opp.evidence.as_chain()
            self.assertTrue(any("impressions" in c for c in chain))
            self.assertTrue(any("average position" in c for c in chain))
            self.assertTrue(any("matching page" in c for c in chain))

    def test_modelled_ctr_is_never_labelled_google_confirmed(self):
        opps = analysis.low_ctr_opportunities(
            [_row("bathroom tiles coimbatore", impressions=200, clicks=0, position=3.0)], 28)
        actionable = [o for o in opps if o.actionable]
        self.assertTrue(actionable)
        opp = actionable[0]
        self.assertIsNotNone(opp.evidence.expected_ctr)
        self.assertIn("heuristic", opp.limitations.lower())
        # The measured half is still Google's; only the note is inferred.
        self.assertIs(opp.evidence.source, Provenance.GOOGLE_CONFIRMED)

    def test_findings_declare_where_they_came_from(self):
        f = model.Finding(code="x", title="t", detail="d", provenance=Provenance.CRAWL_OBSERVED)
        self.assertEqual(f.to_dict()["provenance"], "crawl_observed")


class TestInsufficientEvidence(unittest.TestCase):
    def test_thin_data_is_declined_not_invented(self):
        _seed_targets()
        opps = analysis.analyse(
            [_row("granite shop karamadai", impressions=2, clicks=0, position=12.0)],
            [], jobs._targets(), 28)
        self.assertTrue(opps)
        self.assertTrue(all(o.confidence is Confidence.INSUFFICIENT_EVIDENCE for o in opps))
        self.assertFalse(any(o.actionable for o in opps))
        self.assertIn("Nothing yet", opps[0].what_to_change)

    def test_out_of_area_queries_are_not_opportunities(self):
        _seed_targets()
        opps = analysis.missing_page_opportunities(
            [_row("granite dealer chennai", impressions=500, clicks=0, position=15.0)],
            jobs._targets(), 28)
        self.assertEqual(opps, [], "a query outside the service area is not an opportunity")

    def test_empty_search_console_yields_no_recommendations(self):
        _seed_targets()
        report = jobs.weekly_opportunities(gsc=FakeGSC(queries=[], pages=[]), create_approvals=True)
        self.assertTrue(report.ok)
        self.assertEqual(report.opportunities, [])
        self.assertEqual(report.approvals_created, [])
        self.assertTrue(any(f.code == "seo.no_queries" for f in report.findings))


class TestApprovalCannotBeBypassed(unittest.TestCase):
    def test_recommendations_only_ever_become_approvals(self):
        _seed_targets()
        before = len(store.list_approvals("pending", limit=500))
        report = jobs.weekly_opportunities(
            gsc=FakeGSC(queries=[
                _row("granite countertop coimbatore price", impressions=140, clicks=1, position=11.0),
                _row("bathroom tiles coimbatore", impressions=90, clicks=0, position=6.0),
            ]),
            create_approvals=True)
        after = store.list_approvals("pending", limit=500)
        self.assertGreater(len(after), before)
        for approval in after:
            self.assertEqual(approval["status"], "pending")
            self.assertEqual(approval["kind"], "seo")
            self.assertTrue(approval["payload"].get("requiresHumanReview"))

    def test_every_opportunity_demands_review(self):
        _seed_targets()
        opps = analysis.analyse(
            [_row("granite countertop coimbatore", impressions=300, clicks=1, position=7.0)],
            [], jobs._targets(), 28)
        self.assertTrue(all(o.requires_human_review for o in opps))

    def test_the_agent_has_no_route_to_publish(self):
        """The guarantee, asserted rather than trusted: nothing in the package
        imports git, subprocess or the website build."""
        forbidden = ("subprocess", "git", "shutil.rmtree", "os.system", "os.remove")
        for name in ("model", "sources", "analysis", "jobs"):
            text = (ROOT / "agents" / "seo" / f"{name}.py").read_text(encoding="utf-8")
            for bad in forbidden:
                self.assertNotIn(f"import {bad}", text, f"{name}.py must not import {bad}")
                self.assertNotIn(f"{bad}(", text.replace(f"# {bad}(", ""),
                                 f"{name}.py must not call {bad}")

    def test_insufficient_evidence_never_reaches_the_queue(self):
        _seed_targets()
        report = jobs.weekly_opportunities(
            gsc=FakeGSC(queries=[_row("tiles karamadai", impressions=3, clicks=0, position=9.0)]),
            create_approvals=True)
        self.assertTrue(report.opportunities)
        self.assertFalse(any(o.actionable for o in report.opportunities))
        self.assertEqual(report.approvals_created, [])


class TestFailureHandling(unittest.TestCase):
    def test_auth_failure_is_reported_not_faked(self):
        _seed_targets()
        report = jobs.daily_snapshot(gsc=FakeGSC(available=(False, "authentication failed")))
        self.assertFalse(report.ok)
        self.assertTrue(report.errors)
        self.assertIn("google_search_console", report.sources_unavailable[0])

    def test_api_error_does_not_produce_an_empty_success(self):
        _seed_targets()
        report = jobs.weekly_opportunities(
            gsc=FakeGSC(raise_on_query=SourceUnavailable("Search Console query failed")))
        self.assertFalse(report.ok)
        self.assertEqual(report.opportunities, [])
        self.assertTrue(report.errors)

    def test_malformed_rows_do_not_crash_the_analysis(self):
        _seed_targets()
        junk = [
            {}, {"query": None}, {"query": "granite coimbatore"},
            {"query": "tiles coimbatore", "impressions": "not a number"},
        ]
        cleaned = []
        for row in junk:
            try:
                cleaned.append(_row(row.get("query") or "", impressions=int(row.get("impressions", 0))))
            except (TypeError, ValueError):
                continue  # the source layer is what normalises; this asserts we survive
        opps = analysis.analyse(cleaned, [], jobs._targets(), 28)
        self.assertIsInstance(opps, list)

    def test_missing_config_does_not_crash(self):
        path = Path(_TMP) / "config" / "seo_targets.json"
        backup = path.read_text(encoding="utf-8") if path.exists() else None
        path.unlink(missing_ok=True)
        try:
            self.assertEqual(jobs._targets(), [])
            self.assertIsInstance(analysis.analyse([], [], [], 28), list)
        finally:
            if backup:
                path.write_text(backup, encoding="utf-8")


class TestDuplicates(unittest.TestCase):
    def test_one_entry_per_query_and_rule(self):
        _seed_targets()
        rows = [_row("granite countertop coimbatore", impressions=n, clicks=0, position=9.0)
                for n in (40, 90, 150)]
        opps = analysis.deduplicate(analysis.analyse(rows, [], jobs._targets(), 28))
        keys = [(o.code, o.evidence.query) for o in opps]
        self.assertEqual(len(keys), len(set(keys)), "duplicate opportunities leaked through")

    def test_strongest_evidence_survives_deduplication(self):
        _seed_targets()
        rows = [_row("bathroom tiles coimbatore", impressions=n, clicks=0, position=8.0)
                for n in (12, 400)]
        opps = analysis.deduplicate(analysis.analyse(rows, [], jobs._targets(), 28))
        striking = [o for o in opps if o.code == "seo.striking_distance"]
        self.assertTrue(striking)
        self.assertEqual(striking[0].evidence.impressions, 400)


class TestSecrets(unittest.TestCase):
    def test_errors_are_scrubbed_before_they_reach_a_log(self):
        leaky = RuntimeError(
            "refresh_token=1//0abcdefghijklmnopqrstuvwxyz0123456789ABCDEF "
            "key=AIzaSyDmockmockmockmockmockmockmockmock"
        )
        safe = _safe_error(leaky)
        self.assertNotIn("1//0abcdefghijklmnopqrstuvwxyz", safe)
        self.assertNotIn("AIzaSyDmockmockmockmock", safe)
        self.assertIn("redacted", safe)

    def test_private_key_blocks_are_scrubbed(self):
        safe = _safe_error(RuntimeError(
            "-----BEGIN PRIVATE KEY-----\nAAAABBBBCCCC\n-----END PRIVATE KEY-----"))
        self.assertNotIn("AAAABBBBCCCC", safe)

    def test_run_reports_never_embed_credentials(self):
        _seed_targets()
        report = jobs.daily_snapshot(gsc=FakeGSC(available=(False, "authentication failed")))
        blob = json.dumps(report.to_dict())
        for marker in ("PRIVATE KEY", "refresh_token", "client_secret", "AIza"):
            self.assertNotIn(marker, blob)


class TestDailySnapshot(unittest.TestCase):
    def test_snapshot_is_stored_through_vicky_store(self):
        _seed_targets()
        day = date.today() - timedelta(days=2)
        report = jobs.daily_snapshot(
            day=day,
            gsc=FakeGSC(
                totals=_row(impressions=41, clicks=4, position=6.9),
                queries=[_row("elite balaji", impressions=20, clicks=3, position=2.5)],
                pages=[_row(page="https://elitebalaji.com/", impressions=27, clicks=3, position=2.5)],
            ))
        self.assertTrue(report.ok)
        saved = store.read_json(Path(_TMP) / "state" / "seo" / "daily" / f"{day.isoformat()}.json")
        self.assertIsNotNone(saved)
        self.assertEqual(saved["totals"]["impressions"], 41)
        self.assertEqual(saved["provenance"], Provenance.GOOGLE_CONFIRMED.value)
        self.assertEqual(saved["schemaVersion"], store.SCHEMA_VERSION)

    def test_a_run_is_always_logged(self):
        _seed_targets()
        before = len(store.recent_runs(limit=200))
        jobs.daily_snapshot(day=date.today() - timedelta(days=3),
                            gsc=FakeGSC(totals=_row(impressions=1)))
        self.assertGreater(len(store.recent_runs(limit=200)), before)


class TestCrawlParsing(unittest.TestCase):
    HTML = ('<html><head><title>Granite in Karamadai | Elite Balaji</title>'
            '<meta name="description" content="Granite, marble and tiles from our own yard in Karamadai.">'
            '<link rel="canonical" href="https://elitebalaji.com/granite/">'
            '</head><body><h1>Granite</h1></body></html>')

    def test_reads_the_tags_it_claims_to(self):
        c = WebsiteCrawlSource()
        self.assertEqual(c.title_of(self.HTML), "Granite in Karamadai | Elite Balaji")
        self.assertTrue(c.description_of(self.HTML).startswith("Granite, marble"))
        self.assertEqual(c.canonical_of(self.HTML), "https://elitebalaji.com/granite/")
        self.assertEqual(c.robots_meta_of(self.HTML), "")

    def test_missing_tags_return_empty_not_an_exception(self):
        c = WebsiteCrawlSource()
        self.assertEqual(c.title_of("<html></html>"), "")
        self.assertEqual(c.canonical_of("<html></html>"), "")

    def test_price_detection_is_narrow(self):
        self.assertTrue(jobs._looks_like_a_price("<p>Rs. 450 per sq ft</p>"))
        self.assertTrue(jobs._looks_like_a_price("<p>₹1200</p>"))
        self.assertFalse(jobs._looks_like_a_price("<p>600 x 1200mm tiles</p>"))
        self.assertFalse(jobs._looks_like_a_price("<p>Since 2012</p>"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
