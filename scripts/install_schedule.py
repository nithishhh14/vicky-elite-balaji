"""Register Vicky's scheduled jobs with Windows Task Scheduler.

`vicky_data/config/schedule.json` has described the jobs since the day it was
written, but description is not execution — five days after the SEO agent went
in, exactly one snapshot existed, because nothing ran it. This turns the
config into real tasks.

    python scripts/install_schedule.py --dry-run     show what would be created
    python scripts/install_schedule.py               create them
    python scripts/install_schedule.py --verify      show their status
    python scripts/install_schedule.py --remove      remove them again

Only jobs whose agent is actually built get registered. The config also lists
marketing and website jobs; those are skipped with a reason rather than
scheduled to fail every morning at 10.

Deliberately Task Scheduler and not a daemon: it survives reboots, needs no
service to babysit, runs as the logged-in user so it inherits the same
credentials the dashboard uses, and the client can see and disable it in a UI
they already have.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PREFIX = "Vicky"
TASK_PATH = "\\" + PREFIX + "\\"
WRAPPER = BASE / "scripts" / "run_job.cmd"

#: job id -> (wrapper argument, PowerShell trigger expression, human text)
#: Only what exists. Adding the marketing agent later means adding a line.
RUNNABLE = {
    "seo-daily": ("daily", "New-ScheduledTaskTrigger -Daily -At 7:30am", "daily 07:30"),
    "seo-health": ("health", "New-ScheduledTaskTrigger -Daily -At 7:40am", "daily 07:40"),
    "seo-opportunities": (
        "weekly",
        "New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 8:00am",
        "Mon 08:00",
    ),
}

NOT_BUILT = {
    "campaign-weekly": "marketing agent not built",
    "campaign-post-reminder": "marketing agent not built",
    "website-inbox": "website agent not built",
    "leads-digest": "executive digest not built",
    "backup": "backup job not built",
    "security-monthly": "runs in CI, not on this machine",
}


def jobs() -> list[dict]:
    cfg = json.loads((BASE / "vicky_data" / "config" / "schedule.json").read_text(encoding="utf-8"))
    return cfg.get("jobs", [])


def _ps(script: str) -> tuple[bool, str]:
    res = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
    )
    return res.returncode == 0, (res.stdout or res.stderr).strip()


def register(job_id: str, arg: str, trigger: str) -> tuple[bool, str]:
    """Register one task through PowerShell rather than schtasks.

    schtasks bakes the surrounding quotes into the Execute field, so the task
    gets created, reports exit 0, and never runs the program — the most
    annoying possible failure. Register-ScheduledTask takes Execute, Argument
    and WorkingDirectory as separate values and quotes them correctly.
    """
    script = (
        f"$act = New-ScheduledTaskAction -Execute '{WRAPPER}' "
        f"-Argument '{arg}' -WorkingDirectory '{BASE}'; "
        f"$trg = {trigger}; "
        "$set = New-ScheduledTaskSettingsSet -StartWhenAvailable "
        "-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries "
        "-ExecutionTimeLimit (New-TimeSpan -Minutes 20); "
        f"Register-ScheduledTask -TaskName '{job_id}' -TaskPath '{TASK_PATH}' "
        "-Action $act -Trigger $trg -Settings $set -Force | Out-Null"
    )
    return _ps(script)


def install(dry: bool) -> int:
    if not WRAPPER.exists():
        print(f"missing wrapper: {WRAPPER}")
        return 1
    created = skipped = 0
    for job in jobs():
        jid = job["id"]
        if jid not in RUNNABLE:
            print(f"  skip  {jid:<24} {NOT_BUILT.get(jid, 'no runner defined')}")
            skipped += 1
            continue
        arg, trigger, human = RUNNABLE[jid]
        print(f"  task  {jid:<24} {human}")
        if dry:
            continue
        ok, err = register(jid, arg, trigger)
        if ok:
            created += 1
        else:
            print(f"        FAILED: {err[:160]}")
    total = len(RUNNABLE) if dry else created
    print(f"\n{'would create' if dry else 'created'}: {total}, skipped (agent not built): {skipped}")
    if not dry and created:
        print("Verify:  python scripts/install_schedule.py --verify")
        print("Output:  vicky_data/state/logs/schedule.log")
    return 0


def verify() -> int:
    for jid in RUNNABLE:
        _, out = _ps(
            f"$i = Get-ScheduledTaskInfo -TaskName '{jid}' -TaskPath '{TASK_PATH}' "
            "-ErrorAction SilentlyContinue; "
            'if ($i) { "$($i.LastRunTime) | $($i.LastTaskResult) | $($i.NextRunTime)" } '
            "else { 'not registered' }"
        )
        print(f"  {jid:<22} {out}")
    print("\n  columns: last run | last result (0 = ok) | next run")
    print("  A result of 0 with no matching line in schedule.log means the task fired")
    print("  but the command did nothing — read the log before trusting the exit code.")
    return 0


def remove() -> int:
    for jid in RUNNABLE:
        ok, _ = _ps(
            f"Unregister-ScheduledTask -TaskName '{jid}' -TaskPath '{TASK_PATH}' "
            "-Confirm:$false -ErrorAction SilentlyContinue"
        )
        print(f"  {'removed' if ok else 'not present'}  {jid}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    if a.remove:
        raise SystemExit(remove())
    if a.verify:
        raise SystemExit(verify())
    raise SystemExit(install(a.dry_run))
