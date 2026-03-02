# esi-service

FastAPI microservice for ESI OAuth2 authentication. Exchanges PKCE authorization code for tokens, syncs user profile to PostgreSQL.

## Stack

- FastAPI + Uvicorn
- PostgreSQL + asyncpg (SQLAlchemy async)
- Alembic migrations
- Pydantic v2 / httpx

## Setup

```bash
cp .env-example .env  # fill in required vars
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t esi-service .
docker run -d -p 8000:8000 --env-file .env esi-service
```

## Environment

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | yes | `postgresql+asyncpg://user:pass@host/db` |
| `SECRET_KEY` | yes | JWT signing secret |
| `ESI_URL` | yes | ESI base URL |
| `ESI_CLIENT_ID` | yes | OAuth2 client ID |
| `ESI_CLIENT_SECRET` | yes | OAuth2 client secret |
| `ESI_REDIRECT_URI` | yes | OAuth2 callback URL |
| `ALLOWED_ORIGINS` | yes | Comma-separated CORS origins |
| `ALGORITHM` | no | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | no | Default: `30` |
| `IS_PRODUCTION` | no | Disables `/docs` and `/redoc` when `True` |

## API

### `POST /api/v1/esi_login`

Exchange authorization code for ESI access token and upsert user.

**Request**
```json
{
  "code": "authorization_code",
  "code_verifier": "pkce_verifier"
}
```

**Response**
```json
{
  "access_token": "...",
  "esi_user_id": 1,
  "esi_user_info": {
    "sub": "...",
    "name": "...",
    "email": "...",
    "organization_tin": "...",
    "organization_name": "...",
    "position_name": "...",
    "pin": "...",
    "citizenship": "KZ",
    "gender": "M",
    "birthdate": "1990-01-01",
    "phone_number": "..."
  }
}
```

| Status | Reason |
|---|---|
| 400 | Missing `code` or `code_verifier` |
| 500 | ESI service error |

## Migrations

```bash
alembic revision --autogenerate -m "description"  # new migration
alembic upgrade head                               # apply
alembic downgrade -1                               # rollback
```
