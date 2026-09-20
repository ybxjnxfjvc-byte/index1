# User flow and trust boundaries

## Public demo

`open page → read lesson → choose answer → receive feedback → move to next page`

Trainer flow:

`enter name + unit → start → answer 10 situations → calculate score locally → show result`

Current public trainer does not require a server to show the result.

## Error branches

- name shorter than 3 characters → local validation message;
- unit shorter than 2 characters → local validation message;
- local API lab called without token → `401`;
- body is not valid JSON or contains unknown fields → `400`;
- body too large → `413`;
- unexpected local server error → generic `500`, details only in local console.

## Trust boundaries

1. **Browser / user input.** `name` and `unit` are untrusted.
2. **Static application constants.** Question texts and explanations are authored code, not user input.
3. **Optional local API lab.** Crossing this boundary requires schema validation and bearer authorization.
4. **SQLite file.** Only validated values are written, through parameterized SQL.
