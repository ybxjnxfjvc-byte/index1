"""Small dependency-free repository security check.

It is intentionally conservative: it looks for accidental secrets and a few
security-relevant properties of the existing public HTML files.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "02_roli_v_sisteme_obucheniya_sber.html",
    ROOT / "03_trenazher_kross_prodazh_sber.html",
]

SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "aws-access-key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "generic-bearer": re.compile(r"Bearer\s+[A-Za-z0-9._-]{24,}"),
}

TEXT_EXTENSIONS = {".html", ".md", ".py", ".js", ".json", ".yml", ".yaml", ".txt", ".example", ".gitignore"}


def text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "playwright-report", "test-results"} for part in path.parts):
            continue
        if path.name == ".env.example" or path.name == ".gitignore" or path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for path in text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"possible {label}: {path.relative_to(ROOT)}")

    env_path = ROOT / ".env"
    if env_path.exists():
        failures.append(".env exists in repository working tree")

    trainer = ROOT / "03_trenazher_kross_prodazh_sber.html"
    if trainer.exists():
        text = trainer.read_text(encoding="utf-8")
        if "const RESULTS_ENDPOINT=''" not in text and 'const RESULTS_ENDPOINT=""' not in text:
            warnings.append("RESULTS_ENDPOINT is not visibly empty; review outbound result transmission")
        if ".textContent=user.name" not in text:
            warnings.append("could not confirm textContent is used for result participant name")
        if re.search(r"innerHTML\s*=\s*[^;]*(user\.name|user\.unit|\$\(['\"]name|\$\(['\"]unit)", text):
            failures.append("untrusted participant/unit appears to flow into innerHTML")

    for html in HTML_FILES:
        if not html.exists():
            warnings.append(f"expected existing case file not found: {html.name}")

    if failures:
        print("SECURITY CHECK: FAIL")
        for item in failures:
            print(" -", item)
        return 1

    print("SECURITY CHECK: PASS")
    for item in warnings:
        print(" warning:", item)
    print("Checked for common committed secrets and unsafe participant/unit HTML flow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
