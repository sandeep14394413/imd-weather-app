# India Weather Forecast App

Python application for user accounts and weather prediction UI/API.

## What this repo contains

- FastAPI backend with signup, login, and prediction endpoints.
- Streamlit user interface for selecting Indian state/location and forecast date.
- Client code that calls a model-serving API from the ML pipeline.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py
```

## API

- `POST /auth/signup`
- `POST /auth/login`
- `POST /forecast`
- `GET /health`

This first version uses SQLite and a simple local authentication flow. For production,
move secrets to a managed secret store and use PostgreSQL.

## Deploy to kind

Prerequisites:

- Docker
- kind
- kubectl pointed at your kind cluster
- The ML repo deployed first, so `imd-weather-ml` exists in the `imd-weather` namespace

Manual deployment:

```powershell
.\scripts\deploy-kind.ps1 -ClusterName kind -JwtSecret "replace-me"
kubectl -n imd-weather port-forward svc/imd-weather-ui 8501:8501
```

Then open `http://127.0.0.1:8501`.

GitHub Actions deployment:

- Uses `.github/workflows/deploy-kind.yml`.
- Requires a self-hosted runner on the machine that can access your kind cluster.
- Optional repository secret: `JWT_SECRET`.
