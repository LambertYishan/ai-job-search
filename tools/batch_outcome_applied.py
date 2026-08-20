import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


TRACKER_HEADER = [
    "date",
    "company",
    "sector",
    "role",
    "role_type",
    "channel",
    "status",
    "contact_person",
    "fit_rating",
    "notes",
    "cv_file",
    "cover_letter_file",
    "source",
    "deadline",
]

FINAL_STATUSES = {"hired", "rejected", "no_response", "no response", "offer_declined", "offer declined", "withdrawn"}
LATER_THAN_APPLIED = FINAL_STATUSES | {"interview", "offer"}


def parse_selected_numbers(text: str) -> list[int]:
    """Extract displayed job numbers from common batch-applied phrasings."""
    without_dates = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " ", text)
    return [int(match) for match in re.findall(r"\b\d+\b", without_dates)]


def apply_batch(
    last_results_path: str | Path,
    tracker_path: str | Path,
    numbers: list[int],
    *,
    today: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    last_results_path = Path(last_results_path)
    tracker_path = Path(tracker_path)
    last_results = _load_last_results(last_results_path)
    selected_numbers, duplicate_numbers = _dedupe_numbers(numbers)
    jobs_by_number, ambiguous_numbers = _index_last_results(last_results)
    invalid_numbers = [number for number in selected_numbers if number not in jobs_by_number]

    result: dict[str, Any] = {
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "flagged": [],
        "invalid": invalid_numbers,
        "duplicates": duplicate_numbers,
        "ambiguous": sorted(ambiguous_numbers),
        "applied_count": None,
        "preview": [],
    }

    if invalid_numbers or ambiguous_numbers:
        return result

    rows = _read_tracker(tracker_path)
    for number in selected_numbers:
        job = jobs_by_number[number]
        existing = _find_existing_row(rows, job)
        preview_status = existing.get("status", "") if existing else "(new row)"
        result["preview"].append(
            {
                "number": number,
                "company": _job_company(job),
                "title": _job_title(job),
                "current_status": preview_status,
                "proposed_status": "applied",
            }
        )
        if existing:
            status = existing.get("status", "").strip().lower()
            if status in LATER_THAN_APPLIED:
                result["flagged"].append(
                    {
                        "number": number,
                        "company": _job_company(job),
                        "title": _job_title(job),
                        "current_status": existing.get("status", ""),
                        "reason": "later_stage_status",
                    }
                )
                continue
            if status == "applied":
                result["unchanged"] += 1
                continue
            existing["status"] = "applied"
            if status == "drafted" or not existing.get("date"):
                existing["date"] = today
            existing["notes"] = _append_note(existing.get("notes", ""), _batch_note(today, number, job))
            _preserve_or_fill(existing, "source", _job_url(job))
            _preserve_or_fill(existing, "deadline", _job_deadline(job))
            _preserve_or_fill(existing, "fit_rating", _job_fit_rating(job))
            result["updated"] += 1
        else:
            rows.append(_new_tracker_row(job, number, today))
            result["created"] += 1

    if not dry_run and (result["created"] or result["updated"]):
        _write_tracker(tracker_path, rows)
    result["applied_count"] = sum(1 for row in rows if row.get("status", "").strip().lower() == "applied")
    return result


def _load_last_results(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing last results file: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ValueError("last_results.json must contain a top-level results array")
    return data


def _dedupe_numbers(numbers: list[int]) -> tuple[list[int], list[int]]:
    seen: set[int] = set()
    selected: list[int] = []
    duplicates: list[int] = []
    for number in numbers:
        if number in seen:
            if number not in duplicates:
                duplicates.append(number)
            continue
        seen.add(number)
        selected.append(number)
    return selected, duplicates


def _index_last_results(last_results: dict[str, Any]) -> tuple[dict[int, dict[str, Any]], set[int]]:
    indexed: dict[int, dict[str, Any]] = {}
    ambiguous: set[int] = set()
    for job in last_results["results"]:
        if not isinstance(job, dict):
            continue
        number = job.get("displayed_number")
        if not isinstance(number, int):
            continue
        if number in indexed:
            ambiguous.add(number)
            continue
        indexed[number] = job
    for number in ambiguous:
        indexed.pop(number, None)
    return indexed, ambiguous


def _read_tracker(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            rows.append({key: row.get(key, "") or "" for key in TRACKER_HEADER})
        return rows


def _write_tracker(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRACKER_HEADER)
        writer.writeheader()
        writer.writerows([{key: row.get(key, "") for key in TRACKER_HEADER} for row in rows])


def _find_existing_row(rows: list[dict[str, str]], job: dict[str, Any]) -> dict[str, str] | None:
    company = _normalize(_job_company(job))
    title = _normalize(_job_title(job))
    url = _job_url(job).strip().lower()
    for row in rows:
        row_url = row.get("source", "").strip().lower()
        if url and row_url == url:
            return row
        if _normalize(row.get("company", "")) == company and _normalize(row.get("role", "")) == title:
            return row
    return None


def _new_tracker_row(job: dict[str, Any], number: int, today: str) -> dict[str, str]:
    return {
        "date": today,
        "company": _job_company(job),
        "sector": str(job.get("sector") or job.get("bucket") or ""),
        "role": _job_title(job),
        "role_type": str(job.get("role_type") or "Full-time"),
        "channel": str(job.get("source_portal") or job.get("portal") or job.get("source") or "online"),
        "status": "applied",
        "contact_person": "",
        "fit_rating": _job_fit_rating(job),
        "notes": _batch_note(today, number, job),
        "cv_file": "",
        "cover_letter_file": "",
        "source": _job_url(job),
        "deadline": _job_deadline(job),
    }


def _append_note(existing: str, note: str) -> str:
    if not existing:
        return note
    if note in existing:
        return existing
    return f"{existing}; {note}"


def _batch_note(today: str, number: int, job: dict[str, Any]) -> str:
    parts = [f"{today} batch applied from last_results #{number}"]
    portal = job.get("source_portal") or job.get("portal")
    if portal:
        parts.append(f"portal={portal}")
    if job.get("fit"):
        parts.append(f"fit={job['fit']}")
    if job.get("rank_score") is not None:
        parts.append(f"rank_score={job['rank_score']}")
    return "; ".join(parts)


def _preserve_or_fill(row: dict[str, str], key: str, value: str) -> None:
    if not row.get(key) and value:
        row[key] = value


def _job_company(job: dict[str, Any]) -> str:
    return str(job.get("company") or "")


def _job_title(job: dict[str, Any]) -> str:
    return str(job.get("title") or job.get("role") or "")


def _job_url(job: dict[str, Any]) -> str:
    return str(job.get("url") or job.get("source") or "")


def _job_deadline(job: dict[str, Any]) -> str:
    deadline = job.get("deadline")
    return "" if deadline is None else str(deadline)


def _job_fit_rating(job: dict[str, Any]) -> str:
    if job.get("rank_score") is not None:
        return str(job["rank_score"])
    if job.get("fit_rating") is not None:
        return str(job["fit_rating"])
    return ""


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-mark numbered last-results jobs as applied.")
    parser.add_argument("text", nargs="*", help="Batch outcome text or explicit numbers.")
    parser.add_argument("--last-results", default="job_scraper/last_results.json")
    parser.add_argument("--tracker", default="job_search_tracker.csv")
    parser.add_argument("--today", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    numbers = parse_selected_numbers(" ".join(args.text))
    result = apply_batch(args.last_results, args.tracker, numbers, today=args.today, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))
    return 1 if result["invalid"] or result["ambiguous"] or result["flagged"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
