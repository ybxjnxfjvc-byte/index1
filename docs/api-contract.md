# Local training-results API contract

This contract belongs to the local lab only. It is not a SBER API.

## Endpoint

`POST /api/results`

Headers:
- `Authorization: Bearer <DEMO_API_TOKEN>`
- `Content-Type: application/json`

Maximum request body: 4096 bytes.

## Allowed JSON fields

Required:
- `trainerId`: string, 1..80 chars;
- `participant`: string, 1..80 chars;
- `unit`: string, 1..120 chars;
- `score`: integer, 0..1000;
- `total`: integer, 1..1000;
- `completedAt`: ISO-like string, 10..40 chars.

Optional:
- `answers`: array, max 100 items. The local lab stores only answer count, not the full array.

Unknown fields are rejected.

## Responses

- `201` — accepted and stored locally;
- `400` — invalid JSON/schema/values;
- `401` — missing or invalid bearer token;
- `404` — unknown path;
- `413` — body too large;
- `500` — unexpected error, without stack trace in response.

See `examples/api/valid-result.json` and `examples/api/invalid-extra-field.json`.
