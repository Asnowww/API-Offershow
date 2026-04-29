# OfferShow Backend

FastAPI backend for the Offer Show H5 mobile frontend.

## Quick Start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m app.scripts.import_frontend_mock
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs:

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

Demo accounts:

- `demo` / `demo`, role `user`
- `hr` / `hr`, role `hr`
- `admin` / `admin`, role `admin`
- `cheater` / `cheater`, write operations blocked
- `crawler` / `crawler`, read operations blocked by risk control

Database note: the provided PostgreSQL account does not have `CREATE DATABASE` permission. The project uses the existing `aqimonitor` database and isolates all OfferShow tables under the `offershow` schema.

Data note: `python -m app.scripts.import_frontend_mock` imports the generated data from `frontend/src/api/mockData.js`, so backend responses use the same demo dataset as the frontend mock mode.

The frontend can switch from mock data by setting `VITE_USE_MOCK=false`.

If the background dev server was started by Codex, stop it with:

```powershell
Stop-Process -Id (Get-Content .\uvicorn.pid) -Force
```
