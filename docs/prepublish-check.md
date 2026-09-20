# Prepublication security checklist

Before every push that changes demo or lab files:

- [ ] `git status` shows no `.env`, `.db`, logs, browser profiles or archives;
- [ ] no real passwords/tokens/private keys exist in tracked files;
- [ ] screenshots and fixtures contain synthetic data only;
- [ ] no source archive with customer materials is committed;
- [ ] public HTML contains only intended assets and links;
- [ ] `python scripts/security_check.py` passes;
- [ ] `python -m unittest discover -s tests/python -v` passes;
- [ ] browser smoke/security test passes when Playwright is installed;
- [ ] README and EVIDENCE still distinguish demo from real bank infrastructure;
- [ ] local SQLite database is absent from the commit.
