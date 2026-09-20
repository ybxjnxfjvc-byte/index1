# Case 01 — СБЕР · система обучения

Публичный демонстрационный учебный кейс из трёх экранов: система обучения, ролевой маршрут и тренажёр кросс-продаж.

## Security practice layer

К интерфейсному кейсу добавлен отдельный проверяемый слой практики по информационной безопасности. Он относится **к этому публичному демо и локальному учебному стенду**, а не к инфраструктуре Сбербанка.

Начать просмотр лучше с [`EVIDENCE.md`](EVIDENCE.md).

### Что можно проверить в репозитории

- [`docs/threat-model.md`](docs/threat-model.md) — активы, границы доверия, угрозы и меры;
- [`docs/data-model.md`](docs/data-model.md) — минимизация и чувствительность полей результата;
- [`docs/api-contract.md`](docs/api-contract.md) — контракт локального учебного API;
- [`docs/logging-policy.md`](docs/logging-policy.md) — безопасные события без паролей, токенов и полного пользовательского ввода;
- [`lab/mock_api.py`](lab/mock_api.py) — локальный HTTP API с bearer-аутентификацией, ограничением тела и валидацией схемы;
- [`lab/sqlite_store.py`](lab/sqlite_store.py) — параметризованный SQLite;
- [`scripts/security_check.py`](scripts/security_check.py) — статическая проверка репозитория и отсутствие типовых секретов;
- [`tests/python/test_security_lab.py`](tests/python/test_security_lab.py) — автоматизированные проверки API/SQL;
- [`tests/playwright/security.spec.js`](tests/playwright/security.spec.js) — браузерные проверки пользовательского ввода и отсутствия передачи результата наружу;
- [`.github/workflows/security-check.yml`](.github/workflows/security-check.yml) — CI-проверка.

## Ограничение кейса

Названия и публичные материалы организации используются только как контекст учебного прототипа. Этот репозиторий не подтверждает заказ, внедрение или доступ к внутренним системам СБЕРа.
