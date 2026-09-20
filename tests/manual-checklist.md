# Manual checklist — case 01

| ID | Scenario | Expected result |
|---|---|---|
| M01 | Open `index.html` by keyboard only | Skip link and focus are visible; lesson is navigable |
| M02 | Zoom browser to 200% | Main text remains readable, no critical content is lost |
| M03 | Enter `<img src=x onerror=alert(1)>` as participant name | String is displayed as text; no image/handler is created |
| M04 | Enter `O'Reilly` | Value is accepted as ordinary text |
| M05 | Enter spaces only | Start is blocked by validation |
| M06 | Finish trainer with endpoint unconfigured | Result is shown locally; no result request is required |
| M07 | Start local API without `DEMO_API_TOKEN` | Server refuses to start |
| M08 | POST valid payload without Authorization | `401`, no sensitive response details |
| M09 | POST JSON with extra `password` field | `400` |
| M10 | POST body larger than 4096 bytes | `413` |
| M11 | Store SQL-looking participant/unit strings | Record is stored as text; table remains intact |
| M12 | Inspect local API logs | Token, full participant and full unit are absent |
