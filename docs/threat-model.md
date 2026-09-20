# Mini threat model — public demo + local lab

## Scope

The model covers only this repository, the browser session and the local training API. It does not model SBER infrastructure.

## Assets

1. Integrity of educational content and correct-answer logic.
2. Participant input entered into the demo.
3. Training score and completion metadata.
4. Local API bearer token.
5. Repository integrity and publication contents.

## Roles

- portfolio visitor / trainee;
- repository maintainer;
- local lab operator;
- untrusted web input.

## Trust boundaries

`user → browser DOM → optional localhost API → SQLite file`

`maintainer workstation → Git → GitHub repository → GitHub Pages`

## Risks and controls

| ID | Risk | Example | Control | Safe local check |
|---|---|---|---|---|
| T1 | DOM injection | name contains HTML/event handler | render untrusted values via `textContent`; validate lengths | Playwright payload remains text, no injected element appears |
| T2 | Secret disclosure | API token committed to Git | `.env` ignored; only placeholder in `.env.example`; secret scanner | run `python scripts/security_check.py` |
| T3 | Unauthorized result submission | request sent without valid token | bearer token checked with constant-time comparison | Python API test expects `401` |
| T4 | SQL injection / query corruption | apostrophe or SQL-looking string in participant | parameterized INSERT/SELECT only | Python test inserts `O'Reilly` and SQL-like input safely |
| T5 | Oversized/unexpected request | huge body or extra fields | 4096-byte limit + allow-list schema | API tests expect `413` / `400` |
| T6 | Sensitive logs | full name/unit/token written to log | event-only logging with lengths, score and request id | inspect three safe sample events |
| T7 | Misleading external security claim | repo interpreted as bank audit | explicit scope and disclaimer in README/SECURITY/EVIDENCE | documentation review |
| T8 | Unsafe publication | archive/token/local DB accidentally committed | prepublish checklist + Git ignore + CI static scan | run CI and `git status` before release |

## Residual risks

- GitHub Pages security headers are controlled by the hosting platform, not by this static repository.
- The original pages contain inline CSS/JS, so a strict CSP would require a structural refactor; this is documented rather than falsely claimed as implemented.
- The local bearer-token model is a learning control, not a production identity architecture.
