# Example FastAPI App

This small scaffold provides a minimal FastAPI app under `src/` with a health route and tests.

Files created:
- `src/main.py` - FastAPI app and entrypoint
- `src/api/health.py` - /api/health route
- `tests/test_health.py` - pytest tests
- `requirements.txt` - Python dependencies

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Run tests:

```powershell
pip install -r requirements.txt
pytest -q
```
