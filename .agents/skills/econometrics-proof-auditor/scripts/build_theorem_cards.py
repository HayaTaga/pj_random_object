#!/usr/bin/env python3
"""Draft compact theorem-card candidates from extracted corpus text.

Run from the repository root:

    python .agents/skills/econometrics-proof-auditor/scripts/build_theorem_cards.py
    python .agents/skills/econometrics-proof-auditor/scripts/build_theorem_cards.py --max-cards 50

The output is metadata for later human/Codex verification. It deliberately uses
short heading/context hints only; do not treat generated cards as verified
theorem statements.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TEXT_DIR = Path("corpus/extracted")
DEFAULT_OUT = Path("corpus/metadata/theorem_cards.yaml")
MAX_HEADING_CHARS = 180
MAX_CONTEXT_CHARS = 180

SOURCE_RE = re.compile(r"^=== Source: (.+) ===$")
PAGE_RE = re.compile(r"^=== Page ([0-9]+) ===$")
LEGACY_PAGE_RE = re.compile(r"^----- page ([0-9]+) -----$", re.IGNORECASE)
LABEL_RE = re.compile(
    r"\b(Theorem|Lemma|Proposition|Corollary|Assumption|Definition)\b(?:\s+([0-9A-Za-z.:-]+))?",
    re.IGNORECASE,
)

TOPIC_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("law of large numbers", re.compile(r"\blaw of large numbers\b|\bLLN\b", re.IGNORECASE)),
    ("central limit theorem", re.compile(r"\bcentral limit theorem\b|\bCLT\b", re.IGNORECASE)),
    ("continuous mapping theorem", re.compile(r"\bcontinuous mapping\b", re.IGNORECASE)),
    ("Slutsky theorem", re.compile(r"\bSlutsky(?:'s)?\b", re.IGNORECASE)),
    ("delta method", re.compile(r"\bdelta method\b", re.IGNORECASE)),
    ("uniform law of large numbers", re.compile(r"\buniform law of large numbers\b|\bULLN\b", re.IGNORECASE)),
    ("stochastic equicontinuity", re.compile(r"\bstochastic equicontinuity\b", re.IGNORECASE)),
    ("argmax theorem", re.compile(r"\barg[\s-]?max\b", re.IGNORECASE)),
    ("extremum estimator", re.compile(r"\bextremum estimator", re.IGNORECASE)),
    ("M-estimation", re.compile(r"\bM[- ]?estimat", re.IGNORECASE)),
    ("GMM", re.compile(r"\bGMM\b|generalized method of moments", re.IGNORECASE)),
    ("asymptotic normality", re.compile(r"\basymptotic normality\b", re.IGNORECASE)),
    ("consistency", re.compile(r"\bconsistency\b|\bconsistent\b", re.IGNORECASE)),
    ("sandwich variance", re.compile(r"\bsandwich\b", re.IGNORECASE)),
    ("identification", re.compile(r"\bidentification\b|\bidentified\b", re.IGNORECASE)),
    ("rank and nonsingularity", re.compile(r"\brank\b|\bnonsingular\b|\bpositive definite\b", re.IGNORECASE)),
]


@dataclass(frozen=True)
class TextLine:
    line_no: int
    page: int | None
    text: str


@dataclass(frozen=True)
class Candidate:
    text_file: Path
    pdf_file: str
    book_key: str
    page: int | None
    line_no: int
    label: str | None
    label_has_number: bool
    topic_hints: list[str]
    heading: str
    context_hint: str | None
    location_uncertain: bool


def yaml_quote(value: str | None) -> str:
    if value is None:
        return "null"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def truncate(text: str, max_chars: int) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def infer_pdf_from_text_path(path: Path, text_dir: Path) -> str:
    try:
        relative = path.relative_to(text_dir)
    except ValueError:
        relative = Path(path.name)
    return relative.with_suffix(".pdf").as_posix()


def book_key_for(path: Path, text_dir: Path) -> str:
    try:
        relative = path.relative_to(text_dir)
    except ValueError:
        relative = Path(path.name)
    return re.sub(r"[^A-Za-z0-9]+", "_", relative.with_suffix("").as_posix()).strip("_")


def parse_extracted_file(path: Path, text_dir: Path) -> tuple[str, list[TextLine]]:
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


def label_match_for(line: str) -> re.Match[str] | None:
    match = LABEL_RE.search(line)
    if not match:
        return None
    return match


def label_for(match: re.Match[str] | None) -> tuple[str | None, bool]:
    if not match:
        return None, False
    kind = match.group(1).title()
    raw_number = (match.group(2) or "").strip(".:-")
    if raw_number and not re.search(r"\d", raw_number):
        raw_number = ""
    label = " ".join(part for part in [kind, raw_number] if part)
    return label, bool(raw_number)


def looks_like_heading(line: str, match: re.Match[str] | None) -> bool:
    if not match:
        return False
    prefix = line[: match.start()].strip()
    if len(prefix) > 25:
        return False
    if not prefix:
        return True
    return bool(re.fullmatch(r"[0-9A-Za-z.() -]+", prefix))


def topic_hints_for(text: str) -> list[str]:
    return [name for name, rx in TOPIC_PATTERNS if rx.search(text)]


def context_hint(lines: list[TextLine], index: int) -> str | None:
    page = lines[index].page
    hints: list[str] = []
    for offset in (-1, 1):
        other_index = index + offset
        if other_index < 0 or other_index >= len(lines):
            continue
        other = lines[other_index]
        if other.page != page:
            continue
        hints.append(truncate(other.text, MAX_CONTEXT_CHARS))
    if not hints:
        return None
    return " | ".join(hints)


def iter_candidates(text_dir: Path) -> list[Candidate]:
    candidates: list[Candidate] = []

    for path in sorted(text_dir.rglob("*.txt")):
        if not path.is_file():
            continue
        pdf_file, lines = parse_extracted_file(path, text_dir)
        book_key = book_key_for(path, text_dir)
        for index, item in enumerate(lines):
            label_match = label_match_for(item.text)
            label, label_has_number = label_for(label_match)
            topic_hints = topic_hints_for(item.text)
            if not label and not topic_hints:
                continue
            if label and not label_has_number and not topic_hints and not looks_like_heading(item.text, label_match):
                continue
            candidates.append(
                Candidate(
                    text_file=path,
                    pdf_file=pdf_file,
                    book_key=book_key,
                    page=item.page,
                    line_no=item.line_no,
                    label=label,
                    label_has_number=label_has_number,
                    topic_hints=topic_hints,
                    heading=truncate(item.text, MAX_HEADING_CHARS),
                    context_hint=context_hint(lines, index),
                    location_uncertain=item.page is None or label is None or not label_has_number,
                )
            )

    return candidates


def card_id(candidate: Candidate, index: int) -> str:
    label_part = candidate.label or (candidate.topic_hints[0] if candidate.topic_hints else "candidate")
    raw = f"{candidate.book_key}_{label_part}_p{candidate.page or 'unknown'}_{candidate.line_no}_{index}"
    return re.sub(r"[^a-z0-9_]+", "_", raw.lower()).strip("_")


def write_cards(candidates: list[Candidate], out_path: Path) -> None:
    lines = [
        "# Auto-generated theorem-card candidates.",
        "# Verify labels, pages, conclusions, and conditions before citing.",
        "# Generated cards are not textbook quotations and are not verified theorem statements.",
        "cards:",
    ]

    for index, candidate in enumerate(candidates, start=1):
        lines.extend(
            [
                f"  - id: {card_id(candidate, index)}",
                "    source:",
                f"      book_key: {yaml_quote(candidate.book_key)}",
                f"      text_file: {yaml_quote(candidate.text_file.as_posix())}",
                f"      pdf_file: {yaml_quote(candidate.pdf_file)}",
                f"      page: {candidate.page if candidate.page is not None else 'null'}",
                f"      line: {candidate.line_no}",
                f"      label: {yaml_quote(candidate.label)}",
                f"      location_uncertain: {str(candidate.location_uncertain).lower()}",
            ]
        )
        if candidate.topic_hints:
            lines.append("    topic_hints:")
            for topic in candidate.topic_hints:
                lines.append(f"      - {yaml_quote(topic)}")
        else:
            lines.append("    topic_hints: []")
        lines.extend(
            [
                "    topic: null",
                "    use_case: null",
                "    sufficient_conditions: []",
                "    conclusion: null",
                "    common_misuse: null",
                "    proof_check_questions: []",
                "    related_cards: []",
                "    notes:",
                f"      - {yaml_quote('candidate heading: ' + candidate.heading)}",
            ]
        )
        if candidate.context_hint:
            lines.append(f"      - {yaml_quote('short context hint: ' + candidate.context_hint)}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Draft compact theorem-card candidates from extracted text without copying long passages."
    )
    parser.add_argument("--text-dir", default=str(DEFAULT_TEXT_DIR), help="Directory containing extracted .txt files.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output YAML metadata path.")
    parser.add_argument(
        "--limit-per-book",
        type=int,
        default=200,
        help="Maximum candidates to keep per text file.",
    )
    parser.add_argument("--max-cards", type=int, default=None, help="Optional global maximum number of cards.")
    args = parser.parse_args()

    text_dir = Path(args.text_dir)
    if not text_dir.exists():
        print(f"ERROR: text directory not found: {text_dir}", file=sys.stderr)
        print("Run extract_pdf_text.py first to populate corpus/extracted/.", file=sys.stderr)
        return 2
    if not text_dir.is_dir():
        print(f"ERROR: text path is not a directory: {text_dir}", file=sys.stderr)
        return 2
    if args.limit_per_book <= 0:
        print("ERROR: --limit-per-book must be positive.", file=sys.stderr)
        return 2
    if args.max_cards is not None and args.max_cards <= 0:
        print("ERROR: --max-cards must be positive.", file=sys.stderr)
        return 2

    all_candidates = iter_candidates(text_dir)
    kept: list[Candidate] = []
    per_book_counts: dict[str, int] = {}
    for candidate in all_candidates:
        count = per_book_counts.get(candidate.book_key, 0)
        if count >= args.limit_per_book:
            continue
        kept.append(candidate)
        per_book_counts[candidate.book_key] = count + 1
        if args.max_cards is not None and len(kept) >= args.max_cards:
            break

    out_path = Path(args.out)
    write_cards(kept, out_path)
    uncertain = sum(1 for candidate in kept if candidate.location_uncertain)
    print(f"wrote: {out_path}")
    print(f"text_dir: {text_dir}")
    print(f"candidates_found: {len(all_candidates)}")
    print(f"cards_written: {len(kept)}")
    print(f"location_uncertain: {uncertain}")
    if not kept:
        print("warning: no theorem-card candidates found", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
