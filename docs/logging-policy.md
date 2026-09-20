# Safe logging policy

## Principle

Logs should help diagnose the local lab without becoming a second database of personal data or secrets.

## Allowed fields

- timestamp;
- event name;
- request id;
- HTTP status;
- trainer id;
- score/total;
- lengths of participant/unit strings;
- reason category such as `schema-rejected`.

## Forbidden fields

- bearer token / Authorization header;
- password, cookie, API key, private key;
- phone/e-mail;
- full participant name;
- full team/unit free text;
- raw request body;
- full exception traceback in HTTP response.

## Three safe example records

```json
{"event":"result.accepted","requestId":"demo-001","trainerId":"sber-cross-sales-v1","score":8,"total":10,"participantLength":12,"unitLength":16}
{"event":"request.rejected","requestId":"demo-002","reason":"unauthorized","status":401}
{"event":"request.rejected","requestId":"demo-003","reason":"schema-rejected","status":400}
```
