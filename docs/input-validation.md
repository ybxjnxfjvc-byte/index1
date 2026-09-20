# Untrusted input review

## Inputs

The trainer has two free-text fields: participant name and team/unit. They are treated as untrusted strings even in a portfolio demo.

## Current browser behavior

Safe patterns:
- user name and unit are written to visible elements with `textContent`;
- answer buttons are created with `document.createElement` and their text is set through `textContent`;
- the result participant name is also assigned with `textContent`.

Maintenance risk:
- some UI blocks use `innerHTML` for data sourced from hard-coded arrays. That is acceptable only while the source remains trusted constants. If any of those arrays are ever populated from an API or user input, switch to explicit DOM creation / `textContent` or sanitize with a reviewed policy.

## Test values

The browser test uses strings such as:
- `<img src=x onerror=alert(1)>`
- `"><svg onload=alert(1)>`
- `O'Reilly`
- a 200-character value
- whitespace-only input

The goal is defensive verification: strings must remain strings and must not execute as markup.
