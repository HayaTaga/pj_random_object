#!/usr/bin/env python3
"""Locate likely theorem-like statements in extracted econometrics corpus text.

Run from the repository root:

    python .agents/skills/econometrics-proof-auditor/scripts/locate_theorem.py
    python .agents/skills/econometrics-proof-auditor/scripts/locate_theorem.py "delta method"
    python .agents/skills/econometrics-proof-auditor/scripts/locate_theorem.py "GMM asymptotic normality"

The script searches corpus/extracted recursively and prints compact candidate
locations. It is a locator, not a passage reproducer; context is deliberately
short.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TEXT_DIR = Path("corpus/extracted")
DEFAULT_MAX_RESULTS = 40
DEFAULT_CONTEXT = 1
MAX_LINE_CHARS = 260
MAX_CONTEXT_CHARS = 220

SOURCE_RE = re.compile(r"^=== Source: (.+) ===$")
PAGE_RE = re.compile(r"^=== Page ([0-9]+) ===$")
LEGACY_PAGE_RE = re.compile(r"^----- page ([0-9]+) -----$", re.IGNORECASE)

LABEL_PATTERNS = [
    r"\bTheorem\b",
    r"\bProposition\b",
    r"\bLemma\b",
    r"\bCorollary\b",
    r"\bAssumption\b",
    r"\bDefinition\b",
]

TOPIC_PATTERNS = [
    r"\buniform law of large numbers\b",
    r"\bcentral limit theorem\b",
    r"\bcontinuous mapping(?: theorem)?\b",
    r"\bSlutsky(?:'s)?(?: theorem)?\b",
    r"\bdelta method\b",
    r"\bstochastic equicontinuity\b",
    r"\barg[\s-]?max\b",
    r"\bextremum estimator(?:s)?\b",
    r"\bGMM\b",
    r"\basymptotic normality\b",
    r"\bconsistency\b",
]

LABEL_RE = re.compile("|".join(f"(?:{pat})" for pat in LABEL_PATTERNS), re.IGNORECASE)
TOPIC_RE = re.compile("|".join(f"(?:{pat})" for pat in TOPIC_PATTERNS), re.IGNORECASE)


@dataclass(frozen=True)
class TextLine:
    line_no: int
    page: int | None
    text: str


@dataclass(frozen=True)
class Candidate:
    score: int
    source_file: Path
    pdf_file: str | None
    page: int | None
    line_no: int
    matched_line: str
    context: list[TextLine]
    triggers: list[str]


def truncate(text: str, max_chars: int) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def yaml_quote(text: str | None) -> str:
    if text is None:
        return "null"
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def infer_pdf_from_text_path(path: Path, text_dir: Path) -> str:
    try:
        relative = path.relative_to(text_dir)
    except ValueError:
        relative = Path(path.name)
    return relative.with_suffix(".pdf").as_posix()


def parse_extracted_file(path: Path, text_dir: Path) -> tuple[str | None, list[TextLine]]:
    source: str | None = None
    current_page: int | None = None
    lines: list[TextLine] = []

    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        stripped = line.strip()

        source_match = SOURCE_RE.match(stripped)
        if source_match:
            source = source_match.group(1)
            continue

        page_match = PAGE_RE.match(stripped) or LEGACY_PAGE_RE.match(stripped)
        if page_match:
            current_page = int(page_match.group(1))
            continue

        if stripped:
            lines.append(TextLine(line_no=line_no, page=current_page, text=line))

    return source or infer_pdf_from_text_path(path, text_dir), lines


def query_terms(query: str | None) -> list[str]:
    if not query:
        return []
    return [term.lower() for term in re.findall(r"[A-Za-z0-9']+", query) if term.strip()]


def compile_query(query: str | None) -> re.Pattern[str] | None:
    if not query:
        return None
    terms = query_terms(query)
    if not terms:
        return None
    pattern = ".*".join(re.escape(term) for term in terms)
    return re.compile(pattern, re.IGNORECASE)


def context_for(lines: list[TextLine], index: int, context: int) -> list[TextLine]:
    page = lines[index].page
    start = index
    before = 0
    while start > 0 and before < context:
        candidate = lines[start - 1]
        if candidate.page != page:
            break
        start -= 1
        before += 1

    end = index
    after = 0
    while end + 1 < len(lines) and after < context:
        candidate = lines[end + 1]
        if candidate.page != page:
            break
        end += 1
        after += 1

    return lines[start : end + 1]


def score_line(line: str, context_text: str, query: str | None, query_re: re.Pattern[str] | None) -> tuple[int, list[str]]:
    score = 0
    triggers: list[str] = []

    label_hits = LABEL_RE.findall(line)
    if label_hits:
        score += 8
        triggers.extend(sorted({hit.lower() for hit in label_hits}))

    topic_hits = TOPIC_RE.findall(line)
    if topic_hits:
        score += 5 * len(topic_hits)
        triggers.extend(sorted({hit.lower() for hit in topic_hits}))

    if query and query_re:
        terms = query_terms(query)
        lowered = context_text.lower()
        term_hits = sum(1 for term in terms if term in lowered)
        if query_re.search(line):
            score += 12
            triggers.append("query-line")
        elif query_re.search(context_text):
            score += 6
            triggers.append("query-context")
        elif terms and term_hits == len(terms):
            score += 4 + term_hits
            triggers.append("query-terms")
        elif score > 0 and term_hits:
            score += term_hits
            triggers.append("query-term-near-candidate")

    return score, sorted(set(triggers))


def iter_candidates(text_dir: Path, query: str | None, context: int) -> list[Candidate]:
    query_re = compile_query(query)
    candidates: list[Candidate] = []

    for path in sorted(text_dir.rglob("*.txt")):
        if not path.is_file():
            continue
        pdf_file, lines = parse_extracted_file(path, text_dir)
        for index, line in enumerate(lines):
            ctx = context_for(lines, index, context)
            context_text = " ".join(item.text for item in ctx)
            score, triggers = score_line(line.text, context_text, query, query_re)
            if score <= 0:
                continue
            if query and not any(trigger.startswith("query") for trigger in triggers):
                continue
            candidates.append(
                Candidate(
                    score=score,
                    source_file=path,
                    pdf_file=pdf_file,
                    page=line.page,
                    line_no=line.line_no,
                    matched_line=truncate(line.text, MAX_LINE_CHARS),
                    context=ctx,
                    triggers=triggers,
                )
            )

    return sorted(candidates, key=lambda item: (-item.score, item.source_file.as_posix(), item.line_no))


def print_candidate(index: int, candidate: Candidate) -> None:
    print("---")
    print(f"candidate: {index}")
    print(f"score: {candidate.score}")
    print(f"source_file: {yaml_quote(candidate.source_file.as_posix())}")
    print(f"pdf_file: {yaml_quote(candidate.pdf_file)}")
    print(f"page: {candidate.page if candidate.page is not None else 'null'}")
    print(f"line: {candidate.line_no}")
    print(f"triggers: {', '.join(candidate.triggers) if candidate.triggers else 'none'}")
    print(f"heading_or_matched_line: {yaml_quote(candidate.matched_line)}")
    print("context:")
    for item in candidate.context:
        prefix = ">" if item.line_no == candidate.line_no else "-"
        print(f"  {prefix} line {item.line_no}: {yaml_quote(truncate(item.text, MAX_CONTEXT_CHARS))}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Locate theorem, lemma, proposition, assumption, definition, and major asymptotic-tool candidates."
    )
    parser.add_argument("query", nargs="?", default=None, help="Optional query, e.g. 'delta method'.")
    parser.add_argument("--text-dir", default=str(DEFAULT_TEXT_DIR), help="Directory containing extracted .txt files.")
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS, help="Maximum candidates to print.")
    parser.add_argument("--context", type=int, default=DEFAULT_CONTEXT, help="Context lines on each side.")
    parser.add_argument("--limit", type=int, default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    text_dir = Path(args.text_dir)
    if not text_dir.exists():
        print(f"ERROR: text directory not found: {text_dir}", file=sys.stderr)
        print("Run extract_pdf_text.py first to populate corpus/extracted/.", file=sys.stderr)
        return 2
    if not text_dir.is_dir():
        print(f"ERROR: text path is not a directory: {text_dir}", file=sys.stderr)
        return 2
    if args.context < 0:
        print("ERROR: --context must be nonnegative.", file=sys.stderr)
        return 2

    max_results = args.limit if args.limit is not None else args.max_results
    if max_results <= 0:
        print("ERROR: --max-results must be positive.", file=sys.stderr)
        return 2

    candidates = iter_candidates(text_dir=text_dir, query=args.query, context=args.context)
    shown = candidates[:max_results]

    print(f"query: {yaml_quote(args.query)}")
    print(f"text_dir: {yaml_quote(text_dir.as_posix())}")
    print(f"max_results: {max_results}")
    print(f"candidates_found: {len(candidates)}")
    print(f"candidates_shown: {len(shown)}")

    for index, candidate in enumerate(shown, start=1):
        print_candidate(index, candidate)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
