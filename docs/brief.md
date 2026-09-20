# Brief — security practice for case 01

## Product in scope

Public educational demo consisting of three static HTML pages. The third page is an in-browser trainer that asks for a participant name and team/unit and calculates a score locally.

## User

A portfolio reviewer or junior security/product candidate who needs to demonstrate how a small front-end product is reviewed and prepared for safer integration.

## Problem

A polished interface alone does not prove secure engineering practice. The repository needs evidence that the author can identify data, trust boundaries, misuse cases and controls and can reproduce checks locally.

## Boundaries

In scope:
- files of this repository;
- browser behavior of the demo;
- local lab on `127.0.0.1`;
- synthetic test data.

Out of scope:
- any SBER internal system;
- external scanning or pentesting;
- real customer/employee data;
- production authentication/SSO.

## Done when

- every strong security claim points to a file or automated check;
- no real secret is committed;
- local API rejects missing/invalid authorization and malformed input;
- SQLite operations use placeholders;
- logs contain event metadata but no full participant input or token;
- CI can run without access to private infrastructure.
