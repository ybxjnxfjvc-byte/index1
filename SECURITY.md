# Security policy for this demo repository

## Scope

Security practice in this repository applies only to the public static demo and the local lab under `lab/`.

## Not in scope

Do not test, scan, probe or attempt to access any Sberbank/SBER systems, domains, accounts, APIs or infrastructure on the basis of this repository. The project is not an authorization for external security testing.

## Secrets and personal data

- Never commit real API tokens, passwords, cookies, private keys or `.env` files.
- Do not commit real employee/customer data.
- Use synthetic names in screenshots and tests.
- The local API token is supplied only through an environment variable.

## Reporting an issue in this educational repository

Create a private note to the repository owner describing the affected file, reproduction steps and expected safe behavior. Do not include real credentials or third-party personal data.
