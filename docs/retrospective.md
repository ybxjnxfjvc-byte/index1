# Retrospective

## What became stronger

The original case demonstrated front-end/product work. The added security layer makes the review reproducible: a recruiter or engineer can open a threat model, run a scanner, start a localhost API and execute tests.

## Most useful skills demonstrated

1. **Trust-boundary thinking.** Even a static trainer has untrusted input and a future integration boundary.
2. **Evidence over claims.** Each security statement points to code, test or policy.
3. **Data minimization.** A result payload is examined field by field before storage is introduced.

## Gaps that remain

- no real production identity provider;
- no industrial observability/SIEM;
- no deployment to a backend environment;
- no authorized pentest of external systems;
- no claim of compliance certification.

## Next logical step

Build a separate neutral demo service (without third-party branding) with role-based access, expiring sessions, database migrations, structured audit events and containerized CI. That should be a new project, not silently attributed to this SBER-themed portfolio case.
