# Accessibility check

Security practice does not replace accessibility QA; both are part of a reliable product.

Checklist for the three existing pages:

- [x] document language is Russian;
- [x] viewport is declared;
- [x] keyboard-visible focus styles exist;
- [x] skip links are present;
- [x] feedback areas use `aria-live`;
- [x] trainer answers use buttons rather than clickable divs;
- [x] reduced-motion media query is present;
- [ ] run final keyboard-only pass after any HTML change;
- [ ] verify all inter-page links in CI/smoke test.

The checklist intentionally distinguishes inspected code from checks that should be rerun after future edits.
