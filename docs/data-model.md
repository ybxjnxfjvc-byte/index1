# Data model and classification

The public trainer can form a result payload in memory. For security practice, each field is classified before any hypothetical server integration.

| Field | Type | Purpose | Sensitivity | Storage in public demo |
|---|---|---|---|---|
| `trainerId` | string | identify trainer version | low | memory only |
| `participant` | string | personalize result | personal data if real name | memory only |
| `unit` | string | contextual label | may reveal employment context | memory only |
| `score` | integer | result | low/medium with identity | memory only |
| `total` | integer | denominator | low | memory only |
| `completedAt` | ISO datetime | completion time | metadata | memory only |
| `answers` | array | detailed attempt | behavioral data | memory only |

## Minimization decision

For a real integration, prefer a pseudonymous participant identifier instead of a full name wherever business requirements allow it. Do not collect phone, e-mail, password, token, client account data or free-form comments in this trainer.

## Retention

The local lab is educational. Its SQLite file is ignored by Git and should be deleted after the exercise. A production retention period is deliberately not invented in this case.
