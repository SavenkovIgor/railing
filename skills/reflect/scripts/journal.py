"""Manage the journal of the reflect skill: one JSON entry per run, one line per entry."""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

JOURNAL_FILE = Path.home() / ".local" / "state" / "railing" / "reflect" / "journal.jsonl"
MAX_AGE = timedelta(weeks=4)
DECISIONS = {"applied", "skipped", "undecided"}


class EntryError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EntryError(message)


def validate(entry: object) -> None:
    require(isinstance(entry, dict), "the entry must be a JSON object")
    fields = {"date", "sessions", "failures", "coverage", "proposals"}
    require(entry.keys() == fields, f"the entry must have exactly the fields {sorted(fields)}")
    date.fromisoformat(entry["date"])
    for session in entry["sessions"]:
        require(isinstance(session.get("id"), str), "each session needs a string `id`")
        require(isinstance(session.get("failed"), list), "each session needs a list `failed`")
    require(all(isinstance(n, int) for n in entry["failures"].values()), "`failures` maps criteria to counts")
    require(0 <= entry["coverage"] <= 1, "`coverage` is a share from 0 to 1")
    for proposal in entry["proposals"]:
        require(isinstance(proposal.get("file"), str), "each proposal needs a string `file`")
        require(isinstance(proposal.get("text"), str), "each proposal needs a string `text`")
        require(proposal.get("decision") in DECISIONS, f"each proposal needs a `decision` from {sorted(DECISIONS)}")


def read_entries() -> list[dict]:
    if not JOURNAL_FILE.exists():
        return []
    lines = JOURNAL_FILE.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def write_entries(entries: list[dict]) -> None:
    JOURNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = JOURNAL_FILE.with_suffix(".tmp")
    temp_file.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries), encoding="utf-8")
    temp_file.replace(JOURNAL_FILE)


def prune(entries: list[dict]) -> list[dict]:
    oldest = date.today() - MAX_AGE
    return [e for e in entries if date.fromisoformat(e["date"]) >= oldest]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("reviewed", help="print the IDs of the reviewed sessions")
    commands.add_parser("skipped", help="print the skipped proposals with `file` and `text`")
    commands.add_parser("prune", help=f"delete entries older than {MAX_AGE.days} days")
    append = commands.add_parser("append", help="validate an entry, prune, and append the entry")
    append.add_argument("entry", help="the entry as one JSON object")
    args = parser.parse_args()

    entries = read_entries()
    if args.command == "reviewed":
        for session_id in sorted({s["id"] for e in entries for s in e["sessions"]}):
            print(session_id)
    elif args.command == "skipped":
        for proposal in (p for e in entries for p in e["proposals"] if p["decision"] == "skipped"):
            print(json.dumps({"file": proposal["file"], "text": proposal["text"]}, ensure_ascii=False))
    elif args.command == "prune":
        write_entries(prune(entries))
    else:
        try:
            entry = json.loads(args.entry)
            validate(entry)
        except (ValueError, TypeError, AttributeError, KeyError) as error:
            sys.exit(f"Invalid entry, the journal is unchanged: {error}")
        write_entries(prune(entries) + [entry])


if __name__ == "__main__":
    main()
