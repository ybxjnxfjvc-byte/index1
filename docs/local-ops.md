# Local operations

The lab binds only to localhost.

## Start

```bash
cp .env.example .env
# edit DEMO_API_TOKEN locally; never commit .env
python lab/mock_api.py
```

Default address: `http://127.0.0.1:8765`.

## Health check

```bash
curl http://127.0.0.1:8765/health
```

Expected response: `200` and `{"ok": true}`.

## Process / port diagnostics

Windows PowerShell:

```powershell
Get-NetTCPConnection -LocalPort 8765
Get-Process python
```

Linux/macOS:

```bash
lsof -i :8765
```

## Stop

Use `Ctrl+C` in the terminal that started the lab.

## Data cleanup

Delete the local database after the exercise:

```bash
rm -f lab/demo_results.db
```

On Windows PowerShell:

```powershell
Remove-Item .\lab\demo_results.db -ErrorAction SilentlyContinue
```
