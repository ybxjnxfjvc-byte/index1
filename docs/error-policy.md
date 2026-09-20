# Error policy

## User-facing errors

Expose only:
- what failed at a high level;
- what the user can do next;
- a stable HTTP status when API is involved.

Do not expose:
- stack traces;
- filesystem paths;
- bearer tokens;
- raw exception objects;
- SQL text with user values;
- environment variables.

## Local API examples

- invalid input → `{ "ok": false, "error": "invalid-request" }`;
- invalid auth → `{ "ok": false, "error": "unauthorized" }`;
- internal failure → `{ "ok": false, "error": "internal-error" }`.

Detailed diagnostics may be printed to the local console, but without secret or full free-text user fields.
