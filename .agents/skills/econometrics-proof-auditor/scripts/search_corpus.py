#!/usr/bin/env python3
"""Search extracted econometrics corpus text with page-aware context.

Run from the repository root:

    python .agents/skills/econometrics-proof-auditor/scripts/search_corpus.py "uniform law of large numbers"
    python .agents/skills/econometrics-proof-auditor/scripts/search_corpus.py "stochastic equicontinuity" --context 3
    python .agents/skills/econometrics-proof-auditor/scripts/search_corpus.py "Theorem\\s+2\\.1" --regex --max-results 20

The script searches .txt files under corpus/extracted and prints compact,
Codex-readable result blocks. It never prints full pages.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TEXT_DIR = Path("corpus/extracted")
SOURCE_RE = re.compile(r"^=== Source: (.+) ===$")
PAGE_RE = re.compile(r"^=== Page ([0-9]+) ===$")
LEGACY_PAGE_RE = re.compile(r"^----- page ([0-9]+) -----$", re.IGNORECASE)
DEFAULT_MAX_RESULTS = 25
DEFAULT_CONTEXT = 2
MAX_LINE_CHARS = 240
MAX_MATCH_CHARS = 320


@dataclass(frozen=True)
class TextLine:
    line_no: int
    page: int | None
    text: str


@dataclass(frozen=True)
class MatchResult:
    result_no: int
    text_file: Path
    pdf_file: str | None
    page: int | None
    match_line_no: int
    line_start: int
    line_end: int
    matched_text: str
    context_lines: list[TextLine]


def truncate(text: str, max_chars: int = MAX_LINE_CHARS) -> str:
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
        relative = path.name
    if isinstance(relative, Path):
        return relative.with_suffix(".pdf").as_posix()
    return str(relative).removesuffix(".txt") + ".pdf"


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

        lines.append(TextLine(line_no=line_no, page=current_page, text=line))

    return source or infer_pdf_from_text_path(path, text_dir), lines


def compile_query(query: str, regex: bool, case_sensitive: bool) -> re.Pattern[str]:
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = query if regex else re.escape(query)
    try:
        return re.compile(pattern, flags)
    except re.error as exc:
        raise SystemExit(f"ERROR: invalid regular expression: {exc}") from exc


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


def iter_matches(
    text_dir: Path,
    rx: re.Pattern[str],
    context: int,
    max_results: int,
) -> list[MatchResult]:
    results: list[MatchResult] = []
    files = sorted(path for path in text_dir.rglob("*.txt") if path.is_file())

    for path in files:
        pdf_file, lines = parse_extracted_file(path, text_dir)
        for index, line in enumerate(lines):
            if not rx.search(line.text):
                continue
            ctx = context_for(lines, index, context)
            matched_text = truncate(line.text, MAX_MATCH_CHARS)
            results.append(
                MatchResult(
                    result_no=len(results) + 1,
                    text_file=path,
                    pdf_file=pdf_file,
                    page=line.page,
                    match_line_no=line.line_no,
                    line_start=ctx[0].line_no,
                    line_end=ctx[-1].line_no,
                    matched_text=matched_text,
                    context_lines=ctx,
                )
            )
            if len(results) >= max_results:
                return results
    return results


def print_result(result: MatchResult) -> None:
    print("---")
    print(f"result: {result.result_no}")
    print(f"text_file: {yaml_quote(result.text_file.as_posix())}")
    print(f"pdf_file: {yaml_quote(result.pdf_file)}")
    page_marker = f"=== Page {result.page} ===" if result.page is not None else None
    print(f"page_marker: {yaml_quote(page_marker)}")
    print(f"line_range: {yaml_quote(f'{result.line_start}-{result.line_end}')}")
    print(f"matched_text: {yaml_quote(result.matched_text)}")
    print("context:")
    for ctx_line in result.context_lines:
        prefix = ">" if ctx_line.line_no == result.match_line_no else "-"
        print(f"  {prefix} line {ctx_line.line_no}: {yaml_quote(truncate(ctx_line.text))}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search all .txt files under corpus/extracted with compact page-aware context."
    )
    parser.add_argument("query", help="Plain keyword query, or regex when --regex is set.")
    parser.add_argument("--text-dir", default=str(DEFAULT_TEXT_DIR), help="Directory containing extracted .txt files.")
    parser.add_argument("--regex", action="store_true", help="Treat query as a regular expression.")
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Use case-sensitive matching. Default is case-insensitive.",
    )
    parser.add_argument(
        "--context",
        type=int,
        default=DEFAULT_CONTEXT,
        help="Number of surrounding lines to show on each side within the same page.",
    )
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS, help="Maximum number of matches.")
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

    rx = compile_query(args.query, args.regex, args.case_sensitive)
    results = iter_matches(text_dir=text_dir, rx=rx, context=args.context, max_results=max_results)

    print(f"query: {yaml_quote(args.query)}")
    print(f"mode: {yaml_quote('regex' if args.regex else 'plain')}")
    print(f"case_sensitive: {str(args.case_sensitive).lower()}")
    print(f"text_dir: {yaml_quote(text_dir.as_posix())}")
    print(f"max_results: {max_results}")
    print(f"results_found: {len(results)}")

    for result in results:
        print_result(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
