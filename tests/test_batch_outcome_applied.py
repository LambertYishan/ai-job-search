import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.batch_outcome_applied import apply_batch, parse_selected_numbers, TRACKER_HEADER


def write_last_results(path: Path) -> None:
    data = {
        "generated_at": "2026-08-20T12:00:00",
        "source": "scrape",
        "results": [
            {
                "displayed_number": 1,
                "company": "Alpha Bank",
                "title": "Quantitative Analyst",
                "url": "https://example.com/alpha",
                "source_portal": "linkedin-search",
                "fit": "high",
                "deadline": None,
            },
            {
                "displayed_number": 2,
                "company": "Beta Capital",
                "title": "Risk Model Analyst",
                "url": "https://example.com/beta",
                "source_portal": "freehire-search",
                "fit": "medium",
                "deadline": "2026-09-01",
            },
            {
                "displayed_number": 3,
                "company": "Gamma AI",
                "title": "Data Scientist",
                "url": "https://example.com/gamma",
                "source_portal": "swelist-search",
                "rank_score": 78,
                "rank_verdict": "Strong Fit",
            },
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def read_tracker(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_tracker(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_HEADER)
        writer.writeheader()
        writer.writerows(rows)


class BatchOutcomeAppliedTests(unittest.TestCase):
    def test_three_new_scrape_jobs_create_three_applied_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)

            result = apply_batch(last_results, tracker, [1, 2, 3], today="2026-08-20")

            rows = read_tracker(tracker)
            self.assertEqual(result["created"], 3)
            self.assertEqual(result["updated"], 0)
            self.assertEqual([row["status"] for row in rows], ["applied", "applied", "applied"])
            self.assertEqual(rows[0]["company"], "Alpha Bank")
            self.assertEqual(rows[1]["deadline"], "2026-09-01")
            self.assertEqual(rows[2]["fit_rating"], "78")

    def test_existing_drafted_row_updates_and_two_new_rows_are_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)
            write_tracker(
                tracker,
                [
                    {
                        "date": "2026-08-19",
                        "company": "Alpha Bank",
                        "sector": "Banking",
                        "role": "Quantitative Analyst",
                        "role_type": "Full-time",
                        "channel": "online",
                        "status": "drafted",
                        "contact_person": "",
                        "fit_rating": "82",
                        "notes": "drafted docs",
                        "cv_file": "cv/main_alpha.tex",
                        "cover_letter_file": "cover_letters/cover_alpha.tex",
                        "source": "https://example.com/alpha",
                        "deadline": "",
                    }
                ],
            )

            result = apply_batch(last_results, tracker, [1, 2, 3], today="2026-08-20")

            rows = read_tracker(tracker)
            alpha = rows[0]
            self.assertEqual(result["created"], 2)
            self.assertEqual(result["updated"], 1)
            self.assertEqual(alpha["status"], "applied")
            self.assertEqual(alpha["date"], "2026-08-20")
            self.assertEqual(alpha["cv_file"], "cv/main_alpha.tex")
            self.assertEqual(len(rows), 3)

    def test_later_stage_status_is_flagged_not_downgraded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)
            write_tracker(
                tracker,
                [
                    {
                        "date": "2026-08-18",
                        "company": "Alpha Bank",
                        "sector": "",
                        "role": "Quantitative Analyst",
                        "role_type": "",
                        "channel": "",
                        "status": "interview",
                        "contact_person": "",
                        "fit_rating": "",
                        "notes": "",
                        "cv_file": "",
                        "cover_letter_file": "",
                        "source": "https://example.com/alpha",
                        "deadline": "",
                    }
                ],
            )

            result = apply_batch(last_results, tracker, [1], today="2026-08-20")

            rows = read_tracker(tracker)
            self.assertEqual(result["created"], 0)
            self.assertEqual(result["updated"], 0)
            self.assertEqual(result["flagged"][0]["reason"], "later_stage_status")
            self.assertEqual(rows[0]["status"], "interview")

    def test_invalid_result_number_does_not_modify_tracker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)

            result = apply_batch(last_results, tracker, [99], today="2026-08-20")

            self.assertFalse(tracker.exists())
            self.assertEqual(result["invalid"], [99])

    def test_dry_run_previews_without_writing_tracker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)

            result = apply_batch(last_results, tracker, [1, 2], today="2026-08-20", dry_run=True)

            self.assertFalse(tracker.exists())
            self.assertEqual(result["created"], 2)
            self.assertEqual(result["updated"], 0)
            self.assertEqual(
                [(row["number"], row["company"], row["title"]) for row in result["preview"]],
                [(1, "Alpha Bank", "Quantitative Analyst"), (2, "Beta Capital", "Risk Model Analyst")],
            )

    def test_duplicate_number_input_creates_one_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)

            result = apply_batch(last_results, tracker, [1, 1, 1], today="2026-08-20")

            rows = read_tracker(tracker)
            self.assertEqual(result["created"], 1)
            self.assertEqual(result["duplicates"], [1])
            self.assertEqual(len(rows), 1)

    def test_rerunning_same_batch_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)

            first = apply_batch(last_results, tracker, [1, 2], today="2026-08-20")
            second = apply_batch(last_results, tracker, [1, 2], today="2026-08-20")

            rows = read_tracker(tracker)
            self.assertEqual(first["created"], 2)
            self.assertEqual(second["created"], 0)
            self.assertEqual(second["updated"], 0)
            self.assertEqual(len(rows), 2)

    def test_tracker_remains_parseable_for_report_workflows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_results = root / "last_results.json"
            tracker = root / "job_search_tracker.csv"
            write_last_results(last_results)

            apply_batch(last_results, tracker, [1, 2, 3], today="2026-08-20")

            rows = read_tracker(tracker)
            self.assertEqual(list(rows[0].keys()), TRACKER_HEADER)
            self.assertEqual(sum(1 for row in rows if row["status"] == "applied"), 3)

    def test_parses_natural_batch_number_variations(self):
        cases = {
            "/outcome applied 1 2 3 4 from last scrape": [1, 2, 3, 4],
            "/outcome applied 1,2,3,4": [1, 2, 3, 4],
            "/outcome mark 1 3 5 as applied": [1, 3, 5],
            "I applied to jobs 1, 3, and 5 from the last scrape": [1, 3, 5],
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(parse_selected_numbers(text), expected)


if __name__ == "__main__":
    unittest.main()
