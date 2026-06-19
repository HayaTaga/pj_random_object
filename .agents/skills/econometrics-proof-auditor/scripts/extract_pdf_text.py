#!/usr/bin/env python3
"""Extract page-marked text from private PDFs without copying PDF files.

Run from the repository root:

    python .agents/skills/econometrics-proof-auditor/scripts/extract_pdf_text.py
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol


DEFAULT_PDF_DIR = Path("corpus/pdfs")
DEFAULT_OUT_DIR = Path("corpus/extracted")
DEFAULT_REPORT = Path("corpus/metadata/extraction_report.json")
LITTLE_TEXT_CHARS = 20


class Backend(Protocol):
    name: str

    def extract(self, pdf_path: Path) -> tuple[int, list[str], list[str]]:
        """Return (page_count, page_texts, warnings)."""


@dataclass
class PypdfBackend:
    name: str = "pypdf"

    def extract(self, pdf_path: Path) -> tuple[int, list[str], list[str]]:
        from pypdf import PdfReader

        warnings: list[str] = []
        reader = PdfReader(str(pdf_path))
        if getattr(reader, "is_encrypted", False):
            try:
                decrypt_result = reader.decrypt("")
                warnings.append(f"PDF is encrypted; attempted empty-password decrypt result={decrypt_result}.")
            except Exception as exc:
                raise RuntimeError(f"PDF is encrypted and could not be decrypted: {exc}") from exc

        page_texts: list[str] = []
        pages = list(reader.pages)
        for index, page in enumerate(pages, start=1):
            try:
                page_texts.append(page.extract_text() or "")
            except Exception as exc:
                warnings.append(f"Page {index}: text extraction failed: {exc}")
                page_texts.append("")
        return len(pages), page_texts, warnings


@dataclass
class PymupdfBackend:
    name: str = "pymupdf"

    def extract(self, pdf_path: Path) -> tuple[int, list[str], list[str]]:
        import fitz

        warnings: list[str] = []
        page_texts: list[str] = []
        with fitz.open(str(pdf_path)) as doc:
            if doc.needs_pass:
                if not doc.authenticate(""):
                    raise RuntimeError("PDF is encrypted and could not be decrypted with an empty password.")
                warnings.append("PDF is encrypted; opened with empty-password authentication.")
            for index, page in enumerate(doc, start=1):
                try:
                    page_texts.append(page.get_text("text") or "")
                except Exception as exc:
                    warnings.append(f"Page {index}: text extraction failed: {exc}")
                    page_texts.append("")
            return doc.page_count, page_texts, warnings


def select_backend(preferred: str = "auto") -> Backend:
    if preferred not in {"auto", "pypdf", "pymupdf"}:
        raise ValueError(f"Unknown backend: {preferred}")

    if preferred in {"auto", "pypdf"}:
        try:
            import pypdf  # noqa: F401

            return PypdfBackend()
        except ImportError:
            if preferred == "pypdf":
                raise

    if preferred in {"auto", "pymupdf"}:
        try:
            import fitz  # noqa: F401

            return PymupdfBackend()
        except ImportError:
            if preferred == "pymupdf":
                raise

    raise ImportError(
        "No supported PDF text extraction backend is installed.\n"
        "Install one of:\n"
        "  python -m pip install pypdf\n"
        "  python -m pip install pymupdf\n"
    )


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def output_path_for(pdf_path: Path, pdf_dir: Path, out_dir: Path) -> Path:
    """Mirror the PDF tree below corpus/extracted and replace .pdf with .txt."""
    relative = pdf_path.relative_to(pdf_dir)
    return out_dir / relative.with_suffix(".txt")


def normalized_len(text: str) -> int:
    return len("".join(text.split()))


def format_text(relative_source: Path, page_texts: list[str]) -> str:
    parts = [f"=== Source: {relative_source.as_posix()} ===", ""]
    for index, text in enumerate(page_texts, start=1):
        parts.append(f"=== Page {index} ===")
        parts.append(text.strip())
        parts.append("")
    return "\n".join(parts)


def extract_one(pdf_path: Path, pdf_dir: Path, out_dir: Path, backend: Backend, skip_existing: bool) -> dict:
    out_path = output_path_for(pdf_path, pdf_dir, out_dir)
    relative_source = pdf_path.relative_to(pdf_dir)
    timestamp = utc_timestamp()
    entry = {
        "source_filename": relative_source.as_posix(),
        "output_filename": out_path.as_posix(),
        "number_of_pages": None,
        "extraction_timestamp": timestamp,
        "backend": backend.name,
        "warnings": [],
        "pages_with_little_or_no_extracted_text": [],
        "status": "pending",
    }

    if out_path.exists() and skip_existing:
        entry["warnings"].append("Output already exists; skipped because --skip-existing was set.")
        entry["status"] = "skipped"
        return entry

    try:
        page_count, page_texts, warnings = backend.extract(pdf_path)
    except Exception as exc:
        entry["warnings"].append(f"Extraction failed: {exc}")
        entry["status"] = "error"
        return entry

    entry["number_of_pages"] = page_count
    entry["warnings"].extend(warnings)
    little_pages = [
        index for index, text in enumerate(page_texts, start=1) if normalized_len(text) < LITTLE_TEXT_CHARS
    ]
    entry["pages_with_little_or_no_extracted_text"] = little_pages

    if page_count == 0:
        entry["warnings"].append("PDF reported zero pages.")
    elif len(little_pages) == page_count:
        entry["warnings"].append(
            "Ordinary text extraction produced little or no text on every page. "
            "OCR was not attempted; configure an OCR pipeline only for these files if needed."
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(format_text(relative_source, page_texts), encoding="utf-8")
    entry["status"] = "ok"
    return entry


def write_report(report_path: Path, report: dict) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract ordinary text from all PDFs under corpus/pdfs into page-marked text files."
    )
    parser.add_argument("--pdf-dir", default=str(DEFAULT_PDF_DIR), help="Directory containing private PDFs.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for extracted .txt files.")
    parser.add_argument(
        "--report",
        default=str(DEFAULT_REPORT),
        help="JSON extraction report path.",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "pypdf", "pymupdf"],
        default="auto",
        help="Extraction backend. Default: pypdf if installed, otherwise PyMuPDF.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip PDFs whose output text file already exists. By default outputs are regenerated.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Deprecated compatibility flag; outputs are regenerated by default.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional development limit on number of PDFs.")
    args = parser.parse_args()

    pdf_dir = Path(args.pdf_dir)
    out_dir = Path(args.out_dir)
    report_path = Path(args.report)

    if not pdf_dir.exists():
        print(f"ERROR: PDF directory not found: {pdf_dir}", file=sys.stderr)
        return 2
    if not pdf_dir.is_dir():
        print(f"ERROR: PDF path is not a directory: {pdf_dir}", file=sys.stderr)
        return 2

    pdfs = sorted(p for p in pdf_dir.rglob("*.pdf") if p.is_file())
    if args.limit is not None:
        pdfs = pdfs[: args.limit]
    if not pdfs:
        print(f"ERROR: No PDFs found under {pdf_dir}", file=sys.stderr)
        return 1

    try:
        backend = select_backend(args.backend)
    except ImportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    entries = []
    for pdf_path in pdfs:
        entry = extract_one(pdf_path, pdf_dir, out_dir, backend, args.skip_existing)
        entries.append(entry)
        print(f"{entry['status']}: {entry['source_filename']} -> {entry['output_filename']}")
        for warning in entry["warnings"]:
            print(f"  warning: {warning}", file=sys.stderr)

    report = {
        "generated_at": utc_timestamp(),
        "pdf_dir": pdf_dir.as_posix(),
        "output_dir": out_dir.as_posix(),
        "backend": backend.name,
        "total_pdfs": len(entries),
        "ok": sum(1 for entry in entries if entry["status"] == "ok"),
        "skipped": sum(1 for entry in entries if entry["status"] == "skipped"),
        "errors": sum(1 for entry in entries if entry["status"] == "error"),
        "files": entries,
    }
    write_report(report_path, report)
    print(f"report: {report_path}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
