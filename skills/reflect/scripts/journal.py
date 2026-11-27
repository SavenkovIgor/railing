"""Manage the journal of the reflect skill: one JSON entry per run, one line per entry."""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

JOURNAL_FILE = Path.home() / ".local" / "state" / "railing" / "reflect" / "journal.jsonl"
MAX_AGE = timedelta(weeks=4)
ENTRY_FIELDS = {"date", "sessions", "failures", "coverage", "proposals"}
DECISIONS = {"applied", "skipped", "undecided"}


class EntryError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EntryError(message)


def validate_date(value: object) -> None:
    require(isinstance(value, str), "`date` must be a string in the form YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise EntryError(f"`date` must be in the form YYYY-MM-DD, got: {value}") from None


def validate_session(session: object) -> None:
    require(isinstance(session, dict), "each session must be a JSON object")
    require(isinstance(session.get("id"), str), "each session needs a string `id`")
    require(isinstance(session.get("failed"), list), "each session needs a list `failed` of criteria")


def validate_proposal(proposal: object) -> None:
    require(isinstance(proposal, dict), "each proposal must be a JSON object")
    require(isinstance(proposal.get("file"), str), "each proposal needs a string `file`")
    require(isinstance(proposal.get("text"), str), "each proposal needs a string `text`")
    require(proposal.get("decision") in DECISIONS, f"each proposal needs a `decision` from {sorted(DECISIONS)}")


def validate_entry(entry: object) -> None:
    require(isinstance(entry, dict), "the entry must be a JSON object")
    require(entry.keys() == ENTRY_FIELDS, f"the entry must have exactly the fields {sorted(ENTRY_FIELDS)}")
    validate_date(entry["date"])
    require(isinstance(entry["sessions"], list), "`sessions` must be a list")
    for session in entry["sessions"]:
        validate_session(session)
    failures = entry["failures"]
    require(isinstance(failures, dict), "`failures` must map each criterion to a count")
    require(all(type(count) is int for count in failures.values()), "each count in `failures` must be an integer")
    coverage = entry["coverage"]
    require(type(coverage) in (int, float) and 0 <= coverage <= 1, "`coverage` must be a share from 0 to 1")
    require(isinstance(entry["proposals"], list), "`proposals` must be a list")
    for proposal in entry["proposals"]:
        validate_proposal(proposal)


def parse_entry(text: str) -> dict:
    try:
        entry = json.loads(text)
    except json.JSONDecodeError as error:
        raise EntryError(f"the entry is not valid JSON: {error}") from None
    validate_entry(entry)
    return entry


def read_entries() -> list[dict]:
    if not JOURNAL_FILE.exists():
        return []
    lines = JOURNAL_FILE.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def write_entries(entries: list[dict]) -> None:
    JOURNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = JOURNAL_FILE.with_suffix(".tmp")
    lines = (json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries)
    temp_file.write_text("".join(lines), encoding="utf-8")
    temp_file.replace(JOURNAL_FILE)


def prune(entries: list[dict]) -> list[dict]:
    oldest = date.today() - MAX_AGE
    return [entry for entry in entries if date.fromisoformat(entry["date"]) >= oldest]


def reviewed_sessions(entries: list[dict]) -> list[str]:
    return sorted({session["id"] for entry in entries for session in entry["sessions"]})


def skipped_proposals(entries: list[dict]) -> list[dict]:
    proposals = (proposal for entry in entries for proposal in entry["proposals"])
    return [{"file": proposal["file"], "text": proposal["text"]} for proposal in proposals
            if proposal["decision"] == "skipped"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("reviewed", help="print the IDs of the reviewed sessions")
    commands.add_parser("skipped", help="print the skipped proposals with `file` and `text`")
    commands.add_parser("prune", help=f"delete the entries older than {MAX_AGE.days} days")
    append = commands.add_parser("append", help="validate an entry, prune, and append the entry")
    append.add_argument("entry", help="the entry as one JSON object")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = read_entries()
    if args.command == "reviewed":
        for session_id in reviewed_sessions(entries):
            print(session_id)
    elif args.command == "skipped":
        for proposal in skipped_proposals(entries):
            print(json.dumps(proposal, ensure_ascii=False))
    elif args.command == "prune":
        write_entries(prune(entries))
    else:
        try:
            entry = parse_entry(args.entry)
        except EntryError as error:
            sys.exit(f"Invalid entry, the journal is unchanged. Fix the entry and run append again: {error}")
        write_entries(prune(entries) + [entry])


if __name__ == "__main__":
    main()
